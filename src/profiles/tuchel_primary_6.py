from src.profiles.base import PositionalProfile, ScatterChart, pctl


class TuchelPrimarySixProfile(PositionalProfile):
    name = "Tuchel #6 – Regista Pivot"
    slug = "tuchel/primary_6"
    position_keywords = ["Mid"]

    dimension_weights = {
        "tempo_circulation": 0.30,
        "switch_range": 0.25,
        "press_resistance": 0.25,
        "rest_defence_screen": 0.20,
    }

    radar_labels = [
        "Tempo\nCirculation",
        "Switch\nRange",
        "Press\nResistance",
        "Rest-Defence\nScreen",
    ]

    ranking_title = "Top 25 – Tuchel System Regista #6 Profile Fit"
    radar_title = "Top 5 Regista #6 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "tempo_circulation", "switch_range",
            "Tempo Circulation Score", "Switch Range Score",
            "Circulation vs Range",
            "tempo_vs_switch.png",
        ),
        ScatterChart(
            "press_resistance", "rest_defence_screen",
            "Press Resistance Score", "Rest-Defence Screen Score",
            "Composure vs Screening",
            "composure_vs_screen.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["tempo_circulation"] = (
            pctl(df["accurate_pass"]) * 0.55
            + pctl(df["progressive_pass_share"]) * 0.45
        )

        df["switch_range"] = (
            pctl(df["accurate_long_balls"]) * 0.55
            + pctl(df["progressive_pass_share"]) * 0.45
        )

        df["press_resistance"] = (
            pctl(df["accurate_pass"]) * 0.30
            + pctl(df["carry_to_foul_ratio"]) * 0.35
            + pctl(df["fouls"], ascending=False) * 0.35
        )

        df["rest_defence_screen"] = (
            pctl(df["interception"]) * 0.35
            + pctl(df["clean_defend_rate"]) * 0.35
            + pctl(df["interception_share"]) * 0.30
        )
