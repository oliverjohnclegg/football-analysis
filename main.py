import argparse

import pandas as pd

from src.fotmob_fetcher import FotMobFetcher
from src.charts import render_all
from src.config import (
    OUTPUT_DIR, SEASON_WEIGHTS, PRIMARY_SEASON, MINIMUM_MINUTES_COMBINED,
)
from src.profiles import PROFILES


def main():
    args = _parse_args()
    profile_cls = PROFILES[args.profile]
    profile = profile_cls()

    print(f"Profile: {profile.name}\n")

    fetcher = FotMobFetcher()
    season_results = {}

    for season in SEASON_WEIGHTS:
        raw = fetcher.fetch_all(season=season, use_cache=args.cached)
        filtered = profile.filter_position(raw)

        if filtered.empty:
            print(f"  No position matches for {season}, skipping")
            continue

        print(f"  {season}: {len(filtered)} players matched position filter")
        print(f"  Computing {profile.name} metrics for {season}...")
        season_results[season] = profile.build(filtered)

    if not season_results:
        print("No players matched in any season.")
        return

    results = _combine_and_blend(season_results, profile)

    if results.empty:
        print("No eligible players after applying minutes thresholds.")
        return

    print(f"\nAnalyzed {len(results)} players\n")
    _print_summary(results, profile)

    print("\nGenerating visualizations...")
    render_all(results, profile)

    out_dir = OUTPUT_DIR / profile.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(out_dir / "analysis.csv", index=False)
    print(f"\nFull results exported to {out_dir / 'analysis.csv'}")


def _combine_and_blend(season_results, profile):
    primary = season_results.get(PRIMARY_SEASON)
    prior_seasons = {s: df for s, df in season_results.items() if s != PRIMARY_SEASON}

    if primary is not None:
        combined = primary.copy()
        combined["has_primary_season"] = True
    else:
        combined = pd.DataFrame()
    existing_ids = set(combined["player_id"]) if not combined.empty else set()

    for season, prior in prior_seasons.items():
        prior_only = prior[~prior["player_id"].isin(existing_ids)]
        eligible = prior_only[prior_only["minutes_played"] >= MINIMUM_MINUTES_COMBINED].copy()
        if not eligible.empty:
            eligible["has_primary_season"] = False
            print(f"  {len(eligible)} eligible players from {season} only "
                  f"({MINIMUM_MINUTES_COMBINED}+ min)")
            combined = pd.concat([combined, eligible], ignore_index=True)

    if combined.empty:
        return combined

    for season, prior in prior_seasons.items():
        weight = SEASON_WEIGHTS[season]
        print(f"\nBlending {season} (weight={weight})...")
        combined = _blend_seasons(combined, prior, profile, weight)

    return combined


def _blend_seasons(
    current: pd.DataFrame,
    prior: pd.DataFrame,
    profile,
    prior_weight: float,
) -> pd.DataFrame:
    dim_cols = list(profile.dimension_weights.keys())
    prior_subset = prior[["player_id"] + dim_cols].rename(
        columns={c: f"{c}_prior" for c in dim_cols},
    )

    blended = current.merge(prior_subset, on="player_id", how="left")

    for col in dim_cols:
        prior_col = f"{col}_prior"
        has_prior = blended[prior_col].notna()
        denom = has_prior.astype(float) * prior_weight + 1.0
        blended[col] = (
            blended[col] + blended[prior_col].fillna(0) * prior_weight
        ) / denom
        blended.drop(columns=[prior_col], inplace=True)

    blended["composite_score"] = profile.geometric_composite(blended)
    return blended.sort_values("composite_score", ascending=False)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        choices=list(PROFILES.keys()),
        default="number_six",
    )
    parser.add_argument("--cached", action="store_true")
    return parser.parse_args()


def _print_summary(df: pd.DataFrame, profile, n=20):
    cols = [c for c in profile.summary_columns() if c in df.columns]
    print(df[cols].head(n).to_string(
        index=False, float_format="{:.1f}".format,
    ))


if __name__ == "__main__":
    main()
