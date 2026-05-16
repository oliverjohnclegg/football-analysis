from src.profiles.base import PositionalProfile, ScatterChart, pctl


class RoseniorWideCBProfile(PositionalProfile):
    name = "Rosenior Wide CB – Stepping Cover Defender"
    slug = "rosenior/wide_cb"
    position_keywords = ["Defender"]

    dimension_weights = {
        "positional_versatility": 0.30,
        "rest_defence": 0.25,
        "wide_coverage": 0.25,
        "counter_press": 0.20,
    }

    radar_labels = [
        "Positional\nVersatility",
        "Rest\nDefence",
        "Wide\nCoverage",
        "Counter-\nPress",
    ]

    ranking_title = "Top 25 – Rosenior System Wide CB Profile Fit"
    radar_title = "Top 5 Wide CB Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "positional_versatility", "rest_defence",
            "Positional Versatility Score", "Rest Defence Score",
            "Versatility vs Defensive Solidity",
            "versatility_vs_defence.png",
        ),
        ScatterChart(
            "wide_coverage", "counter_press",
            "Wide Coverage Score", "Counter-Press Score",
            "Wide Defending vs Counter-Pressing",
            "wide_vs_counterpress.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["positional_versatility"] = (
            pctl(df["accurate_pass"]) * 0.30
            + pctl(df["won_contest"]) * 0.25
            + pctl(df["carry_to_foul_ratio"]) * 0.25
            + pctl(df["progressive_pass_share"]) * 0.20
        )

        df["rest_defence"] = (
            pctl(df["interception"]) * 0.30
            + pctl(df["interception_share"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.20
        )

        df["wide_coverage"] = (
            pctl(df["total_tackle"]) * 0.30
            + pctl(df["effective_clearance"]) * 0.25
            + pctl(df["outfielder_block"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.20
        )

        df["counter_press"] = (
            pctl(df["poss_won_att_3rd"]) * 0.35
            + pctl(df["total_tackle"]) * 0.25
            + pctl(df["interception"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.15
        )
