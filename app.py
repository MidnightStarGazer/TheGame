import streamlit as st
import random

# --- INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "inventory" not in st.session_state:
    st.session_state.inventory = {}

# --- LOGIN DIALOG ---
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

# --- SIDEBAR (Appears after Login) ---
if st.session_state.logged_in:
    with st.sidebar:
        st.title("⚙️ Game Menu")
        menu_choice = st.radio("Navigation", ["Main Screen", "Inventory", "Reset Progress"])
        
        if menu_choice == "Inventory":
            st.subheader("🎒 Your Items")
            if not st.session_state.inventory:
                st.write("Your inventory is empty.")
            else:
                for item, count in st.session_state.inventory.items():
                    st.write(f"**{item}**: {count}")
        
        if menu_choice == "Reset Progress":
            if st.button("Confirm Reset"):
                st.session_state.game_started = False
                st.session_state.inventory = {}
                st.rerun()

# --- MAIN SCREEN LOGIC ---
if not st.session_state.logged_in:
    # First Step: Login Button
    st.markdown("<h1 style='text-align: center;'>THE GAME</h1>", unsafe_allow_html=True)
    if st.button("Access Creator Terminal"):
        login_dialog()

elif not st.session_state.game_started:
    # Second Step: Main Menu (Post-Login)
    st.markdown("<h1 style='text-align: center;'>WELCOME TO THE GAME</h1>", unsafe_allow_html=True)
    if st.button("START ->"):
        st.session_state.game_started = True
        st.rerun()

else:
    # Third Step: The Game Content (Vast Plains)
    st.title("🌾 Vast Plains")
    st.image("https://via.placeholder.com/800x400.png?text=Vast+Plains+Landscape") # Placeholder for your plains.png
    
    st.write("""
    You found yourself in the middle of a vast grassy field. You feel the wind blowing gently on your face, 
    the nice feel of grass, and the gentle heat of the sun.
    
    You also noticed a few rocks that seem to have wet soil around them. They might be hiding something useful.
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Search the rocks"):
            st.toast("Searching...")
            if random.random() > 0.5:
                worms = random.randint(1, 5)
                st.session_state.inventory["Worms"] = st.session_state.inventory.get("Worms", 0) + worms
                st.success(f"You found {worms} worms!")
            else:
                st.info("You didn't find anything.")
                
    with col2:
        if st.button("Follow the dirt track"):
            st.write("Walking toward the village...")
            # You can add logic here to change to 'village' state