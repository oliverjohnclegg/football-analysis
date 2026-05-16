from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class FletcherFullBackProfile(PositionalProfile):
    name = "Fletcher FB – Inverting-Overlapping Hybrid"
    slug = "fletcher/full_back"
    position_keywords = ["Defender", "Mid"]

    dimension_weights = {
        "creative_output": 0.30,
        "ball_progression": 0.25,
        "wide_threat": 0.25,
        "defensive_solidity": 0.20,
    }

    radar_labels = [
        "Creative\nOutput",
        "Ball\nProgression",
        "Wide\nThreat",
        "Defensive\nSolidity",
    ]

    ranking_title = "Top 25 – Fletcher System Full-Back Profile Fit"
    radar_title = "Top 5 Full-Back Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "creative_output", "defensive_solidity",
            "Creative Output Score", "Defensive Solidity Score",
            "The Dual-Role Full-Back: Creating vs Defending",
            "creating_vs_defending.png",
        ),
        ScatterChart(
            "ball_progression", "wide_threat",
            "Ball Progression Score", "Wide Threat Score",
            "Inverting vs Overlapping",
            "inverting_vs_overlapping.png",
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
        df["creative_output"] = (
            pctl(df["expected_assists_per_90"]) * 0.30
            + pctl(df["chance_quality"]) * 0.30
            + pctl(df["big_chance_created"]) * 0.20
            + pctl(df["total_att_assist"]) * 0.20
        )

        df["ball_progression"] = (
            pctl(df["won_contest"]) * 0.30
            + pctl(df["carry_to_foul_ratio"]) * 0.25
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["progressive_pass_share"]) * 0.20
        )

        df["wide_threat"] = (
            pctl(df["expected_goals_per_90"]) * 0.25
            + pctl(df["expected_assists_per_90"]) * 0.25
            + pctl(df["goal_involvement_balance"]) * 0.25
            + pctl(df["total_att_assist"]) * 0.25
        )

        df["defensive_solidity"] = (
            pctl(df["total_tackle"]) * 0.30
            + pctl(df["interception"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["poss_won_att_3rd"]) * 0.20
        )
