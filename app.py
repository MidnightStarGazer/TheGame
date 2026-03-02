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
# NEW: Track where the player is in the world
if "location" not in st.session_state:
    st.session_state.location = "Plains"

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
                st.session_state.logged_in = False
                st.session_state.game_started = False
                st.session_state.location = "Plains" # Reset location on quit
                st.session_state.inventory = {} # Clears inventory on quit
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

# --- VAST PLAINS ---
elif st.session_state.location == "Plains":
    st.title("🌾 Vast Plains")
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
            with st.spinner("Walking towards the lake in the distance..."):
                time.sleep(2)
            # Change location and rerun to load the Lake screen
            st.session_state.location = "Lake"
            st.rerun()

# --- LAKESIDE ---
elif st.session_state.location == "Lake":
    st.title("🌊 Lake Side")
    
    st.image("https://via.placeholder.com/800x400.png?text=Peaceful+Lakeside")
    
    st.write("""
    You arrived at the lake. The air is filled with the crisp scent of water mingled with the earthy aroma of nearby foliage. 
    The gentle ripples of the water create a soothing melody, punctuated by the occasional call of distant birds.
    
    You gaze at the waters and see small fishes swimming around.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Fishing"):
            has_worms = st.session_state.inventory.get("Worms", 0) > 0
            
            # 1. Check for bait and set the message/deduct inventory
            if has_worms:
                msg = "Fishing for fish.........."
                st.session_state.inventory["Worms"] -= 1
                if st.session_state.inventory["Worms"] == 0:
                    del st.session_state.inventory["Worms"] # Clean up empty item
            else:
                msg = "Fishing without bait seems kinda silly.... but let's try anyway."
            
            # 2. The Fishing Sequence
            with st.spinner(msg):
                time.sleep(2)
            
            st.toast("You felt a tug!!")
            time.sleep(1)
            
            # 3. Probability Check (Replicating your JS logic)
            catch_chance = random.randint(1, 300) if has_worms else random.randint(1, 100)
            
            if catch_chance > 295: catch = "Huge Bass"
            elif catch_chance > 290: catch = "Cat-fish"
            elif catch_chance > 280: catch = "Bass"
            elif catch_chance > 260: catch = "Trout"
            elif catch_chance > 240: catch = "Perch"
            elif catch_chance > 220: catch = "Carp"
            elif catch_chance > 210: catch = "Rare Golden Fish"
            else: catch = None
            
            # 4. Result
            if catch:
                st.session_state.inventory[catch] = st.session_state.inventory.get(catch, 0) + 1
                st.success(f"You caught a {catch}! Enjoy your catch.")
            else:
                st.warning("You actually just caught a worthless kelp that got dragged by the current, you threw it away...")

    with col2:
        if st.button("Walk Back to the Plains"):
            with st.spinner("Heading back to the plains..."):
                time.sleep(1.5)
            st.session_state.location = "Plains"
            st.rerun()