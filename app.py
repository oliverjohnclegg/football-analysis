import streamlit as st
import pandas as pd

from src.frontend.layout import setup_page
from src.frontend.theme import apply_theme
from src.frontend.filters import render_global_filters
from src.frontend.grid import render_comparison_grid
from src.frontend.details import render_player_details
from src.frontend.data_catalog import get_managers, get_roles, load_role_data
from src.frontend.tiering import apply_tiers_to_dataframe
from src.frontend.table_model import build_ui_view_model
from src.frontend.add_player import render_add_player_controls
from src.profiles import PROFILES

# 1. Setup Page & Theme
setup_page()
apply_theme()

# 3. Global Configuration
managers = get_managers()
if not managers:
    st.warning("No managers found in output directory.")
    st.stop()

selected_manager, selected_role, search_query, selected_tiers, club_league_query, current_season_only = render_global_filters(managers, get_roles)

if not selected_manager or not selected_role:
    st.stop()

render_add_player_controls()

# 4. Data Loading
try:
    df, pillar_cols = load_role_data(selected_manager, selected_role)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Apply tiers
df_tiered = apply_tiers_to_dataframe(df, "composite_score", pillar_cols)

# 5. Build View Models
view_df, raw_df = build_ui_view_model(df_tiered, "composite_score", pillar_cols)

# 6. Apply Filters
mask = pd.Series(True, index=view_df.index)

if search_query:
    mask &= view_df["Name"].str.contains(search_query, case=False, na=False)

if selected_tiers:
    mask &= view_df["_Raw_Tier"].isin(selected_tiers)
    
if club_league_query:
    mask &= view_df["_Club_League"].str.contains(club_league_query, case=False, na=False)

if current_season_only:
    mask &= view_df["_Has_Primary"].astype(bool)

filtered_view_df = view_df[mask].copy()

# Sort by Composite Score Descending
filtered_view_df = filtered_view_df.sort_values(by="Score", ascending=False)
st.write(f"**Showing {len(filtered_view_df)} players**")

# 7. Grid Layout
selected_player_id = render_comparison_grid(filtered_view_df, pillar_cols)

if selected_player_id is not None:
    # Load the selected player's raw stats
    selected_row = raw_df.loc[selected_player_id]
    
    # Resolve profile for radar metadata
    slug = f"{selected_manager}/{selected_role}"
    profile_cls = PROFILES.get(slug)
    
    # Render the deep dive panel in a modal
    render_player_details(selected_row, profile_cls)
