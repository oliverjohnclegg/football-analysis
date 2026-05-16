import streamlit as st
from src.frontend.tiering import TIER_CUTOFFS

def render_global_filters(managers: list[str], get_roles_fn):
    """
    Renders top-level global controls.
    Returns the filter state.
    """
    col1, col2 = st.columns(2)
    with col1:
        selected_manager = st.selectbox("Manager", options=managers)
    
    roles = get_roles_fn(selected_manager) if selected_manager else []
    with col2:
        selected_role = st.selectbox("Role Profile", options=roles)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    fcol1, fcol2, fcol3, fcol4 = st.columns([2, 2, 2, 1])
    with fcol1:
        search_query = st.text_input("🔍 Search Player", value="").strip()
    with fcol2:
        all_tiers = [t for _, t in TIER_CUTOFFS]
        selected_tiers = st.multiselect("🎯 Tier Match", options=all_tiers, default=[])
    with fcol3:
        club_league_query = st.text_input("🏟️ Club or League", value="").strip()
    with fcol4:
        # Spacing to align checkbox with inputs
        st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
        current_season_only = st.checkbox("25/26 only", value=False)
        
    st.divider()
        
    return selected_manager, selected_role, search_query, selected_tiers, club_league_query, current_season_only
