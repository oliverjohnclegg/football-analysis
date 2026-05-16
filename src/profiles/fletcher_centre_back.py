from src.profiles.base import PositionalProfile, ScatterChart, pctl


class FletcherCentreBackProfile(PositionalProfile):
    name = "Fletcher CB – Ball-Progressing Defender"
    slug = "fletcher/centre_back"
    position_keywords = ["Defender"]

    dimension_weights = {
        "ball_progression": 0.30,
        "switch_play": 0.25,
        "recovery_defending": 0.25,
        "aerial_command": 0.20,
    }

    radar_labels = [
        "Ball\nProgression",
        "Switch\nPlay",
        "Recovery\nDefending",
        "Aerial\nCommand",
    ]

    ranking_title = "Top 25 – Fletcher System CB Profile Fit"
    radar_title = "Top 5 CB Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "ball_progression", "recovery_defending",
            "Ball Progression Score", "Recovery Defending Score",
            "Progressor Duality: Building vs Defending",
            "progression_vs_defending.png",
        ),
        ScatterChart(
            "switch_play", "aerial_command",
            "Switch Play Score", "Aerial Command Score",
            "Distribution Range vs Physical Command",
            "distribution_vs_command.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["ball_progression"] = (
            pctl(df["won_contest"]) * 0.25
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["progressive_pass_share"]) * 0.25
            + pctl(df["carry_to_foul_ratio"]) * 0.25
        )

        df["switch_play"] = (
            pctl(df["accurate_long_balls"]) * 0.45
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["progressive_pass_share"]) * 0.30
        )

        df["recovery_defending"] = (
            pctl(df["total_tackle"]) * 0.30
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["interception"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.20
        )

        df["aerial_command"] = (
            pctl(df["effective_clearance"]) * 0.40
            + pctl(df["outfielder_block"]) * 0.30
            + pctl(df["interception"]) * 0.30
        )
