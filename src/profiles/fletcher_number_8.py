from src.profiles.base import PositionalProfile, ScatterChart, pctl, safe_ratio


class FletcherNumberEightProfile(PositionalProfile):
    name = "Fletcher #8 – Aggressive Box-to-Box Runner"
    slug = "fletcher/number_8"
    position_keywords = ["Mid"]

    dimension_weights = {
        "ball_carrying": 0.30,
        "box_arrival": 0.25,
        "creative_link": 0.25,
        "counter_press": 0.20,
    }

    radar_labels = [
        "Ball\nCarrying",
        "Box\nArrival",
        "Creative\nLink",
        "Counter-\nPress",
    ]

    ranking_title = "Top 25 – Fletcher System #8 Profile Fit"
    radar_title = "Top 5 #8 Candidates – Dimension Comparison"

    scatter_charts = [
        ScatterChart(
            "ball_carrying", "box_arrival",
            "Ball Carrying Score", "Box Arrival Score",
            "Driving Forward vs Arriving Late",
            "carrying_vs_arrival.png",
        ),
        ScatterChart(
            "creative_link", "counter_press",
            "Creative Link Score", "Counter-Press Score",
            "Playmaking vs Pressing Intensity",
            "link_vs_pressing.png",
        ),
    ]

    def _derive_efficiency_metrics(self, df):
        super()._derive_efficiency_metrics(df)
        passes = df.get("accurate_pass", 0)
        chances = df.get("total_att_assist", 0)
        df["chance_creation_rate"] = safe_ratio(chances, passes)

        shots = df.get("total_scoring_att", 0)
        xg90 = df.get("expected_goals_per_90", 0)
        df["xg_per_shot"] = safe_ratio(xg90, shots)

    def _compute_dimensions(self, df, nineties):
        df["ball_carrying"] = (
            pctl(df["won_contest"]) * 0.30
            + pctl(df["carry_to_foul_ratio"]) * 0.25
            + pctl(df["accurate_pass"]) * 0.25
            + pctl(df["progressive_pass_share"]) * 0.20
        )

        df["box_arrival"] = (
            pctl(df["expected_goals_per_90"]) * 0.35
            + pctl(df["xg_per_shot"]) * 0.30
            + pctl(df["goals_per_90"]) * 0.20
            + pctl(df["ontarget_scoring_att"]) * 0.15
        )

        df["creative_link"] = (
            pctl(df["expected_assists_per_90"]) * 0.30
            + pctl(df["chance_creation_rate"]) * 0.25
            + pctl(df["total_att_assist"]) * 0.25
            + pctl(df["accurate_pass"]) * 0.20
        )

        df["counter_press"] = (
            pctl(df["poss_won_att_3rd"]) * 0.30
            + pctl(df["total_tackle"]) * 0.25
            + pctl(df["interception"]) * 0.25
            + pctl(df["clean_defend_rate"]) * 0.20
        )
