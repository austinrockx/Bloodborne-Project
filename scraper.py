"""
Bloodborne Wiki Scraper
-----------------------
This script scrapes data from the Bloodborne Wiki, extracting information about
weapons, armor, bosses, items, and NPCs. The data is collected from tables on
the website and structured into dictionaries for further analysis or storage.

Features:
- Fetches HTML content from the Bloodborne Wiki.
- Extracts and structures data for various Bloodborne entities.
- Implements exception handling for request failures.
- Uses BeautifulSoup for HTML parsing.

Modules Used:
- requests: For making HTTP requests to the Bloodborne Wiki.
- BeautifulSoup (bs4): For parsing and navigating HTML content.

Author: Austin Bennett
Date: 2025-03-13
"""

import requests # A Python library for making HTTP requests to fetch web content.
from bs4 import BeautifulSoup # Part of the bs4 library, used for parsing HTML and extracting data from web pages.

# Custom module for scraping data from the Bloodborne Wiki.
class BloodborneScraper:
    def __init__(self): # Initialize the scraper with the base URL of the Bloodborne Wiki.
        self.base_url = "https://www.bloodborne-wiki.com/"

    def fetch_page(self, endpoint):
        """
        Fetches the HTML content of a given endpoint from the Bloodborne Wiki.
        
        :param endpoint: The specific page to fetch (e.g., "Weapons", "Bosses").
        :return: BeautifulSoup object containing the parsed HTML content.
        """
        try:
            response = requests.get(self.base_url + endpoint) # Make a GET request to the specified URL
            response.raise_for_status()  # Raise an HTTPError for bad responses
            print(f"Fetching: {self.base_url + endpoint}") # Print the URL being fetched
            return BeautifulSoup(response.text, 'html.parser') # Parse the HTML content with BeautifulSoup
        except requests.RequestException as e:
            print(f"Failed to fetch page {endpoint}: {e}")
            print(f"Response Status Code: {response.status_code}")
            return None

    def scrape_weapons(self):
        """
        Scrapes weapon data from the Bloodborne Wiki.
        
        :return: A list of dictionaries containing weapon data.
        """
        weapons = [] # Initialize an empty list to store weapon data
        soup = self.fetch_page("p/weapons.html") # Fetch the weapons page
        if soup:
            expected_headers = ["Name", "Damage", "Durability", "Stats Needed", " Stat Bounses"]
        tables = soup.find_all("table", {"class": "wiki-blog-table-sheader"}) # Find all tables with the class "wiki-blog-table-sheader"
        for table in tables: 
            header_row = table.find("tr") # Find the first row in the table
            if not header_row:
                continue
            headers = [th.text.strip() for th in header_row.find_all("th")] # Find all header cells in the row
            # Check if the headers match the expected headers
            if headers == expected_headers:
                rows = table.find_all("tr") # Find all rows in the table
                for row in rows[1:]:  # Skip header
                    cols = row.find_all("td") # Find all columns in the row
                    if len(cols) < 5: # Ensure there are enough columns
                        continue
                    weapon = {
                        "name": cols[0].text.strip(),
                        "base-damage": cols[1].text.strip(),
                        "durability": cols[3].text.strip(),
                        "stats-needed": cols[4].text.strip(),
                    }
                    weapons.append(weapon)
                break  # Stop after finding the correct table
        return weapons


    def scrape_armor(self):
        """
        Scrapes armor data from the Bloodborne Wiki.
        
        :return: A list of dictionaries containing armor data.
        """
        armor = [] # Initialize an empty list to store armor data
        soup = self.fetch_page("p/armor-sets.html") # Fetch the armor page
        if soup:
            # Find the table containing armor data
            table = soup.find("table", {"class": "wiki_table"}) # Find the first table with the class "wiki_table"
            if table:
                rows = table.find_all("tr") # Find all rows in the table
                for row in rows[1:]:  # Skip the header row
                    cols = row.find_all("td") # Find all columns in the row
                    # Extracting the different armor attributes from the wiki, in order to fill the 'armor' list
                    armor_set = {
                        "set": cols[0].text.strip(),
                        "physical-defense": cols[1].text.strip(), # E.g., Physical, Blunt, Thrust, Blood
                        "elemenatl-defense": cols[2].text.strip(), # E.g., Arcane, Fire, Bolt
                        "resistance": cols[3].text.strip(), # E.g., Slow Poison, Rapid Poison, Frenzy
                        "beastblood-stat": cols[4].text.strip() # E.g., Beasthood
                    }
                    armor.append(armor_set)
        return armor

    def scrape_bosses(self):
        """
        Scrapes boss data from the Bloodborne Wiki.
        
        :return: A list of dictionaries containing boss data.
        """
        bosses = [] # Initialize an empty list to store 'bosses' data
        soup = self.fetch_page("p/bosses.html") # Fetch the bosses page
        
        if soup:
            # Example: Find the table containing boss data
            table = soup.find("table", {"class": "wiki_table"})
            if table:
                rows = table.find_all("tr") # Find all rows in the table
                for row in rows[1:]:  # Skip the header row
                    cols = row.find_all("td") # Find all columns in the row
                    # Extracting the different boss attributes from the wiki, in order to fill the 'bosses' list
                    boss = {
                        "name": cols[0].text.strip(),
                        "location": cols[1].text.strip(),   
                        "defenses": cols[2].text.strip(), # E.g., Physical, Blunt, Thrust, Blood, Arcane, Fire, Bolt
                        "resistances": cols[3].text.strip(), # E.g., Slow Poison, Rapid Poison, Frenzy
                        "bonuses": cols[4].text.strip(), # E.g., Beasts, Kin
                        "drops": cols[5].text.strip() # E.g., Blood Echoes, Blood Vials, Quicksilver Bullets, Blood Gems, Caryll Runes
                    }
                    bosses.append(boss)
        return bosses

    def scrape_items(self):
        """
        Scrapes item data from the Bloodborne Wiki.
        
        :return: A list of dictionaries containing item data.
        """
        items = [] # Initialize an empty list to store 'items' data
        soup = self.fetch_page("p/items.html") # Fetch the items page
        if soup:
            # Example: Find the table containing item data
            table = soup.find("table", {"class": "wiki_table"})
            if table:
                rows = table.find_all("tr")
                for row in rows[1:]:  # Skip the header row
                    cols = row.find_all("td")
                    # Extracting the different item attributes from the wiki, in order to fill the 'items' list
                    item = {
                        "name": cols[0].text.strip(),
                        "type": cols[1].text.strip(), # E.g., Consumable, Hunter Tools, Key, Multiplayer, Caryll Runes
                        "effect": cols[2].text.strip(),
                        "location": cols[3].text.strip(),
                        "usage-type": cols[4].text.strip(), # E.g., Finite, Unlimited Use
                        "num-held": cols[5].text.strip(), 
                        "stored": cols[6].text.strip()
                    }
                    items.append(item)
        return items

    def scrape_npcs(self):
        """
        Scrapes NPC data from the Bloodborne Wiki.
        
        :return: A list of dictionaries containing NPC data.
        """
        npcs = []
        soup = self.fetch_page("p/merchants.html")
        if soup:
            # Example: Find the table containing NPC data
            table = soup.find("table", {"class": "wiki_table"})
            if table:
                rows = table.find_all("tr")
                for row in rows[1:]:  # Skip the header row
                    cols = row.find_all("td")
                    # Extracting the different NPC attributes from the wiki, in order to fill the 'npcs' list
                    npc = {
                        "name": cols[0].text.strip(),
                        "drops": cols[3].text.strip(),
                        "location": cols[1].text.strip(),
                        "timezones": cols[2].text.strip() # E.g., Day, Evening, Night, Blood Moon
                    }
                    npcs.append(npc)
        return npcs