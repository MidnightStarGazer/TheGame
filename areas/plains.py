import streamlit as st
import random
import time
from logic.state import save_game

def show_plains():
    st.title("🌾 Vast Plains")
    st.image("https://via.placeholder.com/800x400.png?text=Vast+Plains+Landscape") 
    
    st.write("""
   ### A Sea of Emerald
You stand at the heart of an endless emerald ocean. The **Whispering Plains** stretch toward the horizon in every direction, the tall grass swaying in a synchronized dance as a gentle, cool breeze whistles past your ears. 

The sun hangs heavy and golden in the sky, its warmth wrapping around you like a familiar blanket. You take a deep breath, and the air tastes of wild clover and sun-drenched earth. 

***

### Surroundings
* **To the South:** The light catches a shimmering ribbon of blue in the distance—the **Great Lake** glimmers like a fallen sapphire, promising cool waters and a quiet place to think.
* **At Your Feet:** You notice a cluster of ancient, moss-covered stones. The soil at their base is dark and damp, unnaturally cool despite the midday heat. 

*Something stirs beneath the surface...*""")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Search the rocks"):
            with st.spinner("Searching the rocks..."):
                time.sleep(2) 
                
            if random.random() > 0.5:
                worms = random.randint(1, 5)
                st.session_state.inventory["Worms"] = st.session_state.inventory.get("Worms", 0) + worms
                st.success(f"You found {worms} worms!")
                save_game()
            else:
                st.info("You didn't find anything.")
                
    with col2:
        if st.button("Follow the dirt track"):
            with st.spinner("Walking along the tracks..."):
                time.sleep(3)
                
                random_event_chance = random.randint(1, 100)
                if random_event_chance <= 30:
                    random_event = random.randint(1, 3)
                    if random_event == 1:
                        st.info("You see that same eagle from before hunting a bunny from afar. But then again, it does not really concern you.")
                    elif random_event == 2:
                        st.warning("A bunny jumped out of the bush as you passed by, your heart almost jumped out of your chest!")
                    else:
                        st.success("You spot a group of deer grazing peacefully.")
                else:
                    st.success("You feel at ease from the peaceful atmosphere of the plains. And finally, you saw something in the distance...")
                
                time.sleep(5)
            st.session_state.location = "Village"
            save_game()
            st.rerun()

    with col3:
        if st.button("Walk south"):
            with st.spinner("Walking towards the lake in the distance..."):
                time.sleep(2)
            st.session_state.location = "Lake"
            save_game()
            st.rerun()