import streamlit as st
import random
import time
from logic.state import save_game

def show_lake():
    st.title("🌊 Lake Side")
    st.image("https://via.placeholder.com/800x400.png?text=Peaceful+Lakeside")
    
    st.write("""
As the tall grasses of the plains finally yield to smooth, sun-warmed stones, the world opens up into a breathtaking vista. Before you lies the **Great Lake**, a vast expanse of liquid sapphire that seems to breathe with the very rhythm of the earth.

The air here is sharp and cool, carrying the pristine scent of fresh water and damp moss. The restless wind of the plains dies down here, replaced by the gentle, rhythmic lapping of ripples against the shore—a soothing melody that clears the mind of all worry.

* **The water is crystal clear, revealing a vibrant underwater world. Schools of silver-scaled fish dart through forests of swaying lake-grass, their movements synchronized and fluid.
* **Further out, where the light fades into shadow, the water turns a mysterious, ink-black blue. Great ripples occasionally break the surface, hinting at the massive creatures that dwell in the silent depths.

""")
    
    col1, col2 = st.columns(2)
    
    with col1:
        placeholder = st.empty()
        
        # Helper function to handle worm loss to keep code clean
        def lose_worm():
            if "Worms" in st.session_state.inventory:
                st.session_state.inventory["Worms"] -= 1
                if st.session_state.inventory["Worms"] <= 0:
                    del st.session_state.inventory["Worms"]
                save_game()

        # --- 1. IDLE ---
        if st.session_state.fishing_step == "idle":
            if st.button("Start Fishing", key="start_fish"):
                # Now we just CHECK for worms, but don't subtract them yet
                if st.session_state.inventory.get("Worms", 0) > 0:
                    st.session_state.fishing_step = "waiting"
                    st.session_state.splash_start_time = time.time()
                    st.rerun()
                else:
                    st.warning("Fishing without bait seems kinda silly.... you need Worms.")

        # --- 2. WAITING ---
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

        # --- 3. FAKE SPLASH (Worm is safe here) ---
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
                # Catch Logic - Adjusted probabilities
                if catch_chance == 400: catch = "Rare Golden Fish"  # 1/400 (0.25%)
                elif catch_chance > 394: catch = "Huge Bass"  # 5/400 (1.25%)
                elif catch_chance > 389: catch = "Cat-fish"  # 5/400 (1.25%)
                elif catch_chance > 339: catch = "Bass"  # 50/400 (12.5%)
                elif catch_chance > 239: catch = "Trout"  # 100/400 (25%)
                elif catch_chance > 139: catch = "Perch"  # 100/400 (25%)
                elif catch_chance > 39: catch = "Carp"  # 100/400 (25%)
                else: catch = None  # 39/400 - Kelp

                
                st.session_state.current_fish = catch
                
                if st.session_state.current_fish:
                    # FISH HOOKED: Consume the worm now
                    lose_worm()
                    st.session_state.fishing_step = "battle_intro"
                    
                    if st.session_state.current_fish in ["Trout", "Perch", "Carp"]: st.session_state.fish_hp = 10
                    elif st.session_state.current_fish in ["Bass", "Cat-fish", "Huge Bass"]: st.session_state.fish_hp = 15
                    elif st.session_state.current_fish == "Rare Golden Fish": st.session_state.fish_hp = 30
                    
                    st.session_state.player_hp = 10
                    st.session_state.fish_dir = random.choice(["LEFT", "RIGHT", "UP"])
                else:
                    # KELP CAUGHT: Worm is safe!
                    st.error("You actually just caught a worthless kelp so you threw it away..You also lost your bait.")
                    st.session_state.fishing_step = "idle"
                    lose_worm()
                    time.sleep(2)
                st.rerun()

            elif elapsed >= 2:
                # TOO LATE: The fish ate the worm and left
                placeholder.warning("Too late! You lost the worm and the fish.")
                lose_worm() # Worm consumed
                st.session_state.fishing_step = "idle"
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

            st.info(f"The fish went.. **{st.session_state.fish_dir}**!")
            
            def advance_battle():
                if st.session_state.fish_hp <= 0:
                    st.session_state.inventory[st.session_state.current_fish] = st.session_state.inventory.get(st.session_state.current_fish, 0) + 1
                    st.session_state.fishing_step = "won"
                    save_game()
                elif st.session_state.player_hp <= 0:
                    st.session_state.fishing_step = "lost"
                else:
                    st.session_state.fish_dir = random.choice(["LEFT!", "RIGHT!", "DIVING DOWN!"])
                    st.session_state.move_start_time = time.time()

            b_col1, b_col2, b_col3 = st.columns(3)
            btn_clicked = False
            
            if b_col1.button("Pull LEFT", key="pull_l"):
                if st.session_state.fish_dir == "RIGHT!":
                    st.session_state.fish_hp -= 2
                    st.toast("Great reflex!", icon="✅")
                else:
                    st.session_state.player_hp -= 2
                    st.toast("Wrong direction!", icon="❌")
                btn_clicked = True

            if b_col2.button("Pull UP", key="pull_u"):
                if st.session_state.fish_dir == "DIVING DOWN!":
                    st.session_state.fish_hp -= 2
                    st.toast("Great reflex!", icon="✅")
                else:
                    st.session_state.player_hp -= 2
                    st.toast("Wrong direction!", icon="❌")
                btn_clicked = True

            if b_col3.button("Pull RIGHT", key="pull_r"):
                if st.session_state.fish_dir == "LEFT!":
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