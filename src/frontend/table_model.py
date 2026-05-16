import pandas as pd
from src.config import PRIMARY_SEASON

def build_ui_view_model(df: pd.DataFrame, score_col: str, pillar_cols: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Transforms the tiered dataframe into a structured view model for the interactive grid.
    Returns a tuple of (view_df, raw_df) both indexed by player_id.
    """
    # Reset index to ensure uniqueness for Styler
    df = df.reset_index(drop=True)
        
    view_df = pd.DataFrame(index=df.index)
    
    # 1. Identity & Hierarchy
    view_df["Tier"] = df.get(f"{score_col}_tier", "C").values
    if "is_manual_add" in df.columns:
        is_manual = df["is_manual_add"].fillna(False).astype(bool).values
    else:
        is_manual = [False] * len(df)
    view_df["Name"] = [
        f"{name}*" if manual else name
        for name, manual in zip(df["player"].values, is_manual)
    ]
    view_df["Team"] = df.get("team", "Unknown").values
    view_df["League"] = df.get("league", "Unknown").values
    
    # 2. Composite Score
    view_df["Score"] = df[score_col].round(2).values
    view_df["Score Pctl"] = df.get(f"{score_col}_pctl", 0).round(1).values
    
    # 3. Dynamic Pillar Stats (Raw values and Percentiles for bars)
    for col in pillar_cols:
        label = col.replace('_', ' ').title()
        view_df[label] = df[col].round(2).values
        view_df[f"{label} Pctl"] = df.get(f"{col}_pctl", 0).round(1).values
        view_df[f"{label} Tier"] = df.get(f"{col}_tier", "C").values

    # Internal flags for filtering
    view_df["_Raw_Tier"] = df.get(f"{score_col}_tier", "C").values
    view_df["_Has_Primary"] = df.get("has_primary_season", True).values
    view_df["_Club_League"] = view_df["Team"] + " " + view_df["League"]
    
    return view_df, df
