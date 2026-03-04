import streamlit as st
from logic.state import save_game


def show_forest():
    st.title("🌲 Western Forest")
    st.image("https://via.placeholder.com/800x400.png?text=Mysterious+Forest")

    st.write("""
    You step beneath the canopy of the western forest. Sunlight dances between the leaves,
    and the sounds of wildlife echo all around. The path ahead leads deeper into the woods,
    while the village is a comfortable distance to the east.
    """)

    if st.button("Return to Western Village"):
        st.session_state.location = "Western_Village_Gate"
        save_game()
        st.rerun()
