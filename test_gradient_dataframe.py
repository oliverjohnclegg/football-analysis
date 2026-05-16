import streamlit as st
import pandas as pd

df = pd.DataFrame({"Score": [50.0, 80.0, 99.0]})

def color_bar(val):
    color = "red" if val < 60 else "green"
    return f"background: linear-gradient(90deg, {color} {val}%, transparent {val}%);"

st.dataframe(df.style.map(color_bar), selection_mode="single-row", on_select="rerun")
