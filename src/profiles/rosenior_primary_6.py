from src.profiles.base import PositionalProfile, ScatterChart, pctl


class RoseniorPrimarySixProfile(PositionalProfile):
    name = "Rosenior #6 – Defensive Pivot Anchor"
    slug = "rosenior/primary_6"
    position_keywords = ["Mid"]

    dimension_weights = {
        "defensive_shield": 0.30,
        "tempo_control": 0.25,
        "counter_press_anchor": 0.25,
        "press_resistance": 0.20,
    }

    radar_labels = [
        "Defensive\nShield",
        "Tempo\nControl",
        "Counter-Press\nAnchor",
        "Press\nResistance",
    ]

    ranking_title = "Top 25 – Rosenior System Primary #6 Profile Fit"
    radar_title = "Top 5 Primary #6 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "defensive_shield", "tempo_control",
            "Defensive Shield Score", "Tempo Control Score",
            "Shielding vs Distributing",
            "shield_vs_tempo.png",
        ),
        ScatterChart(
            "counter_press_anchor", "press_resistance",
            "Counter-Press Anchor Score", "Press Resistance Score",
            "Recovery vs Composure",
            "recovery_vs_composure.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["defensive_shield"] = (
            pctl(df["interception"]) * 0.30
            + pctl(df["interception_share"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.20
        )

        df["tempo_control"] = (
            pctl(df["accurate_pass"]) * 0.40
            + pctl(df["accurate_long_balls"]) * 0.30
            + pctl(df["progressive_pass_share"]) * 0.30
        )

        df["counter_press_anchor"] = (
            pctl(df["total_tackle"]) * 0.30
            + pctl(df["poss_won_att_3rd"]) * 0.25
            + pctl(df["interception"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.20
        )

        df["press_resistance"] = (
            pctl(df["accurate_pass"]) * 0.25
            + pctl(df["won_contest"]) * 0.25
            + pctl(df["carry_to_foul_ratio"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.25
        )
