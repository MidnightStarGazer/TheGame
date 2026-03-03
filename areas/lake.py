import streamlit as st
import random
import time
from logic.state import save_game

def show_lake():
    st.title("🌊 Lake Side")
    st.image("https://via.placeholder.com/800x400.png?text=Peaceful+Lakeside")
    
    st.write("""
    You arrived at the lake. The air is filled with the crisp scent of water. 
    The gentle ripples create a soothing melody. You see small fishes swimming around.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        placeholder = st.empty()
        
        # --- 1. IDLE: Heto yung simula ---
        if st.session_state.fishing_step == "idle":
            if st.button("Start Fishing", key="start_fish"):
                if st.session_state.inventory.get("Worms", 0) > 0:
                    st.session_state.inventory["Worms"] -= 1
                    if st.session_state.inventory["Worms"] == 0:
                        del st.session_state.inventory["Worms"]
                    
                    st.session_state.fishing_step = "waiting"
                    st.session_state.splash_start_time = time.time()
                    
                    # Moved save_game BEFORE rerun so it actually saves the worm count
                    save_game()
                    st.rerun()
                else:
                    st.warning("Fishing without bait seems kinda silly.... you need Worms.")

        # --- 2. WAITING: Habang nag-aabang ng kagat ---
        elif st.session_state.fishing_step == "waiting":
            placeholder.info("Bubble... Bubble... Bubble...")
            elapsed = time.time() - st.session_state.splash_start_time
            if elapsed >= 4:
                st.session_state.fishing_step = random.choice(["fake_splash", "real_splash"])
                st.session_state.splash_start_time = time.time()
                st.rerun()
            else:
                time.sleep(0.1)
                st.rerun()

        # --- 3. FAKE SPLASH: Mapang-linlang na splash ---
        elif st.session_state.fishing_step == "fake_splash":
            placeholder.warning("!!splash!!")
            if st.button("REEL IN!", key="reel_fake"):
                st.error("You pulled too early! The fish got scared away.")
                st.session_state.fishing_step = "idle"
                time.sleep(2)
                st.rerun()
            else:
                elapsed = time.time() - st.session_state.splash_start_time
                if elapsed >= 2:
                    st.session_state.fishing_step = "waiting"
                    st.session_state.splash_start_time = time.time()
                    st.rerun()
                else:
                    time.sleep(0.1)
                    st.rerun()

        # --- 4. REAL SPLASH ---
        elif st.session_state.fishing_step == "real_splash":
            placeholder.error("!!SPLASH!!")
            button_pressed = st.button("REEL IN!", key="reel_real")
            elapsed = time.time() - st.session_state.splash_start_time
            
            if button_pressed:
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
                    if st.session_state.current_fish in ["Trout", "Perch", "Carp"]: st.session_state.fish_hp = 10
                    elif st.session_state.current_fish in ["Bass", "Cat-fish", "Huge Bass"]: st.session_state.fish_hp = 15
                    elif st.session_state.current_fish == "Rare Golden Fish": st.session_state.fish_hp = 30
                    st.session_state.player_hp = 10
                    st.session_state.fish_dir = random.choice(["LEFT", "RIGHT", "UP"])
                else:
                    st.error("You actually just caught a worthless kelp... you threw it away.")
                    st.session_state.fishing_step = "idle"
                    time.sleep(2)
                st.rerun()

            elif elapsed >= 2:
                placeholder.warning("Too late! You lost the worm and the fish.")
                st.session_state.fishing_step = "idle"
                save_game()
                time.sleep(2)
                st.rerun()
            else:
                time.sleep(0.1)
                st.rerun()

        # --- 5. BATTLE LOGIC ---
        elif st.session_state.fishing_step == "battle_intro":
            st.success(f"Is that?.... a {st.session_state.current_fish}!")
            if st.button("Start Reeling In!", key="start_battle"):
                st.session_state.fishing_step = "battle"
                st.session_state.move_start_time = time.time()
                st.rerun()

        elif st.session_state.fishing_step == "battle":
            st.subheader(f"Reeling in: {st.session_state.current_fish}")
            
            # --- INSTRUCTIONS ADDED HERE ---
            st.markdown("""
            > **How to play:** The fish is trying to escape! 
            > Watch its movement and **pull in the opposite direction** to wear it down. 
            > Don't be too slow, or it'll yank the line!
            """)
            
            hp_col1, hp_col2 = st.columns(2)
            hp_col1.metric("Your HP", st.session_state.player_hp)
            hp_col2.metric("Fish HP", st.session_state.fish_hp)
            
            if st.session_state.current_fish == "Rare Golden Fish": reaction_limit = 2
            elif st.session_state.current_fish in ["Bass", "Cat-fish", "Huge Bass"]: reaction_limit = 2
            else: reaction_limit = 2.5

            st.info(f"The fish pulls **{st.session_state.fish_dir}**!")
            
            def advance_battle():
                if st.session_state.fish_hp <= 0:
                    st.session_state.inventory[st.session_state.current_fish] = st.session_state.inventory.get(st.session_state.current_fish, 0) + 1
                    st.session_state.fishing_step = "won"
                elif st.session_state.player_hp <= 0:
                    st.session_state.fishing_step = "lost"
                else:
                    st.session_state.fish_dir = random.choice(["LEFT", "RIGHT", "DIVING DOWN"])
                    st.session_state.move_start_time = time.time()

            b_col1, b_col2, b_col3 = st.columns(3)
            btn_clicked = False
            
            if b_col1.button("Pull LEFT", key="pull_l"):
                if st.session_state.fish_dir == "RIGHT":
                    st.session_state.fish_hp -= 2
                    st.toast("Great reflex!", icon="✅")
                else:
                    st.session_state.player_hp -= 2
                    st.toast("Wrong direction!", icon="❌")
                btn_clicked = True

            if b_col2.button("Pull UP", key="pull_u"):
                if st.session_state.fish_dir == "DIVING DOWN":
                    st.session_state.fish_hp -= 2
                    st.toast("Great reflex!", icon="✅")
                else:
                    st.session_state.player_hp -= 2
                    st.toast("Wrong direction!", icon="❌")
                btn_clicked = True

            if b_col3.button("Pull RIGHT", key="pull_r"):
                if st.session_state.fish_dir == "LEFT":
                    st.session_state.fish_hp -= 2
                    st.toast("Great reflex!", icon="✅")
                else:
                    st.session_state.player_hp -= 2
                    st.toast("Wrong direction!", icon="❌")
                btn_clicked = True

            if btn_clicked:
                advance_battle()
                st.rerun()
            else:
                elapsed = time.time() - st.session_state.move_start_time
                if elapsed >= reaction_limit:
                    st.session_state.player_hp -= 2
                    st.toast("TOO SLOW! The fish yanks the line!", icon="⚠️")
                    advance_battle()
                    st.rerun()
                else:
                    time.sleep(0.1)
                    st.rerun()

        elif st.session_state.fishing_step == "won":
            st.success(f"You caught a {st.session_state.current_fish}!")
            if st.button("Gather Yourself", key="won_cont"):
                st.session_state.fishing_step = "idle"
                save_game()
                st.rerun()
        
        elif st.session_state.fishing_step == "lost":
            st.error("The line snapped! The fish got away.")
            if st.button("Gather Yourself", key="lost_cont"):
                st.session_state.fishing_step = "idle"
                save_game()
                st.rerun()

    with col2:
        if st.session_state.fishing_step == "idle":
            if st.button("Walk Back to the Plains", key="go_plains"):
                st.session_state.location = "Plains"
                save_game()
                st.rerun()