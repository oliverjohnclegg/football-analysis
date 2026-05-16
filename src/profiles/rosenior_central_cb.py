from src.profiles.base import PositionalProfile, ScatterChart, pctl


class RoseniorCentralCBProfile(PositionalProfile):
    name = "Rosenior Central CB – Line-Breaking Distributor"
    slug = "rosenior/central_cb"
    position_keywords = ["Defender"]

    dimension_weights = {
        "line_breaking": 0.30,
        "high_line_defence": 0.25,
        "ball_carrying": 0.25,
        "pressing_aggression": 0.20,
    }

    radar_labels = [
        "Line\nBreaking",
        "High-Line\nDefence",
        "Ball\nCarrying",
        "Pressing\nAggression",
    ]

    ranking_title = "Top 25 – Rosenior System Central CB Profile Fit"
    radar_title = "Top 5 Central CB Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "line_breaking", "high_line_defence",
            "Line-Breaking Score", "High-Line Defence Score",
            "Progression vs High-Line Defending",
            "progression_vs_highline.png",
        ),
        ScatterChart(
            "ball_carrying", "pressing_aggression",
            "Ball Carrying Score", "Pressing Aggression Score",
            "Carrying vs Pressing Out",
            "carrying_vs_pressing.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["line_breaking"] = (
            pctl(df["accurate_long_balls"]) * 0.30
            + pctl(df["progressive_pass_share"]) * 0.25
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["carry_to_foul_ratio"]) * 0.20
        )

        df["high_line_defence"] = (
            pctl(df["interception"]) * 0.30
            + pctl(df["effective_clearance"]) * 0.30
            + pctl(df["interception_share"]) * 0.20
            + pctl(df["fouls"], ascending=False) * 0.20
        )

        df["ball_carrying"] = (
            pctl(df["won_contest"]) * 0.40
            + pctl(df["carry_to_foul_ratio"]) * 0.35
            + pctl(df["fouls"], ascending=False) * 0.25
        )

        df["pressing_aggression"] = (
            pctl(df["poss_won_att_3rd"]) * 0.30
            + pctl(df["total_tackle"]) * 0.30
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["outfielder_block"]) * 0.15
        )
