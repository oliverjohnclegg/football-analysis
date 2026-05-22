from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class TuchelHalfSpaceTenProfile(PositionalProfile):
    name = "Tuchel #10 – Half-Space Connector"
    slug = "tuchel/half_space_10"
    position_keywords = ["Mid", "Attack"]

    dimension_weights = {
        "half_space_creation": 0.30,
        "goal_threat": 0.25,
        "carry_between_lines": 0.25,
        "pressing_trap": 0.20,
    }

    radar_labels = [
        "Half-Space\nCreation",
        "Goal\nThreat",
        "Carry Between\nLines",
        "Pressing\nTrap",
    ]

    ranking_title = "Top 25 – Tuchel System Half-Space #10 Profile Fit"
    radar_title = "Top 5 Half-Space #10 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "half_space_creation", "goal_threat",
            "Half-Space Creation Score", "Goal Threat Score",
            "Creating vs Scoring",
            "creation_vs_scoring.png",
        ),
        ScatterChart(
            "carry_between_lines", "pressing_trap",
            "Carry Between Lines Score", "Pressing Trap Score",
            "Technique vs Pressing",
            "carry_vs_pressing.png",
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

    def _compute_dimensions(self, df, nineties):
        df["half_space_creation"] = (
            pctl(df["expected_assists_per_90"]) * 0.35
            + pctl(df["chance_quality"]) * 0.35
            + pctl(df["big_chance_created"]) * 0.30
        )

        df["goal_threat"] = (
            pctl(df["expected_goals_per_90"]) * 0.35
            + pctl(df["xg_per_shot"]) * 0.35
            + pctl(df["shot_accuracy"]) * 0.30
        )

        df["carry_between_lines"] = (
            pctl(df["won_contest"]) * 0.35
            + pctl(df["carry_to_foul_ratio"]) * 0.35
            + pctl(df["accurate_pass"]) * 0.30
        )

        df["pressing_trap"] = (
            pctl(df["poss_won_att_3rd"]) * 0.40
            + pctl(df["total_tackle"]) * 0.30
            + pctl(df["clean_defend_rate"]) * 0.30
        )
