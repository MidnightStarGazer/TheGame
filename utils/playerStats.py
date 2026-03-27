"""
Player Stats Module - Display and manage character attributes and equipment.
"""

import streamlit as st
from logic.state import save_game


def get_weapons_from_inventory():
    """Extract weapon items from inventory."""
    # Define weapon types (you can expand this)
    weapon_types = ["Sword", "Axe", "Spear", "Dagger"]
    weapons = {}
    for item, count in st.session_state.inventory.items():
        if any(weapon in item for weapon in weapon_types):
            weapons[item] = count
    return weapons


def get_armor_from_inventory():
    """Extract armor items from inventory."""
    # Define armor types (you can expand this)
    armor_types = ["Helmet", "Chestplate", "Leggings", "Boots"]
    armors = {}
    for item, count in st.session_state.inventory.items():
        if any(armor in item for armor in armor_types):
            armors[item] = count
    return armors


def get_weapon_bonus(weapon_name):
    """Return damage bonus for a weapon."""
    weapon_bonuses = {
        "Sword": 5,
        "Axe": 8,
        "Spear": 6,
        "Dagger": 3,
    }
    for weapon, bonus in weapon_bonuses.items():
        if weapon in weapon_name:
            return bonus
    return 0


def get_armor_bonus(armor_name):
    """Return armor value for armor piece."""
    armor_bonuses = {
        "Helmet": 2,
        "Chestplate": 5,
        "Leggings": 3,
        "Boots": 1,
    }
    for armor, bonus in armor_bonuses.items():
        if armor in armor_name:
            return bonus
    return 0


def display_character_status():
    """Display character status with equipment management."""
    st.subheader(" ''''' ")


    # Character Name and HP
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {st.session_state.player_name or 'Unknown'}")
    with col2:
        st.write(f"**HP:** {st.session_state.player_hp}")

    st.divider()

    # Armor/Defense
    current_armor = st.session_state.get("equipped_armor", None)
    armor_value = get_armor_bonus(current_armor) if current_armor else 0
    st.write(f"**Armor:** {armor_value}")

    st.divider()

    # Damage (Base + Bonus from weapon)
    base_damage = 10
    current_weapon = st.session_state.get("equipped_weapon", None)
    weapon_bonus = get_weapon_bonus(current_weapon) if current_weapon else 0
    total_damage = base_damage + weapon_bonus

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Base Damage:** {base_damage}")
    with col2:
        st.write(f"**Weapon Bonus:** +{weapon_bonus}")
    with col3:
        st.write(f"**Total Damage:** {total_damage}")

    st.divider()

    # Equipment Section
    st.subheader("🛠️ Equipment")

    # Weapon Selection
    st.write("**Weapon:**")
    if current_weapon:
        st.caption(f"Currently equipped: {current_weapon}")
    else:
        st.caption("No weapon equipped")

    if st.button("⚔️ Select Weapon"):
        st.session_state.selecting_weapon = True
        st.rerun()

    # Armor Selection
    st.write("**Armor:**")
    if current_armor:
        st.caption(f"Currently equipped: {current_armor}")
    else:
        st.caption("No armor equipped")

    if st.button("🛡️ Select Armor"):
        st.session_state.selecting_armor = True
        st.rerun()

    st.divider()



def show_weapon_selection():
    """Popup to select a weapon from inventory."""
    st.subheader("Select a Weapon")

    weapons = get_weapons_from_inventory()

    if not weapons:
        st.warning("You have no weapons in your inventory!")
    else:
        for weapon, count in weapons.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{weapon} (Bonus: +{get_weapon_bonus(weapon)})")
            with col2:
                st.caption(f"x{count}")
            with col3:
                if st.button("Equip", key=f"equip_weapon_{weapon}"):
                    st.session_state.equipped_weapon = weapon
                    st.session_state.selecting_weapon = False
                    save_game()
                    st.rerun()

    if st.button("Cancel"):
        st.session_state.selecting_weapon = False
        st.rerun()


def show_armor_selection():
    """Popup to select armor from inventory."""
    st.subheader("Select Armor")

    armors = get_armor_from_inventory()

    if not armors:
        st.warning("You have no armor in your inventory!")
    else:
        for armor, count in armors.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{armor} (Defense: +{get_armor_bonus(armor)})")
            with col2:
                st.caption(f"x{count}")
            with col3:
                if st.button("Equip", key=f"equip_armor_{armor}"):
                    st.session_state.equipped_armor = armor
                    st.session_state.selecting_armor = False
                    save_game()
                    st.rerun()

    if st.button("Cancel"):
        st.session_state.selecting_armor = False
        st.rerun()
