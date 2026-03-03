import streamlit as st
import random
import time

def show_plains():
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
            st.rerun()

    with col3:
        if st.button("Walk south"):
            with st.spinner("Walking towards the lake in the distance..."):
                time.sleep(2)
            st.session_state.location = "Lake"
            st.rerun()