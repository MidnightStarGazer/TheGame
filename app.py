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
    username = st.text_input("Username(ajtd)")
    password = st.text_input("Password(ajtd2)", type="password")
    if st.button("Submit"):
        if username == "ajtd" and password == "ajtd2":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect credentials.")

#Dialogs For about
@st.dialog("About The Game")
def about_dialog():
    st.subheader("What the app does (use-case)")
    st.write("""
    This application is a work in progress **Text-Based Adventure RPG** set in the world of Arteka(wip). 
    It provides an interactive UI flow where players can explore regions(wip), manage 
    character equipment(wip), and engage in fishing minigames and more(wip).
    """)

    st.subheader("Who the target user is")
    st.write("""
    The target users are **casual gamers** and fans of tabletop-style text based RPGs 
    who enjoy narrative-driven text base adventures experiences.
    """)

    st.subheader("Inputs and Outputs")
    st.write("**Inputs:**")
    st.write("- **Text Input:** Character naming and login credentials.")
    st.write("- **Interactions:** Button clicks for navigation and real-time fishing battles.")
    
    st.write("**Outputs:**")
    st.write("- **Visual Progress:** Quest progress bars and health metrics.")
    st.write("- **Narrative:** Dynamic text descriptions based on player location and actions.")

    st.write("**Ui components**")
    st.write("""
    - st.title: used for main headers for locations and menus 
    - st.subheader: used for section headings like "Your Items", "Quest Progress", and "Equipment".
    - st.write: used for storytelling, displaying item lists, and providing general game information throughout the app.
    - st.markdown: used for styled flavor text, centered headers, and instructional blocks in the battle system.(can be seen in the instructions tutorial on fish battle)
    - st.caption: used for secondary labels for item counts, rank status, and equipment details.
    - st.divider: used for horizontal lines to separate UI sections in the sidebar and NPC menus.
    - st.columns: used to organize buttons, stats, and requirements into side-by-side layouts.
    - st.sidebar: used as the primary container for the game menu, navigation, and character status.
    - st.button: used for all interactive choices, including movement, fishing, equipment management, and menu navigation.
    - st.text_input: used for entering the player's name and login credentials.
    - st.radio: used for the main navigation menu within the sidebar.
    - st.success: used to signal positive outcomes like finding worms, catching fish, or completing quests.
    - st.info: used for providing general guidance, NPC dialogue, and bubble cues during fishing.
    - st.warning: used for cautionary feedback like missing bait, early reels, or quit confirmations.
    - st.error: used for failure messages like line snaps, wrong login details, or having no fish to sell.
    - st.toast: used for quick pop-up alerts during fishing battles and to confirm saving progress.
    - st.spinner: used to show loading animations while "searching" rocks or "walking" between areas.
    - st.balloons: used to trigger a celebration animation when the player completes the registration quest.(doesn't work properly in my phone tbh)
    - st.progress: used to visualize the percentage of completion for quest requirements. (this are the bar in thw quest tracker)
    - st.metric: used to display numerical HP values for both the player and fish during the fishing minigame.
    - st.dialog: used for modal pop-up windows like the login screen and the "Buy Worms" menu.
    - st.chat_message: used to create a dedicated character message block for Mira at the guild counter.
    - st.empty: used as a dynamic placeholder for updating dialogue and fishing cues without a full page refresh.
    """)
 
#Dialogs Tutorial
@st.dialog("Game Hints")
def hints_dialog():
    st.subheader("What the app does (use-case)")
    st.write("""
    - At the spawn point(Plains), there's a rock, search it again and again maybe it'll help with the fishing.
    - When fishing only watch out for the real !!SPLASH!! 
    - When fighting to reel in the fish.. pull it to the opposite direction it's going.
    - You can sell the fish at the village to the fishmonger
    - Check the guild!! Maybe you'll meet someone interesting!
    """)
    


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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("START GAME ->", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
    with col2:
        # This button now clears everything AND enters the game
        if st.button("NEW GAME", use_container_width=True, type="primary"):
            reset_game()
    with col3:
        #For about shit
        if st.button("ℹ️ ABOUT", use_container_width=True):
            about_dialog()
    with col4:
        #For hint
        if st.button("☝️🤓 Hints/Guide!", use_container_width=True):
            hints_dialog()

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
        show_forest()    """)

    st.subheader("Who the target user is")
    st.write("""
    The target users are **casual gamers** and fans of tabletop-style text based RPGs 
    who enjoy narrative-driven text base adventures experiences.
    """)

    st.subheader("Inputs and Outputs")
    st.write("**Inputs:**")
    st.write("- **Text Input:** Character naming and login credentials.")
    st.write("- **Interactions:** Button clicks for navigation and real-time fishing battles.")
    
    st.write("**Outputs:**")
    st.write("- **Visual Progress:** Quest progress bars and health metrics.")
    st.write("- **Narrative:** Dynamic text descriptions based on player location and actions.")

    st.write("**Ui components**")
    st.write("""
    - st.title: used for main headers for locations and menus 
    - st.subheader: used for section headings like "Your Items", "Quest Progress", and "Equipment".
    - st.write: used for storytelling, displaying item lists, and providing general game information throughout the app.
    - st.markdown: used for styled flavor text, centered headers, and instructional blocks in the battle system.(can be seen in the instructions tutorial on fish battle)
    - st.caption: used for secondary labels for item counts, rank status, and equipment details.
    - st.divider: used for horizontal lines to separate UI sections in the sidebar and NPC menus.
    - st.columns: used to organize buttons, stats, and requirements into side-by-side layouts.
    - st.sidebar: used as the primary container for the game menu, navigation, and character status.
    - st.button: used for all interactive choices, including movement, fishing, equipment management, and menu navigation.
    - st.text_input: used for entering the player's name and login credentials.
    - st.radio: used for the main navigation menu within the sidebar.
    - st.success: used to signal positive outcomes like finding worms, catching fish, or completing quests.
    - st.info: used for providing general guidance, NPC dialogue, and bubble cues during fishing.
    - st.warning: used for cautionary feedback like missing bait, early reels, or quit confirmations.
    - st.error: used for failure messages like line snaps, wrong login details, or having no fish to sell.
    - st.toast: used for quick pop-up alerts during fishing battles and to confirm saving progress.
    - st.spinner: used to show loading animations while "searching" rocks or "walking" between areas.
    - st.balloons: used to trigger a celebration animation when the player completes the registration quest.(doesn't work properly in my phone tbh)
    - st.progress: used to visualize the percentage of completion for quest requirements. (this are the bar in thw quest tracker)
    - st.metric: used to display numerical HP values for both the player and fish during the fishing minigame.
    - st.dialog: used for modal pop-up windows like the login screen and the "Buy Worms" menu.
    - st.chat_message: used to create a dedicated character message block for Mira at the guild counter.
    - st.empty: used as a dynamic placeholder for updating dialogue and fishing cues without a full page refresh.
    """)
 
#Dialogs Tutorial
@st.dialog("Game Hints")
def hints_dialog():
    st.subheader("What the app does (use-case)")
    st.write("""
    - At the spawn point(Plains), there's a rock, search it again and again maybe it'll help with the fishing.
    - When fishing only watch out for the real !!SPLASH!! 
    - When fighting to reel in the fish.. pull it to the opposite direction it's going.
    - You can sell the fish at the village to the fishmonger
    - Check the guild!! Maybe you'll meet someone interesting!
    """)
    


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
            else:h
                display_character_status()
    
    # --- GAME MENU SIDEBAR THINGY ---
    else:
        with st.sidebar:
            st.title("⚙️ Game Menu")
            menu_choice = st.radio8hh("Navigation", ["Inventory", "Quest Progress", "Quit to Menu", "Logout"])
            
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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("START GAME ->", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
    with col2:
        # This button now clears everything AND enters the game
        if st.button("NEW GAME", use_container_width=True, type="primary"):
            reset_game()
    with col3:
        #For about shit
        if st.button("ℹ️ ABOUT", use_container_width=True):
            about_dialog()
    with col4:
        #For hint
        if st.button("☝️🤓 Hints/Guide!", use_container_width=True):
            hints_dialog()

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
