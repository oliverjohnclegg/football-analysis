from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class FletcherGoalkeeperProfile(PositionalProfile):
    name = "Fletcher GK – Sweeper-Distributor"
    slug = "fletcher/goalkeeper"
    position_keywords = ["Keeper"]

    dimension_weights = {
        "shot_stopping": 0.30,
        "distribution": 0.40,
        "sweeper_command": 0.30,
    }

    radar_labels = [
        "Shot\nStopping",
        "Distribution",
        "Sweeper\nCommand",
    ]

    ranking_title = "Top 25 – Fletcher System GK Profile Fit"
    radar_title = "Top 5 GK Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "distribution", "shot_stopping",
            "Distribution Score", "Shot-Stopping Score",
            "Build-Up Composure vs Shot-Stopping",
            "distribution_vs_stopping.png",
        ),
        ScatterChart(
            "sweeper_command", "distribution",
            "Sweeper Command Score", "Distribution Score",
            "Sweeping vs Distributing",
            "sweeping_vs_distributing.png",
        ),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        matches = df.get("matches_played", 1).clip(lower=1)
        df["saves_per_match"] = safe_ratio(df.get("saves", 0), matches)
        df["clean_sheet_rate"] = safe_ratio(df.get("clean_sheet", 0), matches)

    def _compute_dimensions(self, df, nineties):
        df["shot_stopping"] = (
            pctl(df["saves_per_match"]) * 0.50
            + pctl(df["clean_sheet_rate"]) * 0.50
        )

        df["distribution"] = (
            pctl(df["accurate_pass"]) * 0.30
            + pctl(df["accurate_long_balls"]) * 0.35
            + pctl(df["progressive_pass_share"]) * 0.35
        )

        df["sweeper_command"] = (
            pctl(df["effective_clearance"]) * 0.45
            + pctl(df["clean_sheet_rate"]) * 0.30
            + pctl(df["accurate_pass"]) * 0.25
        )
