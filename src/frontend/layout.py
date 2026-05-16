import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="Role Explorer",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="collapsed", # Minimized sidebar usage as per plan
    )

