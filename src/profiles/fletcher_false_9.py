from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class FletcherFalseNineProfile(PositionalProfile):
    name = "Fletcher False 9 – Dropping Link-Up Striker"
    slug = "fletcher/false_9"
    position_keywords = ["Attack"]

    dimension_weights = {
        "link_play": 0.30,
        "creative_output": 0.25,
        "finishing": 0.25,
        "press_trigger": 0.20,
    }

    radar_labels = [
        "Link\nPlay",
        "Creative\nOutput",
        "Finishing",
        "Press\nTrigger",
    ]

    ranking_title = "Top 25 – Fletcher System False 9 Profile Fit"
    radar_title = "Top 5 False 9 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "link_play", "finishing",
            "Link Play Score", "Finishing Score",
            "Dropping Deep vs Staying Clinical",
            "link_vs_finishing.png",
        ),
        ScatterChart(
            "creative_output", "press_trigger",
            "Creative Output Score", "Press Trigger Score",
            "Creating vs Leading the Press",
            "creating_vs_pressing.png",
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
        df["link_play"] = (
            pctl(df["total_att_assist"]) * 0.25
            + pctl(df["expected_assists_per_90"]) * 0.25
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["won_contest"]) * 0.25
        )

        df["creative_output"] = (
            pctl(df["expected_assists_per_90"]) * 0.30
            + pctl(df["chance_quality"]) * 0.30
            + pctl(df["big_chance_created"]) * 0.20
            + pctl(df["total_att_assist"]) * 0.20
        )

        df["finishing"] = (
            pctl(df["expected_goals_per_90"]) * 0.30
            + pctl(df["xg_per_shot"]) * 0.25
            + pctl(df["goals_per_90"]) * 0.25
            + pctl(df["shot_accuracy"]) * 0.20
        )

        df["press_trigger"] = (
            pctl(df["poss_won_att_3rd"]) * 0.40
            + pctl(df["total_tackle"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.20
            + pctl(df["interception"]) * 0.15
        )
