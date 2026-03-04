import streamlit as st
from logic.state import init_session_state, save_game, reset_game
from areas.plains import show_plains
from areas.lake import show_lake
from areas.village import show_village
from areas.fishmonger import show_fishmonger
from areas.guild import show_guild
from utils.quest_tracker import display_quest_progress

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
if st.session_state.logged_in:
    with st.sidebar:
        # The Badge is now the anchor! 
        # If it's in the inventory, they are an adventurer.
        has_badge = "Adventurer's Badge" in st.session_state.inventory

        if has_badge:
            st.markdown(f"<h2 style='text-align: center;'>🛡️ {st.session_state.player_name}</h2>", unsafe_allow_html=True)
            st.caption("Rank: F Adventurer")
        else:
            st.markdown("<h2 style='text-align: center;'>🛡️ <b>???</b></h2>", unsafe_allow_html=True)
            st.caption("Status: Unregistered")
        
        st.divider()

    with st.sidebar:
        st.title("⚙️ Game Menu")
        # Here is your new menu options
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
        if st.button("NEW GAME", use_container_width=True, type="primary"):
            # This is the heavy reset from your state.py
            reset_game() 

else:
    # Navigation logic - checks where you are and shows that file
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