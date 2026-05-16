import streamlit as st

def apply_theme():
    """
    Injects custom 2026 modern CSS styling into the Streamlit app.
    Focuses on typography, hierarchical spacing, and premium card/container aesthetics.
    """
    st.markdown("""
    <style>
        /* Base typography (Inter/Roboto are usually default if set in config.toml, but we enforce fallbacks here) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Number/Monospace targeting for data grids */
        .stDataFrame [data-testid="StyledDataFrameDataCell"] {
            font-family: 'Roboto Mono', monospace !important;
            font-size: 0.9rem !important;
        }

        /* Subtle gradients and borders for the main view container */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        /* Modern details panel / cards */
        .modern-card {
            background-color: rgba(25, 25, 28, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            margin-bottom: 1rem;
        }

        .stat-group-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #888;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        /* Typography Hierarchy */
        .player-name-main {
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 0.1rem;
            background: linear-gradient(90deg, #ffffff, #aaaaaa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .player-club-sub {
            font-size: 0.95rem;
            color: #888;
            font-weight: 400;
            margin-bottom: 1rem;
        }
        
        /* Grid overrides to tighten row padding and zebra striping */
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }
    </style>
    """, unsafe_allow_html=True)
