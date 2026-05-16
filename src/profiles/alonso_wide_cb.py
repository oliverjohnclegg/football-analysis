from src.profiles.base import PositionalProfile, ScatterChart, pctl


class AlonsoWideCBProfile(PositionalProfile):
    name = "Alonso Wide CB – Hybrid Cover Defender"
    slug = "alonso/wide_cb"
    position_keywords = ["Defender"]

    dimension_weights = {
        "ball_playing": 0.30,
        "ball_carrying": 0.25,
        "wide_defending": 0.25,
        "proactive_defending": 0.20,
    }

    radar_labels = [
        "Ball\nPlaying",
        "Ball\nCarrying",
        "Wide\nDefending",
        "Proactive\nDefending",
    ]

    ranking_title = "Top 25 – Alonso System Wide CB Profile Fit"
    radar_title = "Top 5 Wide CB Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "ball_playing", "wide_defending",
            "Ball-Playing Score", "Wide Defending Score",
            "Distribution vs Wide Defending",
            "distribution_vs_defending.png",
        ),
        ScatterChart(
            "ball_carrying", "proactive_defending",
            "Ball Carrying Score", "Proactive Defending Score",
            "Carrying vs Pressing Aggression",
            "carrying_vs_aggression.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["ball_playing"] = (
            pctl(df["accurate_long_balls"]) * 0.30
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["progressive_pass_share"]) * 0.25
            + pctl(df["total_att_assist"]) * 0.20
        )

        df["ball_carrying"] = (
            pctl(df["won_contest"]) * 0.40
            + pctl(df["carry_to_foul_ratio"]) * 0.35
            + pctl(df["fouls"], ascending=False) * 0.25
        )

        df["wide_defending"] = (
            pctl(df["total_tackle"]) * 0.30
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["effective_clearance"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.20
        )

        df["proactive_defending"] = (
            pctl(df["interception"]) * 0.30
            + pctl(df["interception_share"]) * 0.30
            + pctl(df["poss_won_att_3rd"]) * 0.20
            + pctl(df["outfielder_block"]) * 0.20
        )
