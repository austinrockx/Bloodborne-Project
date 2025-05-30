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
from cli import main_menu # CLI interface for interacting with the scraped data.

def main():
    """
        Main function to launch the Bloodborne CLI interface.
        This function serves as the entry point for the application, 
        delegating all user interaction and data exploration to the CLI defined in cli.py.
    """
    # Start the CLI (which can also call save_all_data after any user-driven change)
    main_menu()

if __name__ == "__main__":
    main()