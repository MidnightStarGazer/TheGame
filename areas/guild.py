import streamlit as st
import time
from logic.state import save_game
from utils.adBadgeQuest import REGISTRATION_QUEST, has_requirements, finish_quest
from utils.quest_tracker import get_active_quest, is_quest_complete, start_quest


def show_guild():
    st.title("🏤 Adventurer's Guild")
    st.write("_The hall is filled with the clinking of armor and the low hum of experienced hunters discussing their next mark._")

    # --- GUILD ENVIRONMENT (Not at counter) ---
    if not st.session_state.at_guild_counter:
        st.write("""
        You stand in the main hall of the guild. Adventurers of all ranks mill about, discussing their exploits. 
        At the far end of the hall, you see a counter with a woman behind it - likely the guild clerk.
        
        Various quests are pinned to a board on the wall, and the atmosphere buzzes with activity.
        """)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚶 Approach the Counter"):
                st.session_state.at_guild_counter = True
                save_game()
                st.rerun()

        with col2:
            if st.button("Leave Building"):
                st.session_state.location = "Village"
                st.rerun()

    # --- AT THE COUNTER (Mira's Dialogue) ---
    else:
        with st.chat_message("assistant", avatar="👩‍💼"):

            # --- PHASE 1: Name Entry ---
            if st.session_state.guild_step == "intro":
                st.write("Oh! It seems like this is your first time coming here! What's your name?")
                st.markdown("> *'Huh... you don't really remember your name... let's make one then.'*")

                p_name = st.text_input("Enter a name:", key="new_name_input")
                if st.button("Confirm Name"):
                    if p_name:
                        st.session_state.player_name = p_name
                        st.session_state.guild_step = "clerk_intro"
                        save_game()
                        st.rerun()
                    else:
                        st.warning("You need a name to register, traveler.")

            # --- PHASE 2: Registration Offer ---
            elif st.session_state.guild_step == "clerk_intro":
                st.write(f"Nice to meet you! My name is **Mira**. I handle the desk here in the Guild.")
                st.write("Since you're new here, I'll assume you're here to register as an adventurer?")

                col1, col2 = st.columns(2)
                if col1.button("Yes! I want to join."):
                    st.session_state.guild_step = "explanation"
                    st.rerun()
                if col2.button("No, just looking around."):
                    st.write("Mira smiles. 'No problem! Feel free to soak in the atmosphere.'")

            # --- PHASE 3: Quest Explanation ---
            elif st.session_state.guild_step == "explanation":
                st.write("Great! But I can't just give a badge to anyone. You need to prove you have the basics down.")
                st.write("A true adventurer in **Arteka** must be able to provide for themselves.")

                # Display current quest details
                st.info(f"**Quest:** {REGISTRATION_QUEST['name']}\n\n{REGISTRATION_QUEST['description']}")

                st.write("Mira looks at you expectantly. 'So, do you accept?'")

                q_col1, q_col2 = st.columns(2)
                if q_col1.button("Accept Quest"):
                    st.session_state.guild_step = "on_quest"
                    st.session_state.active_quest = REGISTRATION_QUEST["id"]
                    save_game()
                    st.rerun()

                if q_col2.button("Not now"):
                    st.session_state.guild_step = "clerk_intro"
                    st.rerun()

            # --- PHASE 4: Quest Active Message ---
            elif st.session_state.guild_step == "on_quest":
                quest = get_active_quest()

                if quest:
                    st.write(f"Good luck with the **{quest['name']}**, **{st.session_state.player_name}**!")
                    st.write(f"_Mira smiles encouragingly._")
                    st.info("📱 Check your **Quest Progress** in the Game Menu sidebar to track your progress!")

                    # Check if quest is complete and ready to turn in
                    if is_quest_complete():
                        if st.button(f"Turn in {quest['name']}"):
                            st.session_state.inventory = finish_quest(st.session_state.inventory)

                            # Logic for first-time registration
                            if quest["id"] == "adventurer_badge":
                                st.session_state.is_adventurer = True
                                st.session_state.guild_step = "registered"
                                st.balloons()
                                st.success("Quest Complete! You received the **Adventurer's Badge**!")

                            st.session_state.active_quest = None
                            save_game()
                            st.rerun()
                else:
                    st.error("Wait... I don't see an active quest for you. Let's talk again.")
                    st.session_state.guild_step = "clerk_intro"
                    st.rerun()

            # --- PHASE 5: Registered / Quest Board ---
            elif st.session_state.guild_step == "registered":
                st.write(f"Welcome back, Adventurer **{st.session_state.player_name}**!")
                st.write("Your **Adventurer's Badge** is your proof of membership. Keep it safe.")

                st.divider()
                st.subheader("📜 Quest Board")
                st.write("The board is currently empty. Check back soon for new Rank F postings!(WIP)")

        # Leave the counter button
        st.divider()
        if st.button("◀️ Leave the Counter"):
            st.session_state.at_guild_counter = False
            save_game()
            st.rerun()
