from src.profiles.base import PositionalProfile, ScatterChart, pctl


class FletcherNumberSixProfile(PositionalProfile):
    name = "Fletcher #6 – Deep-Lying Playmaker"
    slug = "fletcher/number_6"
    position_keywords = ["Mid"]

    dimension_weights = {
        "tempo_control": 0.25,
        "switch_play": 0.25,
        "press_resistance": 0.20,
        "defensive_shield": 0.15,
        "counter_press": 0.15,
    }

    radar_labels = [
        "Tempo\nControl",
        "Switch\nPlay",
        "Press\nResistance",
        "Defensive\nShield",
        "Counter-\nPress",
    ]

    ranking_title = "Top 25 – Fletcher System #6 Profile Fit"
    radar_title = "Top 5 #6 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "tempo_control", "defensive_shield",
            "Tempo Control Score", "Defensive Shield Score",
            "Scholes Duality: Tempo vs Shield",
            "tempo_vs_shield.png",
        ),
        ScatterChart(
            "switch_play", "press_resistance",
            "Switch Play Score", "Press Resistance Score",
            "Range vs Composure Under Pressure",
            "range_vs_composure.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["tempo_control"] = (
            pctl(df["accurate_pass"]) * 0.40
            + pctl(df["progressive_pass_share"]) * 0.30
            + pctl(df["accurate_long_balls"]) * 0.30
        )

        df["switch_play"] = (
            pctl(df["accurate_long_balls"]) * 0.55
            + pctl(df["progressive_pass_share"]) * 0.45
        )

        df["press_resistance"] = (
            pctl(df["accurate_pass"]) * 0.25
            + pctl(df["won_contest"]) * 0.25
            + pctl(df["carry_to_foul_ratio"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.25
        )

        df["defensive_shield"] = (
            pctl(df["interception"]) * 0.30
            + pctl(df["interception_share"]) * 0.30
            + pctl(df["clean_defend_rate"]) * 0.25
            + pctl(df["fouls"], ascending=False) * 0.15
        )

        df["counter_press"] = (
            pctl(df["total_tackle"]) * 0.30
            + pctl(df["poss_won_att_3rd"]) * 0.25
            + pctl(df["interception"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.20
        )
