import streamlit as st

def init_session_state():
    if "logged_in" not in st.session_state: st.session_state.logged_in = False
    if "game_started" not in st.session_state: st.session_state.game_started = False
    if "inventory" not in st.session_state: st.session_state.inventory = {}
    if "location" not in st.session_state: st.session_state.location = "Plains"
    if "fishing_step" not in st.session_state: st.session_state.fishing_step = "idle"
    if "player_hp" not in st.session_state: st.session_state.player_hp = 10
    if "fish_hp" not in st.session_state: st.session_state.fish_hp = 10
    if "current_fish" not in st.session_state: st.session_state.current_fish = ""
    if "fish_dir" not in st.session_state: st.session_state.fish_dir = "LEFT"
    if "splash_start_time" not in st.session_state: st.session_state.splash_start_time = 0
    if "move_start_time" not in st.session_state: st.session_state.move_start_time = 0