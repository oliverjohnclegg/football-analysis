import pandas as pd

from src.config import OUTPUT_DIR, SEASON_WEIGHTS, PRIMARY_SEASON
from src.fotmob_fetcher import FotMobFetcher
from src.profiles import PROFILES


class DuplicatePlayerError(Exception):
    pass


class PlayerNotFoundError(Exception):
    pass


class ManualAddService:
    def __init__(self):
        self._fetcher = FotMobFetcher()

    def add_player(self, player_id: int, team_id: int) -> list[str]:
        league_name, league_id = self._fetcher.resolve_player_league(team_id)
        raw_cache = self._load_raw_cache()

        raw_per_season: dict[str, pd.DataFrame] = {}
        for season in SEASON_WEIGHTS:
            tournament_id = self._fetcher.resolve_tournament_id(league_id, season)
            if tournament_id is None:
                continue
            player_df = self._fetcher.fetch_single_player_stats(
                player_id, team_id, league_id, tournament_id, league_name,
            )
            if player_df is not None and not player_df.empty:
                raw_per_season[season] = player_df

        if not raw_per_season:
            raise PlayerNotFoundError(
                "No stats found for this player in any configured season."
            )

        position = raw_per_season[next(iter(raw_per_season))].iloc[0].get("position", "")
        added_to: list[str] = []

        for slug, profile_cls in PROFILES.items():
            csv_path = OUTPUT_DIR / slug / "analysis.csv"
            if not csv_path.exists():
                continue

            profile = profile_cls()
            if not self._position_matches(position, profile.position_keywords):
                continue

            df = pd.read_csv(csv_path)
            if player_id in df["player_id"].values:
                continue

            row = self._build_player_row(
                player_id, raw_per_season, raw_cache, profile,
            )
            if row is None or row.empty:
                continue

            row["is_manual_add"] = True
            if "is_manual_add" not in df.columns:
                df["is_manual_add"] = False

            df = pd.concat([df, row], ignore_index=True)
            df.to_csv(csv_path, index=False)
            added_to.append(slug)

        if not added_to:
            raise PlayerNotFoundError(
                "Player position did not match any existing role profiles, "
                "or they already exist in all matching datasets."
            )

        return added_to

    @staticmethod
    def _position_matches(position: str, keywords: list[str]) -> bool:
        if not position:
            return False
        for keyword in keywords:
            if keyword.lower() in position.lower():
                return True
        return False

    def _build_player_row(
        self,
        player_id: int,
        raw_per_season: dict[str, pd.DataFrame],
        raw_cache: dict[str, pd.DataFrame],
        profile,
    ) -> pd.DataFrame | None:
        season_frames: dict[str, pd.DataFrame] = {}

        for season, player_df in raw_per_season.items():
            population = raw_cache.get(season)
            if population is not None and not population.empty:
                population = population[population["player_id"] != player_id]
                combined = pd.concat([population, player_df], ignore_index=True)
            else:
                combined = player_df

            built = profile.build(combined)
            built_row = built[built["player_id"] == player_id]
            if not built_row.empty:
                season_frames[season] = built_row.head(1)

        if not season_frames:
            return None

        return self._combine_and_blend(season_frames, profile)

    @staticmethod
    def _combine_and_blend(
        season_frames: dict[str, pd.DataFrame], profile,
    ) -> pd.DataFrame:
        primary = season_frames.get(PRIMARY_SEASON)
        prior_seasons = {s: df for s, df in season_frames.items() if s != PRIMARY_SEASON}

        if primary is not None:
            combined = primary.copy()
            combined["has_primary_season"] = True
        elif prior_seasons:
            first_key = next(iter(prior_seasons))
            combined = prior_seasons.pop(first_key).copy()
            combined["has_primary_season"] = False
        else:
            return pd.DataFrame()

        dim_cols = list(profile.dimension_weights.keys())
        for _season, prior in prior_seasons.items():
            weight = SEASON_WEIGHTS[_season]
            prior_subset = prior[["player_id"] + dim_cols].rename(
                columns={c: f"{c}_prior" for c in dim_cols},
            )
            combined = combined.merge(prior_subset, on="player_id", how="left")
            for col in dim_cols:
                prior_col = f"{col}_prior"
                has_prior = combined[prior_col].notna()
                denom = has_prior.astype(float) * weight + 1.0
                combined[col] = (
                    combined[col] + combined[prior_col].fillna(0) * weight
                ) / denom
                combined.drop(columns=[prior_col], inplace=True)
            combined["composite_score"] = profile.geometric_composite(combined)

        return combined

    @staticmethod
    def _load_raw_cache() -> dict[str, pd.DataFrame]:
        result = {}
        for season in SEASON_WEIGHTS:
            cache_file = OUTPUT_DIR / f"raw_all_players_{season.replace('/', '_')}.csv"
            if cache_file.exists():
                result[season] = pd.read_csv(cache_file)
        return result
