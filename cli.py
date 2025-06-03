"""
Bloodborne Wiki Data CLI Interface
----------------------------------
This script provides a command-line interface for interacting with Bloodborne Wiki data.
Users can search, filter, and display information about weapons, bosses, NPCs, and more.
The CLI loads data from JSON files and allows for interactive exploration and export.

Features:
- Search for entities by name.
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
from scraper import BloodborneScraper # Import the scraper for Bloodborne data
from collections import Counter # Import Counter for counting occurrences in data

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

def search_by_name(data, name_key="name"):
    """
    Prompts the user for a search query and returns a list of entries
    whose 'name' field contains the query (case-insensitive).
    Prints a numbered list of matching entries.
    """
    query = input("Enter name to search (leave blank to list all): ").lower()
    if not query:
        return data
    results = [d for d in data if query in d.get(name_key, "").lower()]
    for i, entry in enumerate(results):
        print(f"{i+1}. {entry.get(name_key, entry.get('set', 'No Name'))}")
    return results

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

def main_menu():
    """
    Main CLI loop. Presents the user with options to search, filter, display,
    and export data for all Bloodborne entities.
    """
    weapons, armor, bosses, items, npcs = load_data()
    data_handler = DataHandler()
    last_results = []
    last_model_cls = None

    menu_options = {
        "1": lambda: handle_search(weapons, Weapon, "name"),
        "2": lambda: handle_search(armor, Armor, "set"),
        "3": lambda: handle_search(bosses, Boss, "name"),
        "4": lambda: handle_search(items, Item, "name"),
        "5": lambda: handle_search(npcs, NPC, "name"),
        "6": lambda: export_results(last_results, "filtered_results", data_handler),
        "7": lambda: advanced_filter(weapons, armor, bosses, items, npcs),
        "8": lambda: list_all(weapons, Weapon, "name"),
        "9": lambda: list_all(armor, Armor, "set"),
        "10": lambda: list_all(bosses, Boss, "name"),
        "11": lambda: list_all(items, Item, "name"),
        "12": lambda: list_all(npcs, NPC, "name"),
    }

    while True:
        print("\nBloodborne Data CLI: Search and Explore Bloodborne Entities")
        print("1. Search Weapons")
        print("2. Search Armor")
        print("3. Search Bosses")
        print("4. Search Consumables")
        print("5. Search NPCs")
        print("6. Export Last Search Results")
        print("7. Advanced Filter/Search")
        print("8. List All Weapons")
        print("9. List All Armor")
        print("10. List All Bosses")
        print("11. List All Consumables")
        print("12. List All NPCs")
        print("13. Exit")
        choice = input("Choose an option: ")

        if choice == "13":
            print("Goodbye!")
            break
        elif choice in menu_options:
            result = menu_options[choice]()
            # Update last_results and last_model_cls if a search was performed
            if choice in {"1", "2", "3", "4", "5"} and result:
                last_results, last_model_cls = result
        else:
            print("Invalid choice.")

def handle_search(data, model_cls, name_key="name"):
    """
    Handles searching by name for a given entity type.
    Returns the search results and the model class.
    """
    results = search_by_name(data, name_key=name_key)
    show_details(results, model_cls)
    return results, model_cls

if __name__ == "__main__":
    main_menu()