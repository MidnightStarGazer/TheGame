import streamlit as st
import random
import time
from logic.state import save_game

def show_village():
    st.title("🏘️ Village")
    st.image("https://via.placeholder.com/800x400.png?text=A+small+but+bustling+Village")
    
    st.write("""
### The Heartbeat of Oakhaven
You stand at the **Village Center**. The quiet solitude of the wild is replaced by a symphony of village life: the rhythmic hammer of a distant blacksmith, the laughter of children, and the rich aroma of baking bread and woodsmoke.

The village breathes with a vibrant, relaxing energy—a sanctuary for those who wander.

***

### Points of Interest
* **The Salty Scale:** To your left, a modest wooden shack stands weathered by time. A wooden placard, carved with rough and hurried strokes, hangs by a rusted chain: **"I BUY FISH."** The faint scent of brine and lake-water lingers here, marking it as a humble place of trade.
* **The Great Hall:** Rising above the smaller cottages is a structure of sturdy stone and ancient oak. A magnificent, embroidered tapestry snaps in the wind, its golden thread gleaming with the words: **"Adventurer’s Guild Hall."** It stands as a beacon for those seeking glory—or just a steady job.

***
""")
    
    col1, col2, col3= st.columns(3)
    
    with col1:
        if st.button("Go to Salty Scale"):
            st.session_state.location = "Fishmonger"
            save_game()
            st.rerun()
    with col2:
        if st.button("Guild Hall"):
            st.session_state.location = "Guild"
            save_game()
            st.rerun() 

    with col3:
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

    st.divider()
    st.write("""
          Looking forward, your eyes follows the dirt road of the village
          as it leads towards the western entrance of the village
             """)
    if st.button("Follow the road"):
        st.session_state.location = "Western_Village_Gate"
        save_game()
        st.rerun()
        
