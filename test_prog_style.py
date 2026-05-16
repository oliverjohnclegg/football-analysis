import streamlit as st
import pandas as pd

df = pd.DataFrame({"Score Pctl": [90.0, 50.0]})

def color_bar(val):
    # Try to color the text to see if it colors the ProgressColumn fill
    return "color: purple;"

st.dataframe(
    df.style.map(color_bar),
    column_config={"Score Pctl": st.column_config.ProgressColumn("Score %")},
)
