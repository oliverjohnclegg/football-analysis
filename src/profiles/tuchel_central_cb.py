from src.profiles.base import PositionalProfile, ScatterChart, pctl


class TuchelCentralCBProfile(PositionalProfile):
    name = "Tuchel Central CB – Organiser Anchor"
    slug = "tuchel/central_cb"
    position_keywords = ["Defender"]

    dimension_weights = {
        "circulation_security": 0.35,
        "depth_protection": 0.35,
        "aerial_clearance": 0.30,
    }

    radar_labels = [
        "Circulation\nSecurity",
        "Depth\nProtection",
        "Aerial\nClearance",
    ]

    ranking_title = "Top 25 – Tuchel System Central CB Profile Fit"
    radar_title = "Top 5 Central CB Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "circulation_security", "depth_protection",
            "Circulation Security Score", "Depth Protection Score",
            "Distribution vs Depth Cover",
            "circulation_vs_depth.png",
        ),
        ScatterChart(
            "aerial_clearance", "depth_protection",
            "Aerial Clearance Score", "Depth Protection Score",
            "Aerial Command vs Positional Defence",
            "aerial_vs_depth.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["circulation_security"] = (
            pctl(df["accurate_pass"]) * 0.40
            + pctl(df["progressive_pass_share"]) * 0.35
            + pctl(df["fouls"], ascending=False) * 0.25
        )

        df["depth_protection"] = (
            pctl(df["interception"]) * 0.30
            + pctl(df["interception_share"]) * 0.30
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["outfielder_block"]) * 0.15
        )

        df["aerial_clearance"] = (
            pctl(df["effective_clearance"]) * 0.50
            + pctl(df["outfielder_block"]) * 0.30
            + pctl(df["interception"]) * 0.20
        )
