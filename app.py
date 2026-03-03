import streamlit as st
from logic.state import init_session_state, save_game, reset_game
from areas.plains import show_plains
from areas.lake import show_lake
from areas.village import show_village
from areas.fishmonger import show_fishmonger

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
        st.title("⚙️ Game Menu")
        menu_choice = st.radio("Navigation", ["Inventory", "Quit"])
        
        if menu_choice == "Inventory":
            st.subheader("🎒 Your Items")
            if not st.session_state.inventory:
                st.write("Your inventory is empty.")
            else:
                for item, count in st.session_state.inventory.items():
                    st.write(f"**{item}**: {count}")
            
            # Dedicated Save Button inside Inventory
            if st.button("💾 Save Progress"):
                save_game()
                st.toast("Progress Saved!", icon="💾")

        elif menu_choice == "Quit":
            st.warning("Logout of the session?")
            if st.button("Logout"):
                st.session_state.logged_in = False # Log out without deleting save
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
            reset_game() # Clears file and memory

else:
    # Navigation logic
    if st.session_state.location == "Plains": show_plains()
    elif st.session_state.location == "Lake": show_lake()
    elif st.session_state.location == "Village": show_village()
    elif st.session_state.location == "Fishmonger": show_fishmonger()