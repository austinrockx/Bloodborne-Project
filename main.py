"""
Bloodborne Wiki Data Scraper - Main Script
------------------------------------------
This script orchestrates the scraping and saving of Bloodborne Wiki data. 
It utilizes the BloodborneScraper to extract data on weapons, armor, bosses, 
items, and NPCs, and the DataHandler to store the information in JSON and CSV files.

Features:
- Initializes the scraper and data handler modules.
- Scrapes various types of data from the Bloodborne Wiki.
- Saves extracted data in both JSON and CSV formats.
- Implements exception handling to manage potential errors.

Modules Used:
- requests: For HTTP requests to fetch web content.
- BeautifulSoup (bs4): For HTML parsing and data extraction.
- json: For saving structured data in JSON format.
- csv: For storing data in CSV format.
- os: For file operations.

Custom Modules:
- scraper: Contains the BloodborneScraper class responsible for fetching data.
- data_handler: Handles saving and organizing the scraped data.

Author: Austin Bennett
Date: 2025-03-13
"""


import requests # A Python library for making HTTP requests to fetch web content.
from bs4 import BeautifulSoup # Part of the bs4 library, used for parsing HTML and extracting data from web pages.
import json # A module for working with JSON data, allowing you to save and load structured data.
import csv # A module for reading and writing CSV (Comma-Separated Values) files.
import os # Provides functions for interacting with the operating system, such as file handling.

# Import your custom modules
from scraper import BloodborneScraper # Custom module for scraping data from the Bloodborne Wiki.
from data_handler import DataHandler  # Custom module for saving the scraped data into JSON and CSV formats.
from models import Weapon, Armor, Boss, NPC, Item # Custom data models for representing different entities in the game.

# Main function to orchestrate the scraping and saving of data
def main():
    # Create instances of your scraper and data handler
    scraper = BloodborneScraper()
    data_handler = DataHandler()

    # Example usage: Scrape data and save it to JSON and CSV
    try:
        # Scrape data
        weapons_data = scraper.scrape_weapons()
        armor_data = scraper.scrape_armor()
        bosses_data = scraper.scrape_bosses()
        consumables_data = scraper.scrape_consumables()
        npcs_data = scraper.scrape_npcs()
        
        # Convert dicts to class instances
        weapons = [Weapon.from_dict(w) for w in weapons_data]
        armor = [Armor.from_dict(a) for a in armor_data]
        bosses = [Boss.from_dict(b) for b in bosses_data]
        items = [Item.from_dict(i) for i in consumables_data]
        npcs = [NPC.from_dict(n) for n in npcs_data]

        # Example: Display info for the first weapon, armor, boss, item, and npc
        if weapons: weapons[0].display_info()
        if armor: armor[0].display_info()
        if bosses: bosses[0].display_info()
        if items: items[0].display_info()
        if npcs: npcs[0].display_info()

        # Save data to JSON
        data_handler.save_to_json('weapons.json', weapons_data)
        data_handler.save_to_json('armor.json', armor_data)
        data_handler.save_to_json('bosses.json', bosses_data)
        data_handler.save_to_json('items.json', consumables_data)
        data_handler.save_to_json('npcs.json', npcs_data)

        # Save data to CSV
        data_handler.save_to_csv('weapons.csv', weapons_data)
        data_handler.save_to_csv('armor.csv', armor_data)
        data_handler.save_to_csv('bosses.csv', bosses_data)
        data_handler.save_to_csv('items.csv', consumables_data)
        data_handler.save_to_csv('npcs.csv', npcs_data)

        print("Data scraping and saving completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()