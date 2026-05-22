from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class TuchelCentreForwardProfile(PositionalProfile):
    name = "Tuchel #9 – Pinning Striker"
    slug = "tuchel/centre_forward"
    position_keywords = ["Attack"]

    dimension_weights = {
        "central_finishing": 0.40,
        "box_presence": 0.40,
        "link_play": 0.10,
        "first_line_press": 0.10,
    }

    radar_labels = [
        "Central\nFinishing",
        "Box\nPresence",
        "Link\nPlay",
        "First-Line\nPress",
    ]

    ranking_title = "Top 25 – Tuchel System Centre Forward Profile Fit"
    radar_title = "Top 5 Centre Forward Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "central_finishing", "link_play",
            "Central Finishing Score", "Link Play Score",
            "Finishing vs Link-Up",
            "finishing_vs_link.png",
        ),
        ScatterChart(
            "box_presence", "first_line_press",
            "Box Presence Score", "First-Line Press Score",
            "Box Occupation vs Pressing",
            "box_vs_press.png",
        ),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        shots = df.get("total_scoring_att", 0)
        shots_ot = df.get("ontarget_scoring_att", 0)
        xg90 = df.get("expected_goals_per_90", 0)
        dribbles = df.get("won_contest", 0)
        df["shot_accuracy"] = safe_ratio(shots_ot, shots)
        df["xg_per_shot"] = safe_ratio(xg90, shots)
        df["shooting_focus"] = safe_ratio(shots, dribbles.clip(lower=0.1))

    def _compute_dimensions(self, df, nineties):
        df["central_finishing"] = (
            pctl(df["expected_goals_per_90"]) * 0.30
            + pctl(df["goals_per_90"]) * 0.30
            + pctl(df["xg_per_shot"]) * 0.25
            + pctl(df["shot_accuracy"]) * 0.15
        )

        df["box_presence"] = (
            pctl(df["total_scoring_att"]) * 0.30
            + pctl(df["ontarget_scoring_att"]) * 0.25
            + pctl(df["shooting_focus"]) * 0.25
            + pctl(df["xg_per_shot"]) * 0.20
        )

        df["link_play"] = (
            pctl(df["total_att_assist"]) * 0.45
            + pctl(df["accurate_pass"]) * 0.35
            + pctl(df["expected_assists_per_90"]) * 0.20
        )

        df["first_line_press"] = (
            pctl(df["poss_won_att_3rd"]) * 0.45
            + pctl(df["total_tackle"]) * 0.30
            + pctl(df["fouls"], ascending=False) * 0.25
        )
