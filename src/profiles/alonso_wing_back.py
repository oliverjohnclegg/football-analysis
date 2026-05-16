from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class AlonsoWingBackProfile(PositionalProfile):
    name = "Alonso WB – Attacking Width Provider"
    slug = "alonso/wing_back"
    position_keywords = ["Defender", "Mid"]

    dimension_weights = {
        "attacking_output": 0.30,
        "chance_creation": 0.25,
        "wide_progression": 0.25,
        "defensive_recovery": 0.20,
    }

    radar_labels = [
        "Attacking\nOutput",
        "Chance\nCreation",
        "Wide\nProgression",
        "Defensive\nRecovery",
    ]

    ranking_title = "Top 25 – Alonso System Wing-Back Profile Fit"
    radar_title = "Top 5 Wing-Back Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "attacking_output", "defensive_recovery",
            "Attacking Output Score", "Defensive Recovery Score",
            "The Two-Way Wing-Back: Attack vs Defence",
            "attack_vs_defence.png",
        ),
        ScatterChart(
            "wide_progression", "chance_creation",
            "Wide Progression Score", "Chance Creation Score",
            "Carrying vs Creating",
            "carrying_vs_creating.png",
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
        df["attacking_output"] = (
            pctl(df["expected_goals_per_90"]) * 0.25
            + pctl(df["expected_assists_per_90"]) * 0.25
            + pctl(df["goal_involvement_balance"]) * 0.25
            + pctl(df["total_att_assist"]) * 0.25
        )

        df["chance_creation"] = (
            pctl(df["expected_assists_per_90"]) * 0.30
            + pctl(df["chance_quality"]) * 0.30
            + pctl(df["big_chance_created"]) * 0.20
            + pctl(df["total_att_assist"]) * 0.20
        )

        df["wide_progression"] = (
            pctl(df["won_contest"]) * 0.35
            + pctl(df["carry_to_foul_ratio"]) * 0.30
            + pctl(df["accurate_long_balls"]) * 0.20
            + pctl(df["progressive_pass_share"]) * 0.15
        )

        df["defensive_recovery"] = (
            pctl(df["total_tackle"]) * 0.30
            + pctl(df["interception"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["poss_won_att_3rd"]) * 0.20
        )
