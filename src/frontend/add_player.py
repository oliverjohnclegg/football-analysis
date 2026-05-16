import streamlit as st

from src.fotmob_fetcher import FotMobFetcher
from src.manual_add_service import ManualAddService, DuplicatePlayerError, PlayerNotFoundError


def render_add_player_controls():
    with st.expander("➕ Add Player to Dataset", expanded=False):
        search_term = st.text_input(
            "Search any player (name)", key="add_player_search", value="",
        ).strip()

        if not search_term or len(search_term) < 2:
            return

        fetcher = FotMobFetcher()
        try:
            results = fetcher.search_players(search_term)
        except Exception as exc:
            st.error(f"Search failed: {exc}")
            return

        if not results:
            st.info("No players found.")
            return

        options = {
            f"{r['player']} ({r['team']})": r for r in results
        }
        selected_label = st.selectbox(
            "Select player", options=list(options.keys()), key="add_player_select",
        )
        selected = options[selected_label]

        if st.button("Add to Dataset", key="add_player_btn"):
            with st.spinner("Fetching stats and computing metrics..."):
                try:
                    service = ManualAddService()
                    added_to = service.add_player(
                        selected["player_id"], selected["team_id"],
                    )
                    roles = ", ".join(f"`{s}`" for s in added_to)
                    st.success(f"Added **{selected['player']}** to {roles}")
                    st.rerun()
                except PlayerNotFoundError as exc:
                    st.warning(str(exc))
                except Exception as exc:
                    st.error(f"Failed to add player: {exc}")
