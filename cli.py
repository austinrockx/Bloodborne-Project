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
    query = input("Enter name to search: ").lower()
    results = [d for d in data if query in d.get(name_key, "").lower()]
    for i, entry in enumerate(results):
        print(f"{i+1}. {entry.get(name_key, '')}")
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

def main_menu():
    """
    Main CLI loop. Presents the user with options to search, filter, display,
    and export data for all Bloodborne entities.
    """
    weapons, armor, bosses, items, npcs = load_data()
    data_handler = DataHandler()
    last_results = []
    last_model_cls = None

    while True:
        print("\nBloodborne Data CLI")
        print("1. Search Weapons")
        print("2. Search Armor")
        print("3. Search Bosses")
        print("4. Search Consumables")
        print("5. Search NPCs")
        print("6. Export Last Search Results")
        print("7. Advanced Filter/Search")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            last_results = search_by_name(weapons)
            last_model_cls = Weapon
            show_details(last_results, Weapon)
        elif choice == "2":
            last_results = search_by_name(armor)
            last_model_cls = Armor
            show_details(last_results, Armor)
        elif choice == "3":
            last_results = search_by_name(bosses)
            last_model_cls = Boss
            show_details(last_results, Boss)
        elif choice == "4":
            last_results = search_by_name(items)
            last_model_cls = Item
            show_details(last_results, Item)
        elif choice == "5":
            last_results = search_by_name(npcs)
            last_model_cls = NPC
            show_details(last_results, NPC)
        elif choice == "6":
            if last_results:
                export_results(last_results, "filtered_results", data_handler)
            else:
                print("No previous search results to export.")
        elif choice == "7":
            advanced_filter(weapons, armor, bosses, items, npcs)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()