import streamlit as st
import random
import time

def show_lake():
    st.title("🌊 Lake Side")
    st.image("https://via.placeholder.com/800x400.png?text=Peaceful+Lakeside")
    
    st.write("""
    You arrived at the lake. The air is filled with the crisp scent of water mingled with the earthy aroma of nearby foliage. 
    The gentle ripples of the water create a soothing melody, punctuated by the occasional call of distant birds.
    
    You gaze at the waters and see small fishes swimming around.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        placeholder = st.empty()
        
        # IDLE
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

        # WAITING
        elif st.session_state.fishing_step == "waiting":
            placeholder.info("Bubble... Bubble... Bubble...")
            time.sleep(4)
            st.session_state.fishing_step = random.choice(["fake_splash", "real_splash"])
            st.rerun()

        # FAKE SPLASH
        elif st.session_state.fishing_step == "fake_splash":
            placeholder.warning("!!splash!!")
            if st.button("REEL IN!"):
                st.error("You pulled too early! The fish got scared away.")
                st.session_state.fishing_step = "idle"
                time.sleep(2)
                st.rerun()
            time.sleep(2)
            st.session_state.fishing_step = "waiting"
            st.rerun()

        # REAL SPLASH
        elif st.session_state.fishing_step == "real_splash":
            placeholder.error("!!SPLASH!!")
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
                    if st.session_state.current_fish in ["Trout", "Perch", "Carp"]: st.session_state.fish_hp = 10
                    elif st.session_state.current_fish in ["Bass", "Cat-fish", "Huge Bass"]: st.session_state.fish_hp = 15
                    elif st.session_state.current_fish == "Rare Golden Fish": st.session_state.fish_hp = 20
                    st.session_state.player_hp = 10
                    st.session_state.fish_dir = random.choice(["LEFT", "RIGHT", "UP"])
                else:
                    st.error("You actually just caught a worthless kelp... you threw it away.")
                    st.session_state.fishing_step = "idle"
                st.rerun()

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

        # BATTLE
        elif st.session_state.fishing_step == "battle":
            st.subheader(f"Fighting: {st.session_state.current_fish}")
            hp_col1, hp_col2 = st.columns(2)
            hp_col1.metric("Your HP", st.session_state.player_hp)
            hp_col2.metric("Fish HP", st.session_state.fish_hp)
            
            if st.session_state.current_fish == "Rare Golden Fish": reaction_limit = 1.5
            elif st.session_state.current_fish in ["Bass", "Cat-fish", "Huge Bass"]: reaction_limit = 2.5
            else: reaction_limit = 3.5

            st.info(f"The fish pulls **{st.session_state.fish_dir}**!")
            
            def advance_battle():
                if st.session_state.fish_hp <= 0:
                    st.session_state.inventory[st.session_state.current_fish] = st.session_state.inventory.get(st.session_state.current_fish, 0) + 1
                    st.session_state.fishing_step = "won"
                elif st.session_state.player_hp <= 0:
                    st.session_state.fishing_step = "lost"
                else:
                    st.session_state.fish_dir = random.choice(["LEFT", "RIGHT", "UP"])
                    st.session_state.move_start_time = time.time()

            b_col1, b_col2, b_col3 = st.columns(3)
            
            if b_col1.button("Pull LEFT"):
                if "LEFT" == st.session_state.fish_dir: st.session_state.fish_hp -= 2; st.toast("Great reflex!", icon="✅")
                else: st.session_state.player_hp -= 2; st.toast("Wrong direction!", icon="❌")
                advance_battle()
                st.rerun()
                
            if b_col2.button("Pull UP"):
                if "UP" == st.session_state.fish_dir: st.session_state.fish_hp -= 2; st.toast("Great reflex!", icon="✅")
                else: st.session_state.player_hp -= 2; st.toast("Wrong direction!", icon="❌")
                advance_battle()
                st.rerun()
                
            if b_col3.button("Pull RIGHT"):
                if "RIGHT" == st.session_state.fish_dir: st.session_state.fish_hp -= 2; st.toast("Great reflex!", icon="✅")
                else: st.session_state.player_hp -= 2; st.toast("Wrong direction!", icon="❌")
                advance_battle()
                st.rerun()

            time.sleep(reaction_limit) 
            st.session_state.player_hp -= 2
            st.toast("TOO SLOW! The fish yanks the line!", icon="⚠️")
            advance_battle()
            st.rerun()

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