from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class FletcherTargetNineProfile(PositionalProfile):
    name = "Fletcher Target 9 – Physical Reference Point"
    slug = "fletcher/target_9"
    position_keywords = ["Attack"]

    dimension_weights = {
        "finishing": 0.30,
        "box_occupation": 0.25,
        "hold_up_play": 0.25,
        "press_leadership": 0.20,
    }

    radar_labels = [
        "Finishing",
        "Box\nOccupation",
        "Hold-Up\nPlay",
        "Press\nLeadership",
    ]

    ranking_title = "Top 25 – Fletcher System Target 9 Profile Fit"
    radar_title = "Top 5 Target 9 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "finishing", "hold_up_play",
            "Finishing Score", "Hold-Up Play Score",
            "Clinical vs Link-Up",
            "finishing_vs_holdup.png",
        ),
        ScatterChart(
            "box_occupation", "press_leadership",
            "Box Occupation Score", "Press Leadership Score",
            "Box Presence vs Pressing from the Front",
            "box_vs_pressing.png",
        ),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        shots = df.get("total_scoring_att", 0)
        shots_ot = df.get("ontarget_scoring_att", 0)
        xg90 = df.get("expected_goals_per_90", 0)
        df["shot_accuracy"] = safe_ratio(shots_ot, shots)
        df["xg_per_shot"] = safe_ratio(xg90, shots)

    def _compute_dimensions(self, df, nineties):
        df["finishing"] = (
            pctl(df["expected_goals_per_90"]) * 0.30
            + pctl(df["xg_per_shot"]) * 0.25
            + pctl(df["goals_per_90"]) * 0.25
            + pctl(df["shot_accuracy"]) * 0.20
        )

        df["box_occupation"] = (
            pctl(df["total_scoring_att"]) * 0.30
            + pctl(df["ontarget_scoring_att"]) * 0.30
            + pctl(df["xg_per_shot"]) * 0.40
        )

        df["hold_up_play"] = (
            pctl(df["total_att_assist"]) * 0.25
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["won_contest"]) * 0.25
            + pctl(df["carry_to_foul_ratio"]) * 0.25
        )

        df["press_leadership"] = (
            pctl(df["poss_won_att_3rd"]) * 0.40
            + pctl(df["total_tackle"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.20
            + pctl(df["interception"]) * 0.15
        )
