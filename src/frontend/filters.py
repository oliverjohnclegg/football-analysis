import streamlit as st
import pandas as pd
from src.frontend.tiering import TIER_CUTOFFS


def render_global_filters(managers: list[str], get_roles_fn):
    col1, col2 = st.columns(2)
    with col1:
        selected_manager = st.selectbox("Manager", options=managers)

    roles = get_roles_fn(selected_manager) if selected_manager else []
    with col2:
        selected_role = st.selectbox("Role Profile", options=roles)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    return selected_manager, selected_role


def render_data_filters(view_df: pd.DataFrame):
    fcol1, fcol2, fcol3, fcol4 = st.columns([2, 2, 2, 1])
    with fcol1:
        search_query = st.text_input("Search Player", value="").strip()
    with fcol2:
        all_tiers = [tier for _, tier in TIER_CUTOFFS]
        selected_tiers = st.multiselect("Tier Match", options=all_tiers, default=[])
    with fcol3:
        club_league_query = st.text_input("Club or League", value="").strip()
    with fcol4:
        st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
        current_season_only = st.checkbox("25/26 only", value=False)

    nationality_options = _sorted_unique(view_df, "Nationality")
    team_options = _sorted_unique(view_df, "Team")
    league_options = _sorted_unique(view_df, "League")

    dcol1, dcol2, dcol3 = st.columns(3)
    with dcol1:
        selected_nationalities = st.multiselect(
            "Nationality",
            options=nationality_options,
            default=[],
        )
    with dcol2:
        selected_teams = st.multiselect("Team", options=team_options, default=[])
    with dcol3:
        selected_leagues = st.multiselect("League", options=league_options, default=[])

    st.divider()

    return (
        search_query,
        selected_tiers,
        club_league_query,
        current_season_only,
        selected_nationalities,
        selected_teams,
        selected_leagues,
    )


def _sorted_unique(view_df: pd.DataFrame, column: str) -> list[str]:
    if column not in view_df.columns:
        return []
    values = view_df[column].dropna().astype(str).str.strip()
    values = values[values != ""]
    return sorted(values.unique().tolist())
