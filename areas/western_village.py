import streamlit as st
from logic.state import save_game


def show_western_village():
    st.title("🏞️ Western Village Entrance")
    st.image("https://via.placeholder.com/800x400.png?text=Western+Village+Entrance")

    st.write("""
    You stand at the western edge of the village. To the north sits a sturdy blacksmith's shop,
    its forge smoke curling into the sky. The air smells of hot metal and coal.
    To the west, a dirt path disappears into a dense forest – the frontier beyond the village.
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enter the Blacksmith's"):  # placeholder behaviour
            st.info("The blacksmith is closed for now. Come back later.")
    with col2:
        if st.button("Head West to the Forest"):
            st.session_state.location = "Forest"
            save_game()
            st.rerun()

    if st.button("Go back to Village Center"):
        st.session_state.location = "Village"
        save_game()
        st.rerun()
