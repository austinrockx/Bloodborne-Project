"""
Bloodborne Wiki Data CLI Interface
----------------------------------
This script provides a command-line interface for interacting with Bloodborne Wiki data.
Users can list, filter, and display information about weapons, bosses, NPCs, and more.
The CLI loads data from JSON files and allows for interactive exploration and export.

Features:
- List all entries with pagination for easy browsing.
- Filter NPCs or other entities by keywords.
- Display detailed information for selected entries.
- Modular design for easy expansion.

Modules Used:
- models: Contains dataclasses for Bloodborne entities.
- data_handler: Handles loading data from JSON files.

Author: Austin Bennett
Date: 2025-05-27
"""

from models import Weapon, Armor, Boss, NPC, Item # Import data models
from data_handler import DataHandler # Import data handling utilities
from collections import Counter # Import Counter for counting occurrences in data
from colorama import Fore, Style, init # Import colorama for colored terminal output
init(autoreset=True) # Initialize colorama to reset colors automatically

def load_data():
    """
    Loads all entity data from JSON files using the DataHandler.
    Returns lists of dictionaries for weapons, armor, bosses, items, and npcs.
    """
    data_handler = DataHandler()
    weapons = data_handler.load_from_json('weapons.json')
    armor = data_handler.load_from_json('armor.json')
    bosses = data_handler.load_from_json('bosses.json')
    items = data_handler.load_from_json('items.json')
    npcs = data_handler.load_from_json('npcs.json')
    return weapons, armor, bosses, items, npcs

def show_details(results, model_cls):
    """
    Prompts the user to select an entry from the results list and displays
    detailed information using the model's display_info() method.
    """
    if not results:
        print("No results found.")
        return
    try:
        idx = int(input("Enter the number of the entry to view details: ")) - 1
        if 0 <= idx < len(results):
            obj = model_cls.from_dict(results[idx])
            obj.display_info()
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def show_statistics(weapons, armor, bosses, items, npcs):
    """
    Displays summary statistics for each entity type, with all text in red.
    """
    stats_text = (
        f"\nBloodborne Data Summary Statistics\n"
        f"{'='*30}\n"
        f"Total Weapons: {len(weapons)}\n"
    )
    if weapons:
        dmg_types = [w.get("damage_type", w.get("damage-type", "Unknown")) for w in weapons]
        most_common = Counter(dmg_types).most_common(1)
        if most_common:
            stats_text += f"Most common weapon damage type: {most_common[0][0]} ({most_common[0][1]})\n"
    stats_text += f"Total Armor Sets: {len(armor)}\n"
    stats_text += f"Total Bosses: {len(bosses)}\n"
    if bosses:
        max_hp = max(bosses, key=lambda b: int(b.get("HP", "0").replace(",", "") or 0))
        stats_text += f"Boss with highest HP: {max_hp.get('name', 'Unknown')} ({max_hp.get('HP', 'N/A')})\n"
    stats_text += f"Total Consumables: {len(items)}\n"
    stats_text += f"Total NPCs: {len(npcs)}\n"
    stats_text += f"{'='*30}\n"
    print(Fore.RED + stats_text + Style.RESET_ALL)

def export_results(results, filename, data_handler):
    """
    Exports the provided results to a JSON or CSV file.
    Prompts the user for the desired format and filename.
    """
    if not results:
        print("No data to export.")
        return
    fmt = input("Export as (json/csv)? ").strip().lower()
    if fmt == "json":
        data_handler.save_to_json(filename + ".json", results)
        print(f"Exported to {filename}.json")
    elif fmt == "csv":
        data_handler.save_to_csv(filename + ".csv", results)
        print(f"Exported to {filename}.csv")
    else:
        print("Unknown format.")

def advanced_filter(weapons, armor, bosses, items, npcs):
    """
    Allows the user to filter any entity type by a specific field and value.
    Prompts for entity type, field, and value, then displays matching results.
    """
    entity_map = {
        "weapon": (weapons, Weapon),
        "armor": (armor, Armor),
        "boss": (bosses, Boss),
        "item": (items, Item),
        "npc": (npcs, NPC)
    }
    print("Entities: weapon, armor, boss, item, npc")
    entity = input("Which entity do you want to filter? ").strip().lower()
    if entity not in entity_map:
        print("Unknown entity.")
        return

    data, model_cls = entity_map[entity]
    if not data:
        print(f"No data loaded for {entity}s.")
        return

    print("Available fields:")
    for key in data[0].keys():
        print(f"- {key}")
    field = input("Enter the field to filter by: ").strip()
    value = input("Enter the value to search for: ").strip().lower()

    results = [d for d in data if field in d and value in str(d[field]).lower()]
    if results:
        print(f"\nFound {len(results)} result(s):")
        for i, entry in enumerate(results):
            print(f"{i+1}. {entry.get('name', entry.get(field, 'No Name'))}")
        show_details(results, model_cls)
    else:
        print("No results found.")

def list_all(data, model_cls, name_key="name", page_size=10):
    """
    Lists all entries in the data with pagination.
    """
    total = len(data)
    if total == 0:
        print("No data available.")
        return
    page = 0
    while True:
        start = page * page_size
        end = min(start + page_size, total)
        for i, entry in enumerate(data[start:end], start=1+start):
            print(f"{i}. {entry.get(name_key, entry.get('set', 'No Name'))}")
        print(f"Showing {start+1}-{end} of {total}. (n: next, p: previous, entity # to view, q: quit)")
        cmd = input("Command: ").strip().lower()
        if cmd == "n" and end < total:
            page += 1
        elif cmd == "p" and page > 0:
            page -= 1
        elif cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < total:
                obj = model_cls.from_dict(data[idx])
                obj.display_info()
        elif cmd == "q":
            break
        else:
            print("Invalid command.")

def show_help():
    """
    Displays help and information about the CLI and Bloodborne entities.
    """
    help_text = (
        f"\nBloodborne CLI Help\n"
        f"\n{'='*20}"
        f"\nThis CLI lets you explore data from the Bloodborne Wiki.\n"
        f"\nYou can list, filter, and export information about:\n"
        f"- Weapons: Tools for combat, each with unique stats and effects.\n"
        f"- Armor: Protective gear with various resistances.\n"
        f"- Bosses: Major enemies with unique drops and locations.\n"
        f"- Consumables: Usable items with effects.\n"
        f"- NPCs: Non-player characters with roles in the world.\n"
        f"\nMenu Options:\n"
        f" - List All: Browse all entries with paging.\n"
        f" - Advanced Filter: Filter by any field.\n"
        f" - Export: Save your filtered results.\n"
        f" - Statistics: View summary stats for each entity type.\n"
        f" - Help: Show this help screen.\n"
        f"\n{'='*20}"
    )
    print(Fore.LIGHTMAGENTA_EX + help_text + Style.RESET_ALL)

def bosses_with_min_hp(bosses):
    """
    Lists all bosses with HP greater than a user-specified value.
    """
    try:
        min_hp = int(input("Show bosses with HP greater than: "))
        filtered = [
            b for b in bosses
            if int(b.get("HP", "0").replace(",", "") or 0) > min_hp
        ]
        stats_text = (
            f"\nBosses with HP > {min_hp}\n"
            f"{'='*30}\n"
        )
        if filtered:
            for boss in filtered:
                stats_text += f"- {boss.get('name', 'Unknown')} (HP: {boss.get('HP', 'N/A')})\n"
        else:
            stats_text += "No bosses found with HP above that value.\n"
        stats_text += f"{'='*30}\n"
        print(Fore.BLUE + stats_text + Style.RESET_ALL)
    except Exception as e:
        print(Fore.BLUE + f"Error: {e}" + Style.RESET_ALL)

def group_weapons_by_damage_type(weapons):
    """
    Groups weapons by damage type and counts them.
    """
    from collections import Counter
    dmg_types = [w.get("damage_type", w.get("damage-type", "Unknown")) for w in weapons]
    counts = Counter(dmg_types)
    stats_text = (
        f"\nWeapon Counts by Damage Type\n"
        f"{'='*30}\n"
    )
    for dtype, count in counts.items():
        stats_text += f"- {dtype}: {count}\n"
    stats_text += f"{'='*30}\n"
    print(Fore.GREEN + stats_text + Style.RESET_ALL)

def main_menu():
    """
    Main CLI loop. Presents the user with options to list, filter, display,
    and export data for all Bloodborne entities.
    """
    weapons, armor, bosses, items, npcs = load_data()
    data_handler = DataHandler()
    last_results = []
    last_model_cls = None

    menu_options = {
        "1": lambda: list_all(weapons, Weapon, "name"),
        "2": lambda: list_all(armor, Armor, "set"),
        "3": lambda: list_all(bosses, Boss, "name"),
        "4": lambda: list_all(items, Item, "name"),
        "5": lambda: list_all(npcs, NPC, "name"),
        "6": lambda: export_results(last_results, "filtered_results", data_handler),
        "7": lambda: advanced_filter(weapons, armor, bosses, items, npcs),
        "8": show_help,
        "9": lambda: show_statistics(weapons, armor, bosses, items, npcs),
        "10": lambda: bosses_with_min_hp(bosses),
        "11": lambda: group_weapons_by_damage_type(weapons),
    }

    while True:
        menu_text = (
            f"\nBloodborne Data CLI: Explore Bloodborne Entities\n"
            f"1. List All Weapons\n"
            f"2. List All Armor\n"
            f"3. List All Bosses\n"
            f"4. List All Consumables\n"
            f"5. List All NPCs\n"
            f"6. Export Last Results\n"
            f"7. Advanced Filter/Search\n"
            f"8. Help/Info\n"
            f"9. Summary Statistics\n"
            f"10. List Bosses with HP > X\n"
            f"11. Group Weapons by Damage Type\n"
            f"12. Exit\n"
        )
        print(Fore.LIGHTMAGENTA_EX + menu_text + Style.RESET_ALL)
        choice = input("Choose an option: ")

        if choice == "8":
            show_help()
        elif choice == "9":
            show_statistics(weapons, armor, bosses, items, npcs)
        elif choice == "12":
            print("Goodbye!")
            break
        elif choice in menu_options:
            result = menu_options[choice]()
            if choice in {"1", "2", "3", "4", "5", "7"} and result:
                last_results, last_model_cls = result if isinstance(result, tuple) else ([], None)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()