import streamlit as st
import time
from logic.state import save_game

@st.dialog("Buy Worms")
def buy_worms_dialog():
    st.write("Select the bundle size:")
    coins = st.session_state.inventory.get("coins", 0)
    col1, col2, col3 = st.columns(3)
    def purchase(cost, amount, name):
        if coins >= cost:
            st.session_state.inventory["coins"] -= cost
            st.session_state.inventory["Worms"] = st.session_state.inventory.get("Worms", 0) + amount
            st.success(f"You bought a {name} for {cost} coins.")
            time.sleep(1.5)
            save_game()
            st.rerun()
        else:
            st.error("You don't have enough coins to buy this bundle.")

    with col1:
        if st.button("Small (5 coins)"): purchase(5, 5, "Small Bundle")
    with col2:
        if st.button("Medium (10 coins)"): purchase(10, 10, "Medium Bundle")
    with col3:
        if st.button("Large (15 coins)"): purchase(15, 15, "Large Bundle")

def show_fishmonger():
   st.title("🐟 Fishmonger's House")
    
   st.write("""
    Stepping inside the cramped building, your eyes land on the fishmonger. The first thing that comes to mind is how unkempt he looks—oily and dirty, with wild hair and a scraggly beard. The air is thick with the overpowering smell of rotting fish. 
    
    As you try to avoid his gaze, you notice a large box beside him filled entirely with squirming worms. Suddenly, he locks eyes with you. 
    
    *"What do you need, stranger?"* he grunts. What do you do?
    """)
    
   col1, col2, col3 = st.columns(3)
    
   with col1:
       if st.button("Sell Fish"):
            fish_prices = {
                "Trout": 5, "Perch": 8, "Carp": 13, 
                "Bass": 15, "Cat-fish": 45, "Huge Bass": 60, "Rare Golden Fish": 500
            }

            
            # The custom dialogue for each fish type
            fish_dialogue = {
                "Trout": '"A Trout, eh? Standard fare, but it\'ll feed a family."',
                "Perch": '"Perch. Decent eating. I\'ll take it."',
                "Carp": '"Carp. A bit muddy, but someone will buy it."',
                "Bass": '"Ah, a solid Bass. Good catch, stranger."',
                "Cat-fish": '"A Cat-fish! Nasty whiskers, but sweet meat."',
                "Huge Bass": '"Whoa! A Huge Bass! Put up a fight, did it?"',
                "Rare Golden Fish": '"Oh? A Rare Golden Fish? Not bad... not bad at all. Haven\'t seen one of these in years!"'
            }
            
            total_coins = 0
            fish_to_remove = []
            
            for item, count in st.session_state.inventory.items():
                if item in fish_prices:
                    total_coins += fish_prices[item] * count
                    fish_to_remove.append(item)
            
            if total_coins > 0:
                # The Dialogue Sequence
                dialog_box = st.empty() # Creates a temporary placeholder on the screen
                
                for fish in fish_to_remove:
                    dialog_box.info(f"The fishmonger inspects the {fish}...\n\n{fish_dialogue[fish]}")
                    time.sleep(4) # Waits 4 seconds for each unique fish type you sell
                
                dialog_box.empty() # Clears the dialogue text once he is done talking
                
                # Delete the sold fish and add the coins
                for fish in fish_to_remove:
                    del st.session_state.inventory[fish]
                st.session_state.inventory["coins"] = st.session_state.inventory.get("coins", 0) + total_coins
                
                st.success(f"You sold your fish for {total_coins} coins!")
                time.sleep(2) # Give the player a second to read the success message
                save_game()
                st.rerun() # Refresh the screen to update the sidebar inventory
            else:
                st.error("You have no valuable fish to sell.")
                
   with col2:
        if st.button("Buy Worms"):
            buy_worms_dialog()
            
   with col3:
        if st.button("Back to Village"):
            st.session_state.location = "Village"
            st.rerun()




