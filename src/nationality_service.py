import json
import re
import time
from pathlib import Path

import pandas as pd
import tls_requests

from src.config import OUTPUT_DIR

NATIONALITY_CACHE_PATH = OUTPUT_DIR / "player_nationalities.csv"
NATIONALITY_FETCH_DELAY = 0.75


class NationalityService:
    def __init__(self, session: tls_requests.Client | None = None):
        self._session = session or tls_requests.Client(
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
                ),
            },
        )
        self._cache: dict[int, str] = self._load_cache()

    def get(self, player_id: int) -> str | None:
        return self._cache.get(int(player_id))

    def fetch(self, player_id: int) -> str:
        player_id = int(player_id)
        cached = self._cache.get(player_id)
        if cached:
            return cached

        nationality = self._fetch_from_player_page(player_id)
        self._cache[player_id] = nationality
        self._save_cache()
        return nationality

    def ensure(self, player_ids: list[int], show_progress: bool = False) -> dict[int, str]:
        missing = [int(pid) for pid in player_ids if int(pid) not in self._cache]
        total = len(missing)
        for index, player_id in enumerate(missing, start=1):
            if show_progress and index % 25 == 0:
                print(f"  Nationality: {index}/{total}")
            self.fetch(player_id)
        return {int(pid): self._cache[int(pid)] for pid in player_ids if int(pid) in self._cache}

    def enrich_dataframe(self, df: pd.DataFrame, fetch_missing: bool = False) -> pd.DataFrame:
        if df.empty or "player_id" not in df.columns:
            return df

        result = df.copy()
        if "nationality" in result.columns:
            result = result.drop(columns=["nationality"])

        player_ids = result["player_id"].dropna().astype(int).unique().tolist()
        if fetch_missing:
            self.ensure(player_ids)

        nationality_map = {
            int(pid): self._cache.get(int(pid), "Unknown")
            for pid in player_ids
        }
        result["nationality"] = result["player_id"].astype(int).map(nationality_map)
        result["nationality"] = result["nationality"].fillna("Unknown")
        return result

    def _fetch_from_player_page(self, player_id: int) -> str:
        time.sleep(NATIONALITY_FETCH_DELAY)
        response = self._session.get(f"https://www.fotmob.com/players/{player_id}")
        response.raise_for_status()

        match = re.search(
            r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',
            response.text,
            re.DOTALL,
        )
        if not match:
            return "Unknown"

        page_data = json.loads(match.group(1))
        player_information = (
            page_data.get("props", {})
            .get("pageProps", {})
            .get("data", {})
            .get("playerInformation", [])
        )
        for item in player_information:
            if item.get("title") == "Country":
                value = item.get("value") or {}
                fallback = value.get("fallback")
                if isinstance(fallback, str) and fallback.strip():
                    return fallback.strip()
        return "Unknown"

    def _load_cache(self) -> dict[int, str]:
        if not NATIONALITY_CACHE_PATH.exists():
            return {}
        cache_df = pd.read_csv(NATIONALITY_CACHE_PATH)
        if cache_df.empty:
            return {}
        return {
            int(row.player_id): str(row.nationality)
            for row in cache_df.itertuples(index=False)
        }

    def _save_cache(self) -> None:
        if not self._cache:
            return
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cache_df = pd.DataFrame(
            [{"player_id": pid, "nationality": nat} for pid, nat in sorted(self._cache.items())],
        )
        cache_df.to_csv(NATIONALITY_CACHE_PATH, index=False)
