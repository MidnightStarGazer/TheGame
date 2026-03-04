import streamlit as st

REGISTRATION_QUEST = {
    "id": "adventurer_badge",
    "name": "Quest: Badge of Trust",
    "requirements": {
        "Trout": 5,
        "Carp": 5,
        "Perch": 5
    },
    "reward": "Adventurer's Badge", # The specific item reward
    "description": "Catch 5 Trout, 5 Carp, and 5 Perch. Mira will trade them for your official badge."
}

def has_requirements(inventory):
    for fish, amount in REGISTRATION_QUEST["requirements"].items():
        if inventory.get(fish, 0) < amount:
            return False
    return True

def finish_quest(inventory):
    # Consume the fish
    for fish, amount in REGISTRATION_QUEST["requirements"].items():
        inventory[fish] -= amount
        if inventory[fish] <= 0:
            del inventory[fish]
    
    # ADD THE REWARD: The badge is now in the inventory!
    inventory[REGISTRATION_QUEST["reward"]] = 1
    return inventory