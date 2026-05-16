import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "Score Pctl": [99.0, 85.0, 50.0],
    "_Raw_Tier": ['S', 'B', 'C']
})

TIER_COLORS = {
    'S': 'hsl(280, 100%, 60%)',
    'B': 'hsl(210, 80%, 45%)',
    'C': 'hsl(60, 80%, 35%)'
}

def style_df(row):
    tier = row.get("_Raw_Tier", "C")
    color = TIER_COLORS.get(tier, '#555')
    res = [''] * len(row)
    idx = row.index.get_loc("Score Pctl")
    val = row["Score Pctl"]
    # Linear gradient to act as a progress bar
    res[idx] = f"background: linear-gradient(90deg, {color} {val}%, transparent {val}%); color: white;"
    return res

styled_df = df.style.apply(style_df, axis=1)

st.dataframe(
    styled_df,
    column_config={
        "Score Pctl": st.column_config.NumberColumn("Score %", format="%.1f"),
        "_Raw_Tier": None
    },
    selection_mode="single-row",
    on_select="rerun"
)
