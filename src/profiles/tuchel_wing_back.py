from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class TuchelWingBackProfile(PositionalProfile):
    name = "Tuchel WB – High Wide Forward"
    slug = "tuchel/wing_back"
    position_keywords = ["Defender", "Mid"]

    dimension_weights = {
        "wide_threat": 0.30,
        "box_delivery": 0.25,
        "penetration": 0.25,
        "transition_defence": 0.20,
    }

    radar_labels = [
        "Wide\nThreat",
        "Box\nDelivery",
        "Penetration",
        "Transition\nDefence",
    ]

    ranking_title = "Top 25 – Tuchel System Wing-Back Profile Fit"
    radar_title = "Top 5 Wing-Back Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "wide_threat", "transition_defence",
            "Wide Threat Score", "Transition Defence Score",
            "Attack vs Recovery",
            "threat_vs_recovery.png",
        ),
        ScatterChart(
            "penetration", "box_delivery",
            "Penetration Score", "Box Delivery Score",
            "Carrying vs Final Delivery",
            "penetration_vs_delivery.png",
        ),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        xa90 = df.get("expected_assists_per_90", 0)
        xg90 = df.get("expected_goals_per_90", 0)
        df["goal_involvement_balance"] = safe_ratio(
            xa90.clip(lower=0.001) * xg90.clip(lower=0.001),
            (xa90 + xg90).clip(lower=0.001),
        )
        chances = df.get("total_att_assist", 0)
        xa = df.get("expected_assists", 0)
        df["chance_quality"] = safe_ratio(xa, chances)

    def _compute_dimensions(self, df, nineties):
        df["wide_threat"] = (
            pctl(df["expected_goals_per_90"]) * 0.35
            + pctl(df["expected_assists_per_90"]) * 0.35
            + pctl(df["goal_involvement_balance"]) * 0.30
        )

        df["box_delivery"] = (
            pctl(df["expected_assists_per_90"]) * 0.30
            + pctl(df["chance_quality"]) * 0.35
            + pctl(df["big_chance_created"]) * 0.35
        )

        df["penetration"] = (
            pctl(df["won_contest"]) * 0.40
            + pctl(df["carry_to_foul_ratio"]) * 0.35
            + pctl(df["progressive_pass_share"]) * 0.25
        )

        df["transition_defence"] = (
            pctl(df["poss_won_att_3rd"]) * 0.35
            + pctl(df["total_tackle"]) * 0.35
            + pctl(df["clean_defend_rate"]) * 0.30
        )
