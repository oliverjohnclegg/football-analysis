from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class RoseniorCentreForwardProfile(PositionalProfile):
    name = "Rosenior #9 – Mobile Pressing Forward"
    slug = "rosenior/centre_forward"
    position_keywords = ["Attack"]

    dimension_weights = {
        "finishing": 0.30,
        "link_play": 0.25,
        "box_presence": 0.25,
        "press_leadership": 0.20,
    }

    radar_labels = [
        "Finishing",
        "Link\nPlay",
        "Box\nPresence",
        "Press\nLeadership",
    ]

    ranking_title = "Top 25 – Rosenior System Centre Forward Profile Fit"
    radar_title = "Top 5 Centre Forward Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "finishing", "link_play",
            "Finishing Score", "Link Play Score",
            "Finishing vs Link-Up",
            "finishing_vs_linkup.png",
        ),
        ScatterChart(
            "box_presence", "press_leadership",
            "Box Presence Score", "Press Leadership Score",
            "Box Presence vs Pressing Leadership",
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

        df["link_play"] = (
            pctl(df["total_att_assist"]) * 0.25
            + pctl(df["expected_assists_per_90"]) * 0.25
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["won_contest"]) * 0.25
        )

        df["box_presence"] = (
            pctl(df["total_scoring_att"]) * 0.30
            + pctl(df["ontarget_scoring_att"]) * 0.30
            + pctl(df["xg_per_shot"]) * 0.40
        )

        df["press_leadership"] = (
            pctl(df["poss_won_att_3rd"]) * 0.40
            + pctl(df["total_tackle"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.20
            + pctl(df["interception"]) * 0.15
        )
