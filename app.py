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
if "fishing_step" not in st.session_state:
    st.session_state.fishing_step = "idle"
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 10
if "fish_hp" not in st.session_state:
    st.session_state.fish_hp = 10
if "current_fish" not in st.session_state:
    st.session_state.current_fish = ""
if "fish_dir" not in st.session_state:
    st.session_state.fish_dir = "LEFT"
if "splash_start_time" not in st.session_state:
    st.session_state.splash_start_time = 0
if "move_start_time" not in st.session_state:
    st.session_state.move_start_time = 0

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

# --- BUY WORMS DIALOG ---
@st.dialog("Buy Worms")
def buy_worms_dialog():
    st.write("Select the bundle size:")
    coins = st.session_state.inventory.get("coins", 0)
    
    col1, col2, col3 = st.columns(3)
    
    def purchase(cost, amount, name):
        if coins >= cost:
            st.session_state.inventory["coins"] -= cost
            st.session_state.inventory["Worms"] = st.session_state.inventory.get("Worms", 0) + amount
            st.success(f"You bought a {name} for {cost} coins.")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("You don't have enough coins to buy this bundle.")

    with col1:
        if st.button("Small (5 coins)"): purchase(5, 5, "Small Bundle")
    with col2:
        if st.button("Medium (10 coins)"): purchase(10, 10, "Medium Bundle")
    with col3:
        if st.button("Large (15 coins)"): purchase(15, 15, "Large Bundle")

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
                st.session_state.location = "Plains"
                st.session_state.inventory = {}
                st.session_state.fishing_step = "idle"
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
            with st.spinner("Walking toward the village..."):
                time.sleep(1.5)
            st.session_state.location = "Village"
            st.rerun()

    with col3:
        if st.button("Walk south"):
            with st.spinner("Walking towards the lake in the distance..."):
                time.sleep(2)
            st.session_state.location = "Lake"
            st.rerun()

# --- LAKESIDE --- 
elif st.session_state.location == "Lake":
    st.title("🌊 Lake Side")
    st.image("https://via.placeholder.com/800x400.png?text=Peaceful+Lakeside")
    
    st.write("You arrived at the lake. You gaze at the waters and see small fishes swimming around.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        placeholder = st.empty()
        
        # IDLE: The Start
        if st.session_state.fishing_step == "idle":
            if st.button("Start Fishing"):
                if st.session_state.inventory.get("Worms", 0) > 0:
                    st.session_state.inventory["Worms"] -= 1
                    if st.session_state.inventory["Worms"] == 0:
                        del st.session_state.inventory["Worms"]
                    st.session_state.fishing_step = "waiting"
                    st.rerun()
                else:
                    st.warning("Fishing without bait seems kinda silly.... you need Worms.")

        # WAITING: The Bubble Loop
        elif st.session_state.fishing_step == "waiting":
            placeholder.info("Bubble... Bubble... Bubble...")
            time.sleep(4)
            # Randomly pick if the splash is a fake-out or the real deal
            st.session_state.fishing_step = random.choice(["fake_splash", "real_splash"])
            st.rerun()

        # FAKE SPLASH: Too Early Plan
        elif st.session_state.fishing_step == "fake_splash":
            placeholder.warning("!!splash!!")
            if st.button("REEL IN!"):
                st.error("You pulled too early! The fish got scared away.")
                st.session_state.fishing_step = "idle"
                time.sleep(2)
                st.rerun()
            
            # If they don't click, it goes back to bubbles after 2 seconds
            time.sleep(2)
            st.session_state.fishing_step = "waiting"
            st.rerun()

        # REAL SPLASH: Hook Window Plan
        elif st.session_state.fishing_step == "real_splash":
            placeholder.error("!!SPLASH!!")
            
            # The player must click this button within the 2-second sleep below
            if st.button("REEL IN!"):
                catch_chance = random.randint(1, 400)
                if catch_chance == 400: catch = "Rare Golden Fish"
                elif catch_chance > 393: catch = "Huge Bass"
                elif catch_chance > 386: catch = "Cat-fish"
                elif catch_chance > 374: catch = "Bass"
                elif catch_chance > 340: catch = "Trout"
                elif catch_chance > 300: catch = "Perch"
                elif catch_chance > 240: catch = "Carp"
                else: catch = None
                
                st.session_state.current_fish = catch
                
                if st.session_state.current_fish:
                    st.session_state.fishing_step = "battle_intro"
                    # Set HP
                    if st.session_state.current_fish in ["Trout", "Perch", "Carp"]:
                        st.session_state.fish_hp = 10
                    elif st.session_state.current_fish in ["Bass", "Cat-fish", "Huge Bass"]:
                        st.session_state.fish_hp = 15
                    elif st.session_state.current_fish == "Rare Golden Fish":
                        st.session_state.fish_hp = 20
                    
                    st.session_state.player_hp = 10
                    st.session_state.fish_dir = random.choice(["LEFT", "RIGHT", "UP"])
                else:
                    st.error("You actually just caught a worthless kelp... you threw it away.")
                    st.session_state.fishing_step = "idle"
                st.rerun()

            # "Too Late" Logic: If the code reaches here, the button wasn't clicked in time
            time.sleep(2)
            placeholder.warning("Too late! You lost the worm and the fish.")
            st.session_state.fishing_step = "idle"
            time.sleep(2)
            st.rerun()

        # BATTLE INTRO
        elif st.session_state.fishing_step == "battle_intro":
            st.success(f"is that?.... a {st.session_state.current_fish}")
            if st.button("Start Reeling In!"):
                st.session_state.fishing_step = "battle"
                st.session_state.move_start_time = time.time()
                st.rerun()

        # THE BATTLE: Move Timer Plan
        elif st.session_state.fishing_step == "battle":
            st.subheader(f"Fighting: {st.session_state.current_fish}")
            hp_col1, hp_col2 = st.columns(2)
            hp_col1.metric("Your HP", st.session_state.player_hp)
            hp_col2.metric("Fish HP", st.session_state.fish_hp)
            
            if st.session_state.current_fish == "Rare Golden Fish": reaction_limit = 1.3
            elif st.session_state.current_fish in ["Bass", "Cat-fish", "Huge Bass"]: reaction_limit = 2.0
            else: reaction_limit = 3.0

            st.info(f"The fish pulls **{st.session_state.fish_dir}**! (Quickly!)")
            b_col1, b_col2, b_col3 = st.columns(3)
            
            def execute_pull(direction):
                elapsed = time.time() - st.session_state.move_start_time
                if elapsed > reaction_limit:
                    st.session_state.player_hp -= 2
                    st.toast(f"TOO SLOW! The fish yanks the line! ({elapsed:.1f}s)", icon="⚠️")
                elif direction == st.session_state.fish_dir:
                    st.session_state.fish_hp -= 2
                    st.toast("Great reflex!", icon="✅")
                else:
                    st.session_state.player_hp -= 2
                    st.toast("Wrong direction!", icon="❌")
                    
                if st.session_state.fish_hp <= 0:
                    st.session_state.inventory[st.session_state.current_fish] = st.session_state.inventory.get(st.session_state.current_fish, 0) + 1
                    st.session_state.fishing_step = "won"
                elif st.session_state.player_hp <= 0:
                    st.session_state.fishing_step = "lost"
                else:
                    st.session_state.fish_dir = random.choice(["LEFT", "RIGHT", "UP"])
                    st.session_state.move_start_time = time.time()

            if b_col1.button("Pull LEFT"): execute_pull("LEFT"); st.rerun()
            if b_col2.button("Pull UP"): execute_pull("UP"); st.rerun()
            if b_col3.button("Pull RIGHT"): execute_pull("RIGHT"); st.rerun()

        elif st.session_state.fishing_step == "won":
            st.success(f"You caught a {st.session_state.current_fish}!")
            if st.button("Continue Fishing"):
                st.session_state.fishing_step = "idle"
                st.rerun()
        
        elif st.session_state.fishing_step == "lost":
            st.error("The line snapped! The fish got away.")
            if st.button("Continue Fishing"):
                st.session_state.fishing_step = "idle"
                st.rerun()

    with col2:
        if st.session_state.fishing_step == "idle":
            if st.button("Walk Back to the Plains"):
                st.session_state.location = "Plains"
                st.rerun()

# --- VILLAGE & FISHMONGER (Keep your existing logic for these) ---
elif st.session_state.location == "Village":
    st.title("🏘️ Village")
    st.image("https://via.placeholder.com/800x400.png?text=A+small+but+bustling+Village")
    st.write("A lively village stretches out in front of you.")
    
    col1, col2 = st.columns(2)
    if col1.button("Go to Fishmonger's House"):
        st.session_state.location = "Fishmonger"
        st.rerun()
    if col2.button("Go back to the plains"):
        with st.spinner("Walking back..."):
            time.sleep(3)
        st.session_state.location = "Plains"
        st.rerun()

elif st.session_state.location == "Fishmonger":
    st.title("🐟 Fishmonger's House")
    st.write('"What do you need, stranger?"')
    
    col1, col2, col3 = st.columns(3)
    if col1.button("Sell Fish"):
        fish_prices = {"Trout": 5, "Perch": 8, "Carp": 10, "Bass": 20, "Cat-fish": 30, "Huge Bass": 55, "Rare Golden Fish": 500}
        total_coins = 0
        fish_to_remove = []
        for item, count in st.session_state.inventory.items():
            if item in fish_prices:
                total_coins += fish_prices[item] * count
                fish_to_remove.append(item)
        if total_coins > 0:
            for f in fish_to_remove: del st.session_state.inventory[f]
            st.session_state.inventory["coins"] = st.session_state.inventory.get("coins", 0) + total_coins
            st.success(f"Sold for {total_coins} coins!")
            time.sleep(2)
            st.rerun()
        else:
            st.error("No fish to sell.")
    if col2.button("Buy Worms"): buy_worms_dialog()
    if col3.button("Back to Village"):
        st.session_state.location = "Village"
        st.rerun()