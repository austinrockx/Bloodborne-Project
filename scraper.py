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
            expected_headers = ['image', 'name', 'damage', 'qs bullet use', 'durability', 'stats needed\nstat bonuses', 'special attack', 'availability', 'special note']
        tables = soup.find_all("table", {"class": "wiki-blog-table-sheader"}) # Find all tables with the class "wiki-blog-table-sheader"
        for table in tables: 
            header_row = table.find("tr") # Find the first row in the table
            if not header_row:
                continue
            headers = [th.text.strip().lower() for th in header_row.find_all("th")] # Find all header cells in the row
            # Check if the headers match the expected headers
            if headers[:len(expected_headers)] == expected_headers:
                rows = table.find_all("tr") # Find all rows in the table
                for row in rows[1:]:  # Skip header
                    cols = row.find_all("td") # Find all columns in the row
                    if len(cols) < 5: # Ensure there are enough columns
                        continue
                    name_link = cols[1].find("a") # Find the first anchor tag in the second column
                                 # Parse damage column: e.g. '25 / - / - / - / -\n\n(Physical)'
                    damage_text = cols[2].text.strip()
                    base_damage = damage_type = ""
                    if "\n\n" in damage_text:
                        base, dtype = damage_text.split("\n\n", 1)
                        base_damage = base.split("/")[0].strip()
                        damage_type = dtype.replace("(", "").replace(")", "").strip()
                    else:
                        base_damage = damage_text.split("/")[0].strip()
                        damage_type = ""
                    # Parse stats needed and stat bonuses
                    stats_text = cols[5].text.strip()
                    if "\n\n" in stats_text:
                        stats_needed, stat_bonuses = stats_text.split("\n\n", 1)
                        stats_needed = stats_needed.strip()
                        stat_bonuses = stat_bonuses.strip()
                    else:
                        stats_needed = stats_text
                        stat_bonuses = ""
                    weapon = {
                        "name": cols[1].text.strip(),
                        "link": name_link["href"] if name_link and name_link.has_attr("href") else None,
                        "base-damage": base_damage,
                        "damage-type": damage_type,
                        "durability": cols[4].text.strip(),
                        "stats-needed": stats_needed,
                        "stat-bonuses": stat_bonuses,
                        "special attack": cols[6].text.strip(),
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
            expected_titles = ['Set', 'Physical', 'VS blunt', 'VS Thurst', 'Blood', 'Arcane', 'Fire', 'Bolt', 'Slow Poison RES', 'Rapid Poison RES', 'Frenzy RES', 'Beasthood']
        tables = soup.find_all("table", {"class": "wiki-blog-table-sheader"})
        for table in tables:
            header_row = table.find("tr")
            if not header_row:
                continue
            # Extract title from <img class="image"> if present, otherwise use text
            header_titles = []
            for th in header_row.find_all("th"):
                img = th.find("img", class_="image")
                if img and img.has_attr("title"):
                    header_titles.append(img["title"].strip())
                else:
                    header_titles.append(th.text.strip())
            # Check if all expected titles are in header_titles (in order)
            if all(title in header_titles for title in expected_titles):
                rows = table.find_all("tr")
                for row in rows[1:]:  # Skip the header row
                    cols = row.find_all("td")
                    if len(cols) < 12:
                        continue
                    set_link = cols[0].find("a")
                    armor_set = {
                        "set": cols[0].text.strip(),
                        "link": set_link["href"] if set_link and set_link.has_attr("href") else None,
                        "physical-defense": cols[1].text.strip(),
                        "blunt-defense": cols[2].text.strip(),
                        "thrust-defense": cols[3].text.strip(),
                        "blood-defense": cols[4].text.strip(),
                        "arcane-defense": cols[5].text.strip(),
                        "fire-defense": cols[6].text.strip(),
                        "bolt-defense": cols[7].text.strip(),
                        "slow-poison-resist": cols[8].text.strip(),
                        "rapid-poison-resist": cols[9].text.strip(),
                        "frenzy-resist": cols[10].text.strip(),
                        "beasthood": cols[11].text.strip(),
                    }
                    armor.append(armor_set)
        return armor

    def scrape_bosses(self):
        """
        Scrapes boss data from the Bloodborne Wiki.
        
        :return: A list of dictionaries containing boss data.
        """
        bosses = [] # Initialize an empty list to store weapon data
        soup = self.fetch_page("p/bosses.html") # Fetch the weapons page
        if soup:
            expected_headers = ['boss', 'drops', 'hp', 'blood echoes', 'location', 'interruptible', 'required']
        tables = soup.find_all("table", {"class": "wiki-blog-table-sheader1"}) # Find all tables with the class "wiki-blog-table-sheader"
        for table in tables: 
            header_row = table.find("tr") # Find the first row in the table
            if not header_row:
                continue
            headers = [th.text.strip().lower() for th in header_row.find_all("th")] # Find all header cells in the row
            # Check if the headers match the expected headers
            if headers[:len(expected_headers)] == expected_headers:
                rows = table.find_all("tr") # Find all rows in the table
                for row in rows[1:]:  # Skip header
                    cols = row.find_all("td") # Find all columns in the row
                    if len(cols) < 6: # Ensure there are enough columns
                        continue
                    name_link = cols[1].find("a") # Find the first anchor tag in the second column
                    boss = {
                        "name": cols[0].text.strip(),
                        "link": name_link["href"] if name_link and name_link.has_attr("href") else None, # Extract the link if it exists
                        "drops": cols[1].text.strip(),
                        "HP": cols[2].text.strip(),
                        "blood-echoes": cols[3].text.strip(),
                        "location": cols[4].text.strip(),
                        "required": cols[6].text.strip(),
                    }
                    bosses.append(boss)
                break  # Stop after finding the correct table
        return bosses
    
    def scrape_consumables(self):
        """
        Scrapes item data from the Bloodborne Wiki.

        :return: A list of dictionaries containing item data.
        """
        consumables = []
        soup = self.fetch_page("p/consumables.html")
        if soup:
        # Define the expected headers (lowercase for comparison)
            expected_headers = ['icon', 'name', 'effect', 'no. held', 'stored', 'usage type', 'availability']
        tables = soup.find_all("table", {"class": "wiki-blog-table-sheader1"})
        for table in tables:
            header_row = table.find("tr")
            if not header_row:
                continue
            headers = [th.text.strip().lower() for th in header_row.find_all("th")]
            if headers[:len(expected_headers)] == expected_headers:
                rows = table.find_all("tr")
                for row in rows[1:]:  # Skip the header row
                    cols = row.find_all("td")
                    if len(cols) < 6:
                        continue
                    name_link = cols[1].find("a")
                    item = {
                        "name": cols[1].text.strip(),
                        "link": name_link["href"] if name_link and name_link.has_attr("href") else None,
                        "effect": cols[2].text.strip(),
                        "num-held": cols[3].text.strip(),
                        "stored": cols[4].text.strip(),
                        "usage-type": cols[5].text.strip()
                    }
                    consumables.append(item)
                break  # Stop after finding the correct table
        return consumables

    def scrape_npcs(self):
        """
        Scrapes NPC data from the Bloodborne Wiki.
        
        :return: A list of dictionaries containing NPC data.
        """
        npcs = []
        soup = self.fetch_page("p/npcs.html")
        if soup:
             # Define the expected headers (lowercase for comparison)
            expected_headers = ['image', 'name', 'item', 'drop', 'location', 'timezones']
            tables = soup.find_all("table", {"class": "wiki-blog-table-sheader1"})
        for table in tables:
            header_row = table.find("tr")
            if not header_row:
                continue
            headers = [th.text.strip().lower() for th in header_row.find_all("th")]
            if headers[:len(expected_headers)] == expected_headers:
                rows = table.find_all("tr")
                for row in rows[1:]:  # Skip the header row
                    cols = row.find_all("td")
                    if len(cols) < 4:
                        continue
                    name_link = cols[1].find("a")
                    npc = {
                        "name": cols[1].text.strip(),
                        "link": name_link["href"] if name_link and name_link.has_attr("href") else None,
                        "item": cols[2].text.strip(),
                        "drop": cols[3].text.strip(),
                        "location": cols[4].text.strip(),
                        "timezones": cols[5].text.strip()  # E.g., Day, Evening, Night, Blood Moon
                    }
                    npcs.append(npc)
                break  # Stop after finding the correct table
        return npcs