import time

import pandas as pd
import tls_requests

from src.config import FOTMOB_LEAGUES, FOTMOB_STATS, MINIMUM_MINUTES, OUTPUT_DIR

BASE_API = "https://www.fotmob.com/api"
SEARCH_API = "https://www.fotmob.com/api/data/search/suggest"
DATA_API = "https://data.fotmob.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    ),
}
RATE_LIMIT = 1.0


def _cache_path(season: str):
    return OUTPUT_DIR / f"raw_all_players_{season.replace('/', '_')}.csv"


class FotMobFetcher:
    def __init__(self):
        self._session = tls_requests.Client(headers=HEADERS)
        self._tournament_ids: dict[str, int] = {}

    def fetch_all(self, season: str, use_cache: bool = False) -> pd.DataFrame:
        cache = _cache_path(season)
        if use_cache and cache.exists():
            print(f"Loading cached FotMob data for {season}...")
            return pd.read_csv(cache)

        print(f"Fetching FotMob data for {season}...")
        self._resolve_tournament_ids(season)
        stats_df = self._fetch_all_stats()
        squads_df = self._fetch_all_squads(stats_df)
        merged = stats_df.merge(
            squads_df[["player_id", "position"]],
            on="player_id",
            how="left",
        )
        merged = merged[merged["minutes_played"] >= MINIMUM_MINUTES]

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        merged.to_csv(cache, index=False)
        print(f"  Cached {len(merged)} players to {cache}")
        return merged

    def _resolve_tournament_ids(self, season: str):
        self._tournament_ids = {}
        self._league_tables: dict[int, int] = {}
        for league_name, league_id in FOTMOB_LEAGUES.items():
            print(f"  Resolving {league_name} ({season})...")
            resp = self._get(f"{BASE_API}/leagues?id={league_id}")
            links = resp["stats"]["seasonStatLinks"]
            for link in links:
                if link["Name"] == season:
                    self._tournament_ids[league_name] = link["TournamentId"]
                    break
            for section in resp.get("table", []):
                rows = section.get("data", {}).get("table", {}).get("all", [])
                num_teams = len(rows)
                for row in rows:
                    position = row.get("idx", num_teams)
                    self._league_tables[row["id"]] = self._team_strength(
                        position, num_teams,
                    )

    def _fetch_all_stats(self) -> pd.DataFrame:
        all_rows = []
        for league_name, tourn_id in self._tournament_ids.items():
            league_id = FOTMOB_LEAGUES[league_name]
            print(f"  Stats: {league_name}...")
            for stat_name in FOTMOB_STATS:
                url = (
                    f"{DATA_API}/stats/{league_id}"
                    f"/season/{tourn_id}/{stat_name}.json"
                )
                try:
                    data = self._get(url)
                except Exception:
                    continue
                for top_list in data.get("TopLists", []):
                    for p in top_list.get("StatList", []):
                        all_rows.append({
                            "player_id": p["ParticiantId"],
                            "player": p["ParticipantName"],
                            "team_id": p["TeamId"],
                            "team": p["TeamName"],
                            "league": league_name,
                            "stat_name": stat_name,
                            "stat_value": p["StatValue"],
                            "minutes_played": p["MinutesPlayed"],
                            "matches_played": p["MatchesPlayed"],
                        })
        long_df = pd.DataFrame(all_rows)
        if long_df.empty:
            raise RuntimeError("No data fetched from FotMob")
        meta = ["player_id", "player", "team_id", "team", "league"]
        minutes = (
            long_df.groupby(meta)[["minutes_played", "matches_played"]]
            .max()
            .reset_index()
        )
        wide = long_df.pivot_table(
            index=meta,
            columns="stat_name",
            values="stat_value",
            aggfunc="first",
        ).reset_index()
        wide.columns.name = None
        return wide.merge(minutes, on=meta, how="left")

    def _fetch_all_squads(self, stats_df: pd.DataFrame) -> pd.DataFrame:
        team_ids = stats_df["team_id"].unique()
        rows = []
        print(f"  Fetching squads for {len(team_ids)} teams...")
        for tid in team_ids:
            try:
                data = self._get(f"{BASE_API}/teams?id={int(tid)}&tab=squad")
            except Exception:
                continue
            for group in data.get("squad", {}).get("squad", []):
                for member in group.get("members", []):
                    role = member.get("role", {})
                    rows.append({
                        "player_id": member.get("id"),
                        "position": role.get("fallback", "Unknown")
                        if isinstance(role, dict)
                        else "Unknown",
                    })
        return pd.DataFrame(rows).drop_duplicates(subset="player_id")

    def search_players(self, term: str, limit: int = 10) -> list[dict]:
        data = self._get(f"{SEARCH_API}?term={term}")
        results = []
        for section in data:
            if section.get("title", {}).get("key") == "players":
                for s in section.get("suggestions", [])[:limit]:
                    if s.get("type") == "player" and not s.get("isCoach"):
                        results.append({
                            "player_id": int(s["id"]),
                            "player": s["name"],
                            "team_id": int(s["teamId"]),
                            "team": s["teamName"],
                        })
        return results

    def resolve_player_league(self, team_id: int) -> tuple[str, int]:
        data = self._get(f"{BASE_API}/teams?id={team_id}&tab=overview")
        details = data.get("details", {})
        league_id = details.get("primaryLeagueId")
        league_name = details.get("primaryLeagueName", "Unknown")
        country = details.get("country", "")
        if country and not league_name.startswith(country):
            league_name = f"{country}-{league_name}"
        return league_name, league_id

    def resolve_tournament_id(self, league_id: int, season: str) -> int | None:
        resp = self._get(f"{BASE_API}/leagues?id={league_id}")
        for link in resp.get("stats", {}).get("seasonStatLinks", []):
            if link["Name"] == season:
                return link["TournamentId"]
        return None

    def fetch_single_player_stats(
        self,
        player_id: int,
        team_id: int,
        league_id: int,
        tournament_id: int,
        league_name: str,
    ) -> pd.DataFrame | None:
        all_rows: list[dict] = []
        for stat_name in FOTMOB_STATS:
            url = f"{DATA_API}/stats/{league_id}/season/{tournament_id}/{stat_name}.json"
            try:
                data = self._get(url)
            except Exception:
                continue
            for top_list in data.get("TopLists", []):
                for p in top_list.get("StatList", []):
                    if p["ParticiantId"] == player_id:
                        all_rows.append({
                            "player_id": p["ParticiantId"],
                            "player": p["ParticipantName"],
                            "team_id": p["TeamId"],
                            "team": p["TeamName"],
                            "league": league_name,
                            "stat_name": stat_name,
                            "stat_value": p["StatValue"],
                            "minutes_played": p["MinutesPlayed"],
                            "matches_played": p["MatchesPlayed"],
                        })
        if not all_rows:
            return None
        long_df = pd.DataFrame(all_rows)
        meta = ["player_id", "player", "team_id", "team", "league"]
        minutes = (
            long_df.groupby(meta)[["minutes_played", "matches_played"]]
            .max()
            .reset_index()
        )
        wide = long_df.pivot_table(
            index=meta, columns="stat_name", values="stat_value", aggfunc="first",
        ).reset_index()
        wide.columns.name = None
        merged = wide.merge(minutes, on=meta, how="left")

        for stat_col in FOTMOB_STATS:
            if stat_col not in merged.columns:
                merged[stat_col] = 0.0

        position = self._fetch_player_position(team_id, player_id)
        merged["position"] = position
        return merged

    def _fetch_player_position(self, team_id: int, player_id: int) -> str:
        try:
            data = self._get(f"{BASE_API}/teams?id={team_id}&tab=squad")
        except Exception:
            return "Unknown"
        for group in data.get("squad", {}).get("squad", []):
            for member in group.get("members", []):
                if member.get("id") == player_id:
                    role = member.get("role", {})
                    return role.get("fallback", "Unknown") if isinstance(role, dict) else "Unknown"
        return "Unknown"

    @staticmethod
    def _team_strength(position: int, num_teams: int) -> float:
        return 1.10 - (position - 1) / max(num_teams - 1, 1) * 0.20

    def _get(self, url: str) -> dict:
        time.sleep(RATE_LIMIT)
        resp = self._session.get(url)
        resp.raise_for_status()
        return resp.json()
