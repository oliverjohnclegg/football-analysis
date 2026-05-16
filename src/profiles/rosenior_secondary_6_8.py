from src.profiles.base import PositionalProfile, ScatterChart, pctl


class RoseniorSecondarySixEightProfile(PositionalProfile):
    name = "Rosenior #6/8 – Progressive Connector"
    slug = "rosenior/secondary_6_8"
    position_keywords = ["Mid"]

    dimension_weights = {
        "ball_progression": 0.30,
        "distribution_range": 0.25,
        "counter_press_intensity": 0.25,
        "rest_defence_cover": 0.20,
    }

    radar_labels = [
        "Ball\nProgression",
        "Distribution\nRange",
        "Counter-Press\nIntensity",
        "Rest-Defence\nCover",
    ]

    ranking_title = "Top 25 – Rosenior System Secondary #6/8 Profile Fit"
    radar_title = "Top 5 Secondary #6/8 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "ball_progression", "counter_press_intensity",
            "Ball Progression Score", "Counter-Press Intensity Score",
            "Driving Forward vs Winning It Back",
            "progression_vs_counterpress.png",
        ),
        ScatterChart(
            "distribution_range", "rest_defence_cover",
            "Distribution Range Score", "Rest-Defence Cover Score",
            "Range vs Rest-Defence Contribution",
            "range_vs_restdefence.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["ball_progression"] = (
            pctl(df["won_contest"]) * 0.30
            + pctl(df["carry_to_foul_ratio"]) * 0.25
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["progressive_pass_share"]) * 0.20
        )

        df["distribution_range"] = (
            pctl(df["accurate_long_balls"]) * 0.35
            + pctl(df["progressive_pass_share"]) * 0.30
            + pctl(df["total_att_assist"]) * 0.20
            + pctl(df["accurate_pass"]) * 0.15
        )

        df["counter_press_intensity"] = (
            pctl(df["poss_won_att_3rd"]) * 0.30
            + pctl(df["total_tackle"]) * 0.25
            + pctl(df["interception"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.20
        )

        df["rest_defence_cover"] = (
            pctl(df["interception"]) * 0.30
            + pctl(df["interception_share"]) * 0.30
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.15
        )
