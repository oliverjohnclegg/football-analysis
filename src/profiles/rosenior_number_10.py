from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class RoseniorNumberTenProfile(PositionalProfile):
    name = "Rosenior #10 – Between-Lines Playmaker"
    slug = "rosenior/number_10"
    position_keywords = ["Mid", "Attack"]

    dimension_weights = {
        "creative_output": 0.30,
        "goal_threat": 0.25,
        "between_lines_craft": 0.25,
        "pressing_contribution": 0.20,
    }

    radar_labels = [
        "Creative\nOutput",
        "Goal\nThreat",
        "Between-Lines\nCraft",
        "Pressing\nContribution",
    ]

    ranking_title = "Top 25 – Rosenior System #10 Profile Fit"
    radar_title = "Top 5 #10 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "creative_output", "goal_threat",
            "Creative Output Score", "Goal Threat Score",
            "The Dual Threat: Creating vs Scoring",
            "creating_vs_scoring.png",
        ),
        ScatterChart(
            "between_lines_craft", "pressing_contribution",
            "Between-Lines Craft Score", "Pressing Contribution Score",
            "Craft vs Work Rate",
            "craft_vs_workrate.png",
        ),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        chances = df.get("total_att_assist", 0)
        xa = df.get("expected_assists", 0)
        df["chance_quality"] = safe_ratio(xa, chances)

        shots = df.get("total_scoring_att", 0)
        shots_ot = df.get("ontarget_scoring_att", 0)
        df["shot_accuracy"] = safe_ratio(shots_ot, shots)

        xg90 = df.get("expected_goals_per_90", 0)
        df["xg_per_shot"] = safe_ratio(xg90, shots)

        xa90 = df.get("expected_assists_per_90", 0)
        df["goal_involvement_balance"] = safe_ratio(
            xa90.clip(lower=0.001) * xg90.clip(lower=0.001),
            (xa90 + xg90).clip(lower=0.001),
        )

    def _compute_dimensions(self, df, nineties):
        df["creative_output"] = (
            pctl(df["expected_assists_per_90"]) * 0.30
            + pctl(df["chance_quality"]) * 0.30
            + pctl(df["big_chance_created"]) * 0.20
            + pctl(df["total_att_assist"]) * 0.20
        )

        df["goal_threat"] = (
            pctl(df["expected_goals_per_90"]) * 0.30
            + pctl(df["xg_per_shot"]) * 0.25
            + pctl(df["goals_per_90"]) * 0.25
            + pctl(df["shot_accuracy"]) * 0.20
        )

        df["between_lines_craft"] = (
            pctl(df["won_contest"]) * 0.25
            + pctl(df["carry_to_foul_ratio"]) * 0.25
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["goal_involvement_balance"]) * 0.25
        )

        df["pressing_contribution"] = (
            pctl(df["poss_won_att_3rd"]) * 0.35
            + pctl(df["total_tackle"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["interception_share"]) * 0.15
        )
