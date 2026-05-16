from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class AlonsoSecondarySixEightProfile(PositionalProfile):
    name = "Alonso #6/8 – Shuttle Connector"
    slug = "alonso/secondary_6_8"
    position_keywords = ["Mid"]

    dimension_weights = {
        "ball_progression": 0.30,
        "counter_press_intensity": 0.25,
        "third_man_link": 0.25,
        "box_arrival": 0.20,
    }

    radar_labels = [
        "Ball\nProgression",
        "Counter-Press\nIntensity",
        "Third-Man\nLink",
        "Box\nArrival",
    ]

    ranking_title = "Top 25 – Alonso System Secondary #6/8 Profile Fit"
    radar_title = "Top 5 Secondary #6/8 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "ball_progression", "counter_press_intensity",
            "Ball Progression Score", "Counter-Press Intensity Score",
            "Driving Forward vs Winning It Back",
            "progression_vs_counterpress.png",
        ),
        ScatterChart(
            "third_man_link", "box_arrival",
            "Third-Man Link Score", "Box Arrival Score",
            "Link Play vs Late Runs",
            "link_vs_arrival.png",
        ),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        passes = df.get("accurate_pass", 0)
        chances = df.get("total_att_assist", 0)
        df["chance_creation_rate"] = safe_ratio(chances, passes)

        shots = df.get("total_scoring_att", 0)
        xg90 = df.get("expected_goals_per_90", 0)
        df["xg_per_shot"] = safe_ratio(xg90, shots)

    def _compute_dimensions(self, df, nineties):
        df["ball_progression"] = (
            pctl(df["won_contest"]) * 0.30
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["carry_to_foul_ratio"]) * 0.25
            + pctl(df["progressive_pass_share"]) * 0.20
        )

        df["counter_press_intensity"] = (
            pctl(df["poss_won_att_3rd"]) * 0.30
            + pctl(df["total_tackle"]) * 0.25
            + pctl(df["interception"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.20
        )

        df["third_man_link"] = (
            pctl(df["expected_assists_per_90"]) * 0.30
            + pctl(df["chance_creation_rate"]) * 0.30
            + pctl(df["total_att_assist"]) * 0.20
            + pctl(df["accurate_pass"]) * 0.20
        )

        df["box_arrival"] = (
            pctl(df["expected_goals_per_90"]) * 0.35
            + pctl(df["xg_per_shot"]) * 0.30
            + pctl(df["goals_per_90"]) * 0.20
            + pctl(df["ontarget_scoring_att"]) * 0.15
        )
