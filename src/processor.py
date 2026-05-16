import pandas as pd

from src.config import MINIMUM_MINUTES, POSITION_FILTER
from src.utils import safe_col


class DataProcessor:
    def filter_qualifying_midfielders(
        self, stats: dict[str, pd.DataFrame]
    ) -> dict[str, pd.DataFrame]:
        standard = stats["standard"]
        position = safe_col(standard, "pos", ("pos", ""), ("", "pos"))
        minutes = safe_col(standard, ("Playing Time", "Min"))
        mask = (
            position.str.contains(POSITION_FILTER, na=False)
            & (minutes >= MINIMUM_MINUTES)
        )
        qualifying_idx = standard[mask].index
        return {
            stat_type: df.loc[df.index.isin(qualifying_idx)]
            for stat_type, df in stats.items()
        }
