import streamlit as st
import json
import os

SAVE_FILE = "save_data.json"

def save_game():
    #Saves inventory, location, and game progress to a JSON file."""
    data = {
        "inventory": st.session_state.inventory,
        "location": st.session_state.location,
        "game_started": st.session_state.game_started
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def reset_game():
    #Deletes the save file and clears session state for a fresh start."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    # Clear session state and re-initialize with defaults
    st.rerun()

def init_session_state():
    # --- 1. LOAD FROM FILE ---
    saved_data = {}
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                saved_data = json.load(f)
        except:
            pass 

    # --- 2. INITIALIZE STATE (Persistent Data) ---
    if "logged_in" not in st.session_state: st.session_state.logged_in = False
    
    if "game_started" not in st.session_state: 
        st.session_state.game_started = saved_data.get("game_started", False)
    
    if "inventory" not in st.session_state: 
        # Give them 5 worms to start if it's a new game!
        st.session_state.inventory = saved_data.get("inventory", {"Worms": 5}) 
    
    if "location" not in st.session_state: 
        st.session_state.location = saved_data.get("location", "Plains")

    # --- 3. INITIALIZE STATE (Transient Data) ---
    if "fishing_step" not in st.session_state: st.session_state.fishing_step = "idle"
    if "player_hp" not in st.session_state: st.session_state.player_hp = 10
    if "fish_hp" not in st.session_state: st.session_state.fish_hp = 10
    if "current_fish" not in st.session_state: st.session_state.current_fish = ""
    if "fish_dir" not in st.session_state: st.session_state.fish_dir = "LEFT"
    if "splash_start_time" not in st.session_state: st.session_state.splash_start_time = 0
    if "move_start_time" not in st.session_state: st.session_state.move_start_time = 0