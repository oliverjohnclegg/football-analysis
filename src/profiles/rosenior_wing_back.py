from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class RoseniorWingBackProfile(PositionalProfile):
    name = "Rosenior FB – Overlapping Width Provider"
    slug = "rosenior/wing_back"
    position_keywords = ["Defender", "Mid"]

    dimension_weights = {
        "wide_progression": 0.30,
        "chance_creation": 0.25,
        "pressing_intensity": 0.25,
        "defensive_solidity": 0.20,
    }

    radar_labels = [
        "Wide\nProgression",
        "Chance\nCreation",
        "Pressing\nIntensity",
        "Defensive\nSolidity",
    ]

    ranking_title = "Top 25 – Rosenior System Full-Back Profile Fit"
    radar_title = "Top 5 Full-Back Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "wide_progression", "defensive_solidity",
            "Wide Progression Score", "Defensive Solidity Score",
            "The Two-Way Full-Back: Attack vs Defence",
            "attack_vs_defence.png",
        ),
        ScatterChart(
            "chance_creation", "pressing_intensity",
            "Chance Creation Score", "Pressing Intensity Score",
            "Creating vs Pressing",
            "creating_vs_pressing.png",
        ),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        chances = df.get("total_att_assist", 0)
        xa = df.get("expected_assists", 0)
        df["chance_quality"] = safe_ratio(xa, chances)

    def _compute_dimensions(self, df, nineties):
        df["wide_progression"] = (
            pctl(df["won_contest"]) * 0.30
            + pctl(df["carry_to_foul_ratio"]) * 0.25
            + pctl(df["accurate_long_balls"]) * 0.25
            + pctl(df["progressive_pass_share"]) * 0.20
        )

        df["chance_creation"] = (
            pctl(df["expected_assists_per_90"]) * 0.30
            + pctl(df["chance_quality"]) * 0.30
            + pctl(df["total_att_assist"]) * 0.20
            + pctl(df["big_chance_created"]) * 0.20
        )

        df["pressing_intensity"] = (
            pctl(df["poss_won_att_3rd"]) * 0.30
            + pctl(df["total_tackle"]) * 0.30
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["interception"]) * 0.15
        )

        df["defensive_solidity"] = (
            pctl(df["total_tackle"]) * 0.25
            + pctl(df["interception"]) * 0.25
            + pctl(df["effective_clearance"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.25
        )
