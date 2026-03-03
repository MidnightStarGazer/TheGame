import streamlit as st
import random
import time
from logic.state import save_game

def show_village():
    st.title("🏘️ Village")
    st.image("https://via.placeholder.com/800x400.png?text=A+small+but+bustling+Village")
    
    st.write("""
    A lively village stretches out in front of you. There are people everywhere, and you notice a few interesting spots along the streets. 
    One of them is a small building with a crude sign that reads, "I BUY FISH." Other than that, there isn't much else to see yet. (WORK IN PROGRESS)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Go to Fishmonger's House"):
            st.session_state.location = "Fishmonger"
            save_game()
            st.rerun()
            
    with col2:
        if st.button("Go back to the plains"):
            st.write("""
            *As you walk along the dirt tracks, stepping away from the village, a serene calmness envelops you...*
            """)
            
            with st.spinner("Walking back to the plains..."):
                time.sleep(3) 
                random_event_chance = random.randint(1, 100)
                if random_event_chance <= 30:
                    st.warning("A bunny jumped out of the bush!")
                else:
                    st.success("You feel at ease from the peaceful atmosphere of the plains.")
                time.sleep(3) 
            
            st.session_state.location = "Plains"
            save_game()
            st.rerun()