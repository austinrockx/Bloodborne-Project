"""
Bloodborne Wiki Data Handler
----------------------------
This script defines the DataHandler class, which provides functionality for 
saving and loading scraped Bloodborne Wiki data in JSON and CSV formats.

Features:
- Saves structured data to JSON files with proper indentation.
- Saves tabular data to CSV files with appropriate headers.
- Loads data from both JSON and CSV files.
- Implements exception handling to prevent data loss or corruption.

Modules Used:
- json: For handling JSON serialization and deserialization.
- csv: For reading and writing CSV files.
- os: For file-related operations.

Usage:
- Use `save_to_json()` and `save_to_csv()` to store scraped data.
- Use `load_from_json()` and `load_from_csv()` to retrieve stored data.

Author: Austin Bennett
Date: 2025-03-13
"""

import json # A module for working with JSON data, allowing you to save and load structured data.
import csv # A module for reading and writing CSV (Comma-Separated Values) files.
import os # Provides functions for interacting with the operating system, such as file handling.

class DataHandler:
    def __init__(self): # Initialize any necessary attributes if needed
        pass
    
    def save_to_json(self, filename, data):
        """
        Saves data to a JSON file.
        
        :param filename: The name of the JSON file to save the data to.
        :param data: The data to save (should be serializable to JSON).
        """
        try:
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            print(f"Data successfully saved to {filename}")
        except IOError as e:
            print(f"Failed to save data to {filename}: {e}")

    def save_to_csv(self, filename, data):
        """
        Saves data to a CSV file.
        
        :param filename: The name of the CSV file to save the data to.
        :param data: The data to save (should be a list of dictionaries).
        """
        if not data:
            print(f"No data to save to {filename}")
            return

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                # Get the headers from the keys of the first dictionary in the list
                headers = data[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            print(f"Data successfully saved to {filename}")
        except IOError as e:
            print(f"Failed to save data to {filename}: {e}")

    def load_from_json(self, filename):
        """
        Loads data from a JSON file.
        
        :param filename: The name of the JSON file to load the data from.
        :return: The loaded data.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            print(f"Data successfully loaded from {filename}")
            return data
        except IOError as e:
            print(f"Failed to load data from {filename}: {e}")
            return None

    def load_from_csv(self, filename):
        """
        Loads data from a CSV file.
        
        :param filename: The name of the CSV file to load the data from.
        :return: The loaded data as a list of dictionaries.
        """
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                data = [row for row in reader]
            print(f"Data successfully loaded from {filename}")
            return data
        except IOError as e:
            print(f"Failed to load data from {filename}: {e}")
            return None