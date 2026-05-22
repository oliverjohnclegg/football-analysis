from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class TuchelSecondarySixEightProfile(PositionalProfile):
    name = "Tuchel #6/8 – Ball-Winning Pivot"
    slug = "tuchel/secondary_6_8"
    position_keywords = ["Mid"]

    dimension_weights = {
        "counterpress_lead": 0.35,
        "vertical_disruption": 0.30,
        "second_ball_coverage": 0.20,
        "link_on_turnover": 0.15,
    }

    radar_labels = [
        "Counterpress\nLead",
        "Vertical\nDisruption",
        "Second-Ball\nCoverage",
        "Link on\nTurnover",
    ]

    ranking_title = "Top 25 – Tuchel System Ball-Winning #6/8 Profile Fit"
    radar_title = "Top 5 Ball-Winning #6/8 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "counterpress_lead", "vertical_disruption",
            "Counterpress Lead Score", "Vertical Disruption Score",
            "Press vs Interception",
            "press_vs_disruption.png",
        ),
        ScatterChart(
            "second_ball_coverage", "link_on_turnover",
            "Second-Ball Coverage Score", "Link on Turnover Score",
            "Coverage vs Link Play",
            "coverage_vs_link.png",
        ),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        passes = df.get("accurate_pass", 0)
        chances = df.get("total_att_assist", 0)
        df["chance_creation_rate"] = safe_ratio(chances, passes)

    def _compute_dimensions(self, df, nineties):
        df["counterpress_lead"] = (
            pctl(df["poss_won_att_3rd"]) * 0.40
            + pctl(df["total_tackle"]) * 0.30
            + pctl(df["clean_defend_rate"]) * 0.30
        )

        df["vertical_disruption"] = (
            pctl(df["interception"]) * 0.50
            + pctl(df["interception_share"]) * 0.50
        )

        df["second_ball_coverage"] = (
            pctl(df["total_tackle"]) * 0.50
            + pctl(df["effective_clearance"]) * 0.50
        )

        df["link_on_turnover"] = (
            pctl(df["accurate_pass"]) * 0.50
            + pctl(df["chance_creation_rate"]) * 0.50
        )
