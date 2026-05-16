import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "Score Pctl": [99.0, 85.0, 50.0],
    "Tier": ['S', 'B', 'C']
})

def bg_color(val):
    return "background-color: hsl(280, 100%, 60%); color: white"

styler = df.style.map(bg_color, subset=["Score Pctl"])

st.dataframe(
    styler,
    column_config={
        "Score Pctl": st.column_config.ProgressColumn(
            "Score %",
            format="%f",
            min_value=0,
            max_value=100
        )
    },
    selection_mode="single-row",
    on_select="rerun"
)
