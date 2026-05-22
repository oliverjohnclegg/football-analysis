from src.profiles.base import PositionalProfile, ScatterChart, pctl


class TuchelWideCBProfile(PositionalProfile):
    name = "Tuchel Wide CB – Step-Out Hybrid"
    slug = "tuchel/wide_cb"
    position_keywords = ["Defender"]

    dimension_weights = {
        "step_out_carry": 0.30,
        "line_breaking_distribution": 0.30,
        "channel_defending": 0.25,
        "counterpress_wide": 0.15,
    }

    radar_labels = [
        "Step-Out\nCarry",
        "Line-Breaking\nDistribution",
        "Channel\nDefending",
        "Counterpress\nWide",
    ]

    ranking_title = "Top 25 – Tuchel System Wide CB Profile Fit"
    radar_title = "Top 5 Wide CB Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "step_out_carry", "line_breaking_distribution",
            "Step-Out Carry Score", "Line-Breaking Distribution Score",
            "Carrying vs Distribution",
            "carry_vs_distribution.png",
        ),
        ScatterChart(
            "channel_defending", "counterpress_wide",
            "Channel Defending Score", "Counterpress Wide Score",
            "Channel Defence vs Transition Press",
            "channel_vs_counterpress.png",
        ),
    ]

    def _compute_dimensions(self, df, nineties):
        df["step_out_carry"] = (
            pctl(df["won_contest"]) * 0.40
            + pctl(df["carry_to_foul_ratio"]) * 0.35
            + pctl(df["fouls"], ascending=False) * 0.25
        )

        df["line_breaking_distribution"] = (
            pctl(df["accurate_long_balls"]) * 0.35
            + pctl(df["progressive_pass_share"]) * 0.35
            + pctl(df["total_att_assist"]) * 0.30
        )

        df["channel_defending"] = (
            pctl(df["total_tackle"]) * 0.35
            + pctl(df["clean_defend_rate"]) * 0.35
            + pctl(df["interception"]) * 0.30
        )

        df["counterpress_wide"] = (
            pctl(df["poss_won_att_3rd"]) * 0.50
            + pctl(df["total_tackle"]) * 0.30
            + pctl(df["interception_share"]) * 0.20
        )
