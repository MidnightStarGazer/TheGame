"""
Quest Tracker Module - Centralized quest progress tracking system.
Handles retrieving quest data, calculating progress, and displaying quest information.
"""

import streamlit as st
from utils.adBadgeQuest import REGISTRATION_QUEST


# --- QUEST DATA REGISTRY ---
# All quests should be registered here for dynamic access
QUEST_REGISTRY = {
    REGISTRATION_QUEST["id"]: REGISTRATION_QUEST,
    # Add more quests here as you create them
}


def get_active_quest():
    """Retrieve the currently active quest object."""
    active_quest_id = st.session_state.get("active_quest")
    if not active_quest_id:
        return None
    return QUEST_REGISTRY.get(active_quest_id)


def get_quest_progress(quest_id=None):
    """
    Calculate progress for a quest.
    Returns a dict with quest info and progress data.
    """
    if quest_id is None:
        quest_id = st.session_state.get("active_quest")
    
    if not quest_id or quest_id not in QUEST_REGISTRY:
        return None
    
    quest = QUEST_REGISTRY[quest_id]
    inventory = st.session_state.inventory
    
    progress = {
        "id": quest["id"],
        "name": quest["name"],
        "description": quest["description"],
        "reward": quest["reward"],
        "requirements": {},
        "completed": True,
    }
    
    # Calculate progress for each requirement
    for item, required_amount in quest["requirements"].items():
        current_amount = inventory.get(item, 0)
        progress["requirements"][item] = {
            "current": current_amount,
            "required": required_amount,
            "percent": min(100, int((current_amount / required_amount) * 100)) if required_amount > 0 else 0,
        }
        
        # Check if this requirement is not met
        if current_amount < required_amount:
            progress["completed"] = False
    
    return progress


def display_quest_progress(quest_id=None):
    """
    Display the quest progress in a formatted way.
    Can be called from sidebar or main area.
    """
    if quest_id is None:
        quest_id = st.session_state.get("active_quest")
    
    progress = get_quest_progress(quest_id)
    
    if not progress:
        st.info("No active quest. Head to the Guild to pick one up!")
        return
    
    # Quest Title
    st.subheader(f"📋 {progress['name']}")
    
    # Quest Description
    st.write(progress["description"])
    
    # Progress for each requirement
    st.write("**Progress:**")
    for item, data in progress["requirements"].items():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"{item}")
        with col2:
            st.progress(data["percent"] / 100, text=f"{data['percent']}%")
        with col3:
            st.caption(f"{data['current']}/{data['required']}")
    
    # Completion status
    if progress["completed"]:
        st.success(f"✅ Quest complete! Ready to turn in for **{progress['reward']}**")
    else:
        st.warning("⏳ Keep working on this quest!")


def is_quest_complete(quest_id=None):
    """Check if a quest's requirements are met."""
    progress = get_quest_progress(quest_id)
    return progress and progress["completed"]


def start_quest(quest_id):
    """Set a quest as active."""
    if quest_id in QUEST_REGISTRY:
        st.session_state.active_quest = quest_id
        from logic.state import save_game
        save_game()
        return True
    return False


def abandon_quest():
    """Abandon the current quest."""
    st.session_state.active_quest = None
    from logic.state import save_game
    save_game()
