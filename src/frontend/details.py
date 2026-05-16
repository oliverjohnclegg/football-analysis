import streamlit as st
import pandas as pd
import plotly.express as px

# Heuristic groupings for raw stats
DEFENSIVE_COLS = ["total_tackle", "interception", "outfielder_block", "effective_clearance", 
                  "poss_won_att_3rd", "fouls", "saves", "clean_sheet", "clean_defend_rate", "interception_share"]

POSSESSION_COLS = ["accurate_pass", "accurate_long_balls", "total_att_assist", "won_contest", 
                   "expected_assists", "expected_assists_per_90", "big_chance_created", 
                   "progressive_pass_share", "carry_to_foul_ratio", "chance_quality"]

ATTACKING_COLS = ["expected_goals_per_90", "goals_per_90", "ontarget_scoring_att", 
                  "total_scoring_att", "goal_assist", "shot_accuracy", "xg_per_shot"]

def _render_stat_group(title: str, cols: list[str], row: pd.Series):
    """Render a card with grouped stats."""
    valid_cols = [c for c in cols if c in row.index and pd.notna(row[c])]
    if not valid_cols:
        return

    st.markdown(f'<div class="modern-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-group-title">{title}</div>', unsafe_allow_html=True)
    
    # Use standard Streamlit metrics or basic columns
    # Split into pairs
    pairs = [valid_cols[i:i+2] for i in range(0, len(valid_cols), 2)]
    for pair in pairs:
        cols_ui = st.columns(len(pair))
        for i, c in enumerate(pair):
            label = c.replace('_', ' ').title()
            val = row[c]
            if isinstance(val, float):
                formatted_val = f"{val:.2f}"
            else:
                formatted_val = str(val)
            cols_ui[i].metric(label, formatted_val)
            
    st.markdown('</div>', unsafe_allow_html=True)

@st.dialog("Player Details", width="large")
def render_player_details(row: pd.Series, profile_cls=None):
    """
    Renders the right-side detail panel for a selected player.
    """
    # Header Identity
    st.markdown(f'<div class="player-name-main">{row["player"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="player-club-sub">{row.get("team", "Unknown")} • {row.get("league", "Unknown")}</div>', unsafe_allow_html=True)
    
    tier = row.get("composite_score_tier", "C")
    score = row.get("composite_score", 0.0)
    st.markdown(f"**Composite Score:** {score:.2f} (Tier {tier})")
    st.divider()

    # Radar Chart
    if profile_cls and hasattr(profile_cls, "dimension_weights"):
        dims = list(profile_cls.dimension_weights.keys())
        # Try to use profile's radar labels, otherwise format the dim names
        labels = getattr(profile_cls, "radar_labels", [d.replace('_', ' ').title() for d in dims])
        
        # Extract values (percentiles make best radar charts)
        vals = []
        for d in dims:
            pctl_col = f"{d}_pctl"
            if pctl_col in row.index:
                vals.append(row[pctl_col])
            else:
                vals.append(row.get(d, 0.0))
                
        # Close the loop for a polygon
        if vals:
            radar_df = pd.DataFrame(dict(
                r=vals + [vals[0]],
                theta=labels + [labels[0]]
            ))
            
            fig = px.line_polar(
                radar_df, r='r', theta='theta', line_close=True,
                color_discrete_sequence=['#c084fc']
            )
            fig.update_traces(fill='toself', fillcolor='rgba(192, 132, 252, 0.2)')
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100]),
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=20, b=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.subheader("Deep Dive Stats")
    
    # Stat Cards
    _render_stat_group("Defensive Work", DEFENSIVE_COLS, row)
    _render_stat_group("Possession & Creation", POSSESSION_COLS, row)
    _render_stat_group("Attacking Output", ATTACKING_COLS, row)
