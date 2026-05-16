import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "Score Pctl": [99.0, 85.0, 50.0],
    "Tier": ['S', 'B', 'C']
})

TIER_COLORS = {
    'S': '#c084fc',
    'B': '#3b82f6',
    'C': '#eab308'
}

def get_color(val):
    if val >= 90: return TIER_COLORS['S']
    elif val >= 75: return TIER_COLORS['B']
    else: return TIER_COLORS['C']

# Pandas styler bar doesn't easily let us change color per row via a simple function in older pandas,
# but let's test if we can do something like this or if it renders in st.dataframe
styler = df.style.bar(subset=["Score Pctl"], color="#c084fc", vmin=0, vmax=100)

st.dataframe(styler, selection_mode="single-row", on_select="rerun")
