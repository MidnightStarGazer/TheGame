import streamlit as st
import random
import time

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

        elif menu_choice == "Quit":
            st.warning("Are you sure you want to exit?")
            if st.button("Quit Game"):
                # Complete reset of the session state to go back to the start
                st.session_state.logged_in = False
                st.session_state.game_started = False
                st.rerun()

# --- MAIN SCREEN LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Welcome to My Game!</h1>", unsafe_allow_html=True)
    if st.button("Login"):
        login_dialog()

elif not st.session_state.game_started:
    st.markdown("<h1 style='text-align: center;'>WELCOME TO THE GAME</h1>", unsafe_allow_html=True)
    if st.button("START ->"):
        st.session_state.game_started = True
        st.rerun()

else:
    st.title("🌾 Vast Plains")
    # Using your existing landscape placeholder
    st.image("https://via.placeholder.com/800x400.png?text=Vast+Plains+Landscape") 
    
    st.write("""
    You found yourself in the middle of a vast grassy field. You feel the wind blowing gently on your face, 
    the nice feel of grass, and the gentle heat of the sun.
    
    You can also notice what seems to be a lake from afar towards the south of you.
             
    You also found a few rocks that seem to have wet soil around them. They might be hiding something useful.
    """)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Search the rocks"):
            with st.spinner("Searching the rocks..."):
                time.sleep(2) 
                
            if random.random() > 0.5:
                worms = random.randint(1, 5)
                st.session_state.inventory["Worms"] = st.session_state.inventory.get("Worms", 0) + worms
                st.success(f"You found {worms} worms!")
            else:
                st.info("You didn't find anything.")
                
    with col2:
        if st.button("Follow the dirt track"):
            st.write("Walking toward the village...")

    with col3:
        if st.button("Walk south"):
            st.write("Walking towards the lake in the distance.....")