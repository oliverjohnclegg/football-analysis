import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd

from src.config import OUTPUT_DIR
from src.nationality_service import NationalityService


def collect_player_ids() -> list[int]:
    player_ids: set[int] = set()
    for csv_path in OUTPUT_DIR.glob("**/*.csv"):
        if csv_path.name == "player_nationalities.csv":
            continue
        df = pd.read_csv(csv_path, usecols=lambda column: column == "player_id")
        if "player_id" not in df.columns:
            continue
        player_ids.update(df["player_id"].dropna().astype(int).tolist())
    return sorted(player_ids)


def patch_analysis_files(nationality_map: dict[int, str]) -> int:
    updated_files = 0
    for analysis_path in OUTPUT_DIR.glob("*/*/analysis.csv"):
        df = pd.read_csv(analysis_path)
        if "player_id" not in df.columns:
            continue
        df["nationality"] = df["player_id"].astype(int).map(nationality_map).fillna("Unknown")
        df.to_csv(analysis_path, index=False)
        updated_files += 1
    return updated_files


def patch_raw_caches(nationality_map: dict[int, str]) -> int:
    updated_files = 0
    for raw_path in OUTPUT_DIR.glob("raw_all_players_*.csv"):
        df = pd.read_csv(raw_path)
        if "player_id" not in df.columns:
            continue
        df["nationality"] = df["player_id"].astype(int).map(nationality_map).fillna("Unknown")
        df.to_csv(raw_path, index=False)
        updated_files += 1
    return updated_files


def main():
    parser = argparse.ArgumentParser(description="Backfill player nationality cache and CSVs.")
    parser.add_argument("--limit", type=int, default=None, help="Only fetch this many missing players")
    args = parser.parse_args()

    player_ids = collect_player_ids()
    if args.limit is not None:
        service = NationalityService()
        missing = [pid for pid in player_ids if service.get(pid) is None][: args.limit]
        nationality_map = service.ensure(missing, show_progress=True)
        nationality_map.update(service._cache)
    else:
        service = NationalityService()
        nationality_map = service.ensure(player_ids, show_progress=True)

    raw_updated = patch_raw_caches(nationality_map)
    analysis_updated = patch_analysis_files(nationality_map)
    print(f"Cached {len(nationality_map)} nationalities")
    print(f"Updated {raw_updated} raw caches and {analysis_updated} analysis files")


if __name__ == "__main__":
    main()
