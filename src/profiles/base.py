from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


def pctl(series, ascending=True):
    return series.rank(pct=True, ascending=ascending) * 100


def safe_ratio(numerator, denominator, fill=0.0):
    denom = denominator.replace(0, np.nan)
    return (numerator / denom).fillna(fill)


@dataclass
class ScatterChart:
    x_col: str
    y_col: str
    xlabel: str
    ylabel: str
    title: str
    filename: str


class PositionalProfile:
    name: str = ""
    slug: str = ""
    position_keywords: list[str] = []
    dimension_weights: dict[str, float] = {}
    radar_labels: list[str] = []
    ranking_title: str = ""
    radar_title: str = ""
    scatter_charts: list[ScatterChart] = []

    def filter_position(self, df: pd.DataFrame) -> pd.DataFrame:
        mask = pd.Series(False, index=df.index)
        for keyword in self.position_keywords:
            mask |= df["position"].str.contains(keyword, case=False, na=False)
        return df[mask]

    def build(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        numeric = result.select_dtypes(include="number").columns
        result[numeric] = result[numeric].fillna(0)
        nineties = result["minutes_played"] / 90

        self._derive_efficiency_metrics(result)
        self._compute_dimensions(result, nineties)

        result["composite_score"] = self.geometric_composite(result)
        return result.sort_values("composite_score", ascending=False)

    def _derive_efficiency_metrics(self, df: pd.DataFrame):
        tkl = df.get("total_tackle", 0)
        intr = df.get("interception", 0)
        fouls = df.get("fouls", 0)
        passes = df.get("accurate_pass", 0)
        long_balls = df.get("accurate_long_balls", 0)
        dribbles = df.get("won_contest", 0)

        df["clean_defend_rate"] = safe_ratio(tkl + intr, tkl + intr + fouls)
        df["interception_share"] = safe_ratio(intr, tkl + intr)
        df["progressive_pass_share"] = safe_ratio(long_balls, passes)
        df["carry_to_foul_ratio"] = safe_ratio(dribbles, fouls)

    def geometric_composite(self, df: pd.DataFrame) -> pd.Series:
        log_sum = pd.Series(0.0, index=df.index)
        for dim, weight in self.dimension_weights.items():
            clamped = df[dim].clip(lower=1.0)
            log_sum += weight * np.log(clamped)
        return np.exp(log_sum)

    def _compute_dimensions(self, df: pd.DataFrame, nineties: pd.Series):
        raise NotImplementedError

    def summary_columns(self) -> list[str]:
        return [
            "player", "team", "league", "minutes_played",
            *self.dimension_weights.keys(),
            "composite_score",
        ]
