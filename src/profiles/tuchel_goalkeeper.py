from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class TuchelGoalkeeperProfile(PositionalProfile):
    name = "Tuchel GK – Sweeper-Distributor"
    slug = "tuchel/goalkeeper"
    position_keywords = ["Keeper"]

    dimension_weights = {
        "build_up_involvement": 0.40,
        "shot_stopping": 0.35,
        "sweeper_behind_line": 0.25,
    }

    radar_labels = [
        "Build-Up\nInvolvement",
        "Shot\nStopping",
        "Sweeper\nBehind Line",
    ]

    ranking_title = "Top 25 – Tuchel System GK Profile Fit"
    radar_title = "Top 5 GK Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "build_up_involvement", "shot_stopping",
            "Build-Up Involvement Score", "Shot-Stopping Score",
            "Circulation vs Shot-Stopping",
            "build_up_vs_stopping.png",
        ),
        ScatterChart(
            "sweeper_behind_line", "build_up_involvement",
            "Sweeper Behind Line Score", "Build-Up Involvement Score",
            "Sweeping vs Distribution",
            "sweeper_vs_build_up.png",
        ),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        matches = df.get("matches_played", 1).clip(lower=1)
        df["saves_per_match"] = safe_ratio(df.get("saves", 0), matches)
        df["clean_sheet_rate"] = safe_ratio(df.get("clean_sheet", 0), matches)

    def _compute_dimensions(self, df, nineties):
        df["build_up_involvement"] = (
            pctl(df["accurate_pass"]) * 0.40
            + pctl(df["progressive_pass_share"]) * 0.30
            + pctl(df["accurate_long_balls"]) * 0.30
        )

        df["shot_stopping"] = (
            pctl(df["saves_per_match"]) * 0.50
            + pctl(df["clean_sheet_rate"]) * 0.50
        )

        df["sweeper_behind_line"] = (
            pctl(df["effective_clearance"]) * 0.50
            + pctl(df["accurate_pass"]) * 0.30
            + pctl(df["clean_sheet_rate"]) * 0.20
        )
