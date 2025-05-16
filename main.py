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
        items_data = scraper.scrape_items()
        npcs_data = scraper.scrape_npcs()

        # Save data to JSON
        data_handler.save_to_json('weapons.json', weapons_data)
        data_handler.save_to_json('armor.json', armor_data)
        data_handler.save_to_json('bosses.json', bosses_data)
        data_handler.save_to_json('items.json', items_data)
        data_handler.save_to_json('npcs.json', npcs_data)

        # Save data to CSV
        data_handler.save_to_csv('weapons.csv', weapons_data)
        data_handler.save_to_csv('armor.csv', armor_data)
        data_handler.save_to_csv('bosses.csv', bosses_data)
        data_handler.save_to_csv('items.csv', items_data)
        data_handler.save_to_csv('npcs.csv', npcs_data)

        print("Data scraping and saving completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()