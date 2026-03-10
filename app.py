import streamlit as st
from logic.state import init_session_state, save_game, reset_game
from areas.plains import show_plains
from areas.lake import show_lake
from areas.village import show_village
from areas.fishmonger import show_fishmonger
from areas.guild import show_guild
from areas.western_village import show_western_village
from areas.forest import show_forest
from utils.quest_tracker import display_quest_progress
from utils.playerStats import display_character_status, show_weapon_selection, show_armor_selection

# --- INITIALIZATION ---
init_session_state()


# --- DIALOGS (Login) ---
@st.dialog("Login to TheGame")
def login_dialog():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        if username == "ajtd" and password == "ajtd2":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect credentials.")

# --- SIDEBAR ---
# only show sidebar once the actual game has started
if st.session_state.logged_in and st.session_state.game_started:
    with st.sidebar:
        # Show player name if available; badge indicates adventurer status
        has_badge = "Adventurer's Badge" in st.session_state.inventory
        player_display = st.session_state.player_name or "???"

        st.markdown(f"<h2 style='text-align: center;'>🛡️ {player_display}</h2>", unsafe_allow_html=True)
        if has_badge:
            st.caption("Rank: F Adventurer")
        else:
            st.caption("Status: Unregistered")

        # Toggle between Menu and Character Stats
        if st.button("Character Stats"):
            st.session_state.show_character_status = True
            st.rerun()

        st.divider()
        
        # Toggle back to menu from character stats
        if st.button("⚙️ Back to Menu"):
            st.session_state.show_character_status = False
            st.rerun()

    # --- CHARACTER STATS SIDEBAR THINGY---
    if st.session_state.show_character_status:
        with st.sidebar:
            st.title("Character Stats")
            
            # This shit does weapon/armor selection or display stats
            if st.session_state.selecting_weapon:
                show_weapon_selection()
            elif st.session_state.selecting_armor:
                show_armor_selection()
            else:
                display_character_status()
    
    # --- GAME MENU SIDEBAR THINGY ---
    else:
        with st.sidebar:
            st.title("⚙️ Game Menu")
            menu_choice = st.radio("Navigation", ["Inventory", "Quest Progress", "Quit to Menu", "Logout"])
            
            if menu_choice == "Inventory":
                st.subheader("🎒 Your Items")
                if not st.session_state.inventory:
                    st.write("Your inventory is empty.")
                else:
                    for item, count in st.session_state.inventory.items():
                        st.write(f"**{item}**: {count}")
                
                if st.button("💾 Save Progress"):
                    save_game()
                    st.toast("Progress Saved!", icon="💾")

            elif menu_choice == "Quest Progress":
                st.subheader("📜 Quest Progress")
                display_quest_progress()

            elif menu_choice == "Quit to Menu":
                st.warning("Return to the Start screen?")
                if st.button("Confirm Quit"):
                    # This just toggles the screen, doesn't log you out
                    st.session_state.game_started = False 
                    st.rerun()

            elif menu_choice == "Logout":
                st.error("This will take you back to the login screen.")
                if st.button("Confirm Logout"):
                    st.session_state.logged_in = False
                    st.session_state.game_started = False 
                    st.rerun()


# --- MAIN ROUTING LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Welcome to My Game!</h1>", unsafe_allow_html=True)
    if st.button("Login"):
        login_dialog()

elif not st.session_state.game_started:
    st.markdown("<h1 style='text-align: center;'>WELCOME TO THE GAME</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("START GAME ->", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
    with col2:
        # This button now clears everything AND enters the game
        if st.button("NEW GAME", use_container_width=True, type="primary"):
            reset_game()

else:
    # Navigation shit - checks where you are and shows that file
    if st.session_state.location == "Plains": 
        show_plains()
    elif st.session_state.location == "Lake": 
        show_lake()
    elif st.session_state.location == "Village": 
        show_village()
    elif st.session_state.location == "Fishmonger": 
        show_fishmonger()
    elif st.session_state.location == "Guild":
        show_guild()
    elif st.session_state.location == "Western_Village_Gate":
        show_western_village()
    elif st.session_state.location == "Forest":
        show_forest()
