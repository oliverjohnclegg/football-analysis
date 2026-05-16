import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "Score Pctl": [99.0, 85.0, 50.0],
    "_Raw_Tier": ['S', 'B', 'C']
})

TIER_COLORS = {
    'S':  {'bg': 'hsl(280, 100%, 60%)', 'fg': '#ffffff'},
    'B':  {'bg': 'hsl(210, 80%, 45%)',  'fg': '#ffffff'},
    'C':  {'bg': 'hsl(60, 80%, 35%)',   'fg': '#ffffff'}
}

def style_df(row):
    tier = row.get("_Raw_Tier", "C")
    style = TIER_COLORS.get(tier, {'bg': '#555', 'fg': '#fff'})
    res = [''] * len(row)
    idx = row.index.get_loc("Score Pctl")
    res[idx] = f"background-color: {style['bg']}; color: {style['fg']}"
    return res

styled_df = df.style.apply(style_df, axis=1)

st.dataframe(
    styled_df,
    column_config={
        "Score Pctl": st.column_config.NumberColumn("Score %", format="%.2f"),
        "_Raw_Tier": None
    },
    selection_mode="single-row",
    on_select="rerun"
)
