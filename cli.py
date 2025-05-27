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
    # Load data from JSON files using DataHandler
    data_handler = DataHandler()
    weapons = data_handler.load_from_json('weapons.json')
    armor = data_handler.load_from_json('armor.json')
    bosses = data_handler.load_from_json('bosses.json')
    items = data_handler.load_from_json('items.json')
    npcs = data_handler.load_from_json('npcs.json')
    return weapons, armor, bosses, items, npcs

# Function to search by name in a list of dictionaries
def search_by_name(data, name_key="name"):
    # Prompt user for a search query and filter data by name
    query = input("Enter name to search: ").lower()
    results = [d for d in data if query in d[name_key].lower()]
    for i, entry in enumerate(results):
        print(f"{i+1}. {entry[name_key]}")
    return results

# Function to search across all entities
def search_all(weapons, armor, bosses, items, npcs):
    query = input("Enter name to search across all entities: ").lower()
    for label, data in [("Weapon", weapons), ("Armor", armor), ("Boss", bosses), ("Item", items), ("NPC", npcs)]:
        matches = [d for d in data if query in d["name"].lower()]
        for m in matches:
            print(f"{label}: {m['name']}")

# Function to display details of a selected item
def show_details(results, model_cls):
    if not results:
        print("No results found.")
        return
    try:
        idx = int(input("Enter the number of the entry to view details: ")) - 1
        if 0 <= idx < len(results):
            # Convert dict to model instance and display info
            obj = model_cls.from_dict(results[idx])
            obj.display_info()
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

# Function to export results to JSON or CSV
def export_results(results, filename, data_handler):
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

# Function to group weapons by damage type and count them
def group_weapons_by_damage_type(weapons):
    types = [w.get("damage-type", "Unknown") for w in weapons]
    counts = Counter(types)
    for dtype, count in counts.items():
        print(f"{dtype}: {count} weapons")

# Function to display detailed information about a selected item
def main_menu():
    # Main CLI loop for user interaction
    weapons, armor, bosses, items, npcs = load_data()
    data_handler = DataHandler()
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
            results = search_by_name(weapons)
            show_details(results, Weapon)
        elif choice == "2":
            results = search_by_name(bosses)
            show_details(results, Boss)
        elif choice == "4":
            export_results(results, "filtered_results", data_handler)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()