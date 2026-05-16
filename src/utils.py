import logging

import pandas as pd

logger = logging.getLogger(__name__)


def safe_col(df, *keys):
    for key in keys:
        try:
            result = df[key]
            if isinstance(result, pd.Series):
                return result
            if isinstance(result, pd.DataFrame) and result.shape[1] == 1:
                return result.iloc[:, 0]
        except (KeyError, TypeError):
            continue
    logger.warning(f"Column not found among: {keys}")
    return pd.Series(0.0, index=df.index)


def per90(series, nineties):
    return series.div(nineties).where(nineties > 0, 0)


def percentile_rank(series, ascending=True):
    return series.rank(pct=True, ascending=ascending) * 100
