import streamlit as st
import pandas as pd
from src.frontend.tiering import TIER_COLORS

def render_comparison_grid(view_df: pd.DataFrame, pillar_cols: list[str]):
    """
    Renders the modern comparison grid using st.dataframe.
    Supports row selection and custom column formatting (progress bars for percentiles).
    Returns the selected row index (if any).
    """
    def style_row(row):
        tier = row.get("_Raw_Tier", "C")
        style = TIER_COLORS.get(tier, {'bg': '#555', 'fg': '#fff'})
        res = [''] * len(row)
        try:
            # Color the player's Name to indicate their tier, since ProgressColumn
            # cannot be colored per-row in Streamlit's canvas grid.
            idx = row.index.get_loc("Name")
            res[idx] = f"color: {style['bg']}; font-weight: bold;"
        except KeyError:
            pass
        return res
        
    styled_df = view_df.style.apply(style_row, axis=1)

    column_config = {
        "Score": None, # Hide raw score
        "Score Pctl": st.column_config.ProgressColumn(
            "Score %",
            help="Percentile Rank",
            min_value=0.0,
            max_value=100.0,
            format="%f",
            width="medium", # Score % is relatively double the width of other %s
        ),
        "Tier": None, # Hide Tier as it can be derived from Score %
        "Name": st.column_config.TextColumn(
            "Player",
            width="medium",
        ),
        "_Raw_Tier": None,  # Hide internal filter column
        "_Has_Primary": None, # Hide internal filter column
        "_Club_League": st.column_config.TextColumn("Club & League", width="medium"),
        "Nationality": st.column_config.TextColumn("Nationality", width="small"),
        "_Nationality": None,
        "Team": None,
        "League": None,
    }

    for col in pillar_cols:
        label = col.replace('_', ' ').title()
        # Hide the raw value
        column_config[label] = None
        # The percentile rendered as a progress bar (shorter horizontally)
        column_config[f"{label} Pctl"] = st.column_config.ProgressColumn(
            f"{label} %",
            min_value=0.0,
            max_value=100.0,
            format="%f",
            width="small",
        )
        # Hide the individual stat tier
        column_config[f"{label} Tier"] = None

    # Render interactive dataframe
    # Streamlit natively handles sticky headers and zebra striping is default
    selection_state = st.dataframe(
        styled_df,
        width="stretch",
        height=800, # Expand vertically to take up most of the page height
        hide_index=True,
        column_config=column_config,
        selection_mode="single-row",
        on_select="rerun"
    )
    
    # Extract selected row index
    selected_rows = selection_state.selection.rows
    if selected_rows:
        # Return the actual player_id (index) of the selected row
        return view_df.iloc[selected_rows[0]].name
    return None
