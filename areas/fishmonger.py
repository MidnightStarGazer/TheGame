import streamlit as st
import time

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
    Stepping inside the cramped building, your eyes land on the fishmonger. The first thing that comes to mind is how unkempt he looks—oily and dirty, with wild hair and a scraggly beard. 
    
    *"What do you need, stranger?"* he grunts. What do you do?
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Sell Fish"):
            fish_prices = {
                "Trout": 5, "Perch": 8, "Carp": 13, 
                "Bass": 15, "Cat-fish": 45, "Huge Bass": 60, "Rare Golden Fish": 500
            }
            
            total_coins = 0
            fish_to_remove = []
            
            for item, count in st.session_state.inventory.items():
                if item in fish_prices:
                    total_coins += fish_prices[item] * count
                    fish_to_remove.append(item)
            
            if total_coins > 0:
                for fish in fish_to_remove:
                    del st.session_state.inventory[fish]
                st.session_state.inventory["coins"] = st.session_state.inventory.get("coins", 0) + total_coins
                
                st.success(f"You sold your fish for {total_coins} coins!")
                time.sleep(2) 
                st.rerun() 
            else:
                st.error("You have no valuable fish to sell.")
                
    with col2:
        if st.button("Buy Worms"):
            buy_worms_dialog()
            
    with col3:
        if st.button("Back to Village"):
            st.session_state.location = "Village"
            st.rerun()