from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class FletcherWingerProfile(PositionalProfile):
    name = "Fletcher Winger – Direct 1v1 Isolator"
    slug = "fletcher/winger"
    position_keywords = ["Attack", "Mid"]

    dimension_weights = {
        "dribbling_isolation": 0.30,
        "goal_output": 0.25,
        "chance_creation": 0.25,
        "transition_pressing": 0.20,
    }

    radar_labels = [
        "Dribbling\nIsolation",
        "Goal\nOutput",
        "Chance\nCreation",
        "Transition\nPressing",
    ]

    ranking_title = "Top 25 – Fletcher System Winger Profile Fit"
    radar_title = "Top 5 Winger Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "dribbling_isolation", "chance_creation",
            "Dribbling Isolation Score", "Chance Creation Score",
            "1v1 Threat vs Creative Output",
            "dribbling_vs_creation.png",
        ),
        ScatterChart(
            "goal_output", "transition_pressing",
            "Goal Output Score", "Transition Pressing Score",
            "Scoring vs Counter-Press Contribution",
            "scoring_vs_pressing.png",
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
        df["dribbling_isolation"] = (
            pctl(df["won_contest"]) * 0.40
            + pctl(df["carry_to_foul_ratio"]) * 0.30
            + pctl(df["fouls"], ascending=False) * 0.15
            + pctl(df["expected_goals_per_90"]) * 0.15
        )

        df["goal_output"] = (
            pctl(df["expected_goals_per_90"]) * 0.30
            + pctl(df["xg_per_shot"]) * 0.25
            + pctl(df["goals_per_90"]) * 0.25
            + pctl(df["shot_accuracy"]) * 0.20
        )

        df["chance_creation"] = (
            pctl(df["expected_assists_per_90"]) * 0.30
            + pctl(df["chance_quality"]) * 0.30
            + pctl(df["big_chance_created"]) * 0.20
            + pctl(df["total_att_assist"]) * 0.20
        )

        df["transition_pressing"] = (
            pctl(df["poss_won_att_3rd"]) * 0.35
            + pctl(df["total_tackle"]) * 0.25
            + pctl(df["interception"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.15
        )
