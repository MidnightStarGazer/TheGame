import streamlit as st
import time
from logic.state import save_game
from utils.adBadgeQuest import REGISTRATION_QUEST, has_requirements, finish_quest


def show_guild():
    st.title("🏤 Adventurer's Guild")
    st.write("_The hall is filled with the clinking of armor and the low hum of experienced hunters discussing their next mark._")

    # 1. Create a Master Quest Dictionary for dynamic lookup
    # As you add more quest files, add them to this dictionary
    QUEST_DATA = {
        REGISTRATION_QUEST["id"]: REGISTRATION_QUEST
    }

    # Mira's Dialogue Box
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

        # --- PHASE 4: Dynamic Quest Tracking ---
        elif st.session_state.guild_step == "on_quest":
            # Fetch the data for whichever quest is currently active
            current_q_id = st.session_state.get("active_quest")
            quest = QUEST_DATA.get(current_q_id)

            if quest:
                st.write(f"How's the **{quest['name']}** going, **{st.session_state.player_name}**?")

                # Dynamic Progress Bars/Text
                for item, req in quest["requirements"].items():
                    current_amt = st.session_state.inventory.get(item, 0)
                    st.write(f"- {item}: {min(current_amt, req)}/{req}")

                # Check if requirements for THIS specific quest are met
                if has_requirements(st.session_state.inventory):
                    if st.button(f"Turn in {quest['name']}"):
                        st.session_state.inventory = finish_quest(st.session_state.inventory)

                        # Logic for first-time registration
                        if current_q_id == "adventurer_badge":
                            st.session_state.is_adventurer = True
                            st.session_state.guild_step = "registered"
                            st.balloons()
                            st.success("Quest Complete! You received the **Adventurer's Badge**!")

                        st.session_state.active_quest = None
                        save_game()
                        st.rerun()
                else:
                    st.write(f"_Mira waits patiently for the items required for the {quest['name']}._")
            else:
                st.error("Wait... I don't see an active quest for you. Let's talk again.")
                st.session_state.guild_step = "clerk_intro"   ##(Whyd go back to clerk intro?? Wouldnt this mean well have to input the name again??)##
                st.rerun()                                     ### No..

        # --- PHASE 5: Registered / Quest Board ---
        elif st.session_state.guild_step == "registered":
            st.write(f"Welcome back, Adventurer **{st.session_state.player_name}**!")
            st.write("Your **Adventurer's Badge** is your proof of membership. Keep it safe.")

            st.divider()
            st.subheader("📜 Quest Board")
            st.write("The board is currently empty. Check back soon for new Rank F postings!(WIP)")

    # Building exit
    if st.button("Leave Building"):
        st.session_state.location = "Village"
        st.rerun()
