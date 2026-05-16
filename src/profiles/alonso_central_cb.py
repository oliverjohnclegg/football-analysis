from src.profiles.base import PositionalProfile, ScatterChart, pctl


class AlonsoCentralCBProfile(PositionalProfile):
    name = "Alonso Central CB – Modern Libero"
    slug = "alonso/central_cb"
    position_keywords = ["Defender"]

    dimension_weights = {
        "line_breaking": 0.30,
        "rest_defence": 0.25,
        "switch_play": 0.25,
        "aerial_command": 0.20,
    }

    radar_labels = [
        "Line\nBreaking",
        "Rest\nDefence",
        "Switch\nPlay",
        "Aerial\nCommand",
    ]

    ranking_title = "Top 25 – Alonso System Central CB Profile Fit"
    radar_title = "Top 5 Central CB Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "line_breaking", "rest_defence",
            "Line-Breaking Score", "Rest Defence Score",
            "Libero Duality: Progression vs Defence",
            "progression_vs_defence.png",
        ),
        ScatterChart(
            "switch_play", "aerial_command",
            "Switch Play Score", "Aerial Command Score",
            "Distribution Range vs Physical Command",
            "distribution_vs_command.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["line_breaking"] = (
            pctl(df["won_contest"]) * 0.30
            + pctl(df["accurate_long_balls"]) * 0.25
            + pctl(df["progressive_pass_share"]) * 0.25
            + pctl(df["carry_to_foul_ratio"]) * 0.20
        )

        df["rest_defence"] = (
            pctl(df["interception"]) * 0.30
            + pctl(df["interception_share"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.20
        )

        df["switch_play"] = (
            pctl(df["accurate_long_balls"]) * 0.40
            + pctl(df["accurate_pass"]) * 0.30
            + pctl(df["progressive_pass_share"]) * 0.30
        )

        df["aerial_command"] = (
            pctl(df["effective_clearance"]) * 0.35
            + pctl(df["outfielder_block"]) * 0.30
            + pctl(df["interception"]) * 0.35
        )
