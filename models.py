"""
Bloodborne Wiki Data Models
---------------------------
This module defines dataclasses for Bloodborne entities, including Weapon, Armor, Boss, NPC, and Item.
Each class encapsulates the attributes and behaviors of its respective entity, provides a display_info() 
method for pretty-printing, and a from_dict() classmethod for easy instantiation from scraped data.

Features:
- Object-oriented representation of Bloodborne data entities.
- Methods for displaying entity information in a readable format.
- Class methods for constructing objects from dictionaries.

Modules Used:
- dataclasses: For concise and readable class definitions.

Author: Austin Bennett
Date: 2025-05-23
"""

from dataclasses import dataclass # Import dataclass decorator for concise class definitions
from colorama import Fore, Style, init # Import colorama for colored terminal output
init(autoreset=True) # Automatically reset color after each print

@dataclass
class Weapon:
    name: str
    link: str
    base_damage: str
    damage_type: str
    durability: str
    stats_needed: str
    stat_bonuses: str
    special_attack: str

    def display_info(self):
        info = (
        f"\n{'='*10}\n"
        f"Weapon: {self.name}\n"
        f"Base Damage: {self.base_damage} ({self.damage_type})\n"
        f"Durability: {self.durability}\n"
        f"Stats Needed: {self.stats_needed}\n"
        f"Stat Bonuses: {self.stat_bonuses}\n"
        f"Special Attack: {self.special_attack}\n"
        f"{'='*10}"
        )
        print(Fore.CYAN + info + Style.RESET_ALL)

    @classmethod
    def from_dict(cls, data):
        # Create a Weapon instance from a dictionary
        return cls(
            name=data.get("name", ""),
            link=data.get("link", ""),
            base_damage=data.get("base-damage", ""),
            damage_type=data.get("damage-type", ""),
            durability=data.get("durability", ""),
            stats_needed=data.get("stats-needed", ""),
            stat_bonuses=data.get("stat-bonuses", ""),
            special_attack=data.get("special attack", "")
        )

@dataclass
class Armor:
    set: str
    link: str
    physical_defense: str
    blunt_defense: str
    thrust_defense: str
    blood_defense: str
    arcane_defense: str
    fire_defense: str
    bolt_defense: str
    slow_poison_resist: str
    rapid_poison_resist: str
    frenzy_resist: str
    beasthood: str

    def display_info(self):
        # Print a summary of the armor set's key stats
        info = (
        f"\n{'='*10}\n"
        f"Armor Set: {self.set}\n"
        f"Physical Defenses: {self.physical_defense}, {self.blunt_defense}, {self.thrust_defense}, {self.blood_defense}\n"
        f"Elemenatl Defenses: {self.arcane_defense}, {self.fire_defense}, {self.bolt_defense}\n"
        f"Resistances: {self.slow_poison_resist}, {self.rapid_poison_resist}, {self.frenzy_resist}\n"
        f"Beasthood: {self.beasthood}\n"
        f"{'='*10}"
        )
        print(Fore.YELLOW + info + Style.RESET_ALL)

    @classmethod
    def from_dict(cls, data):
        # Create an Armor instance from a dictionary
        return cls(
            set=data.get("set", ""),
            link=data.get("link", ""),
            physical_defense=data.get("physical-defense", ""),
            blunt_defense=data.get("blunt-defense", ""),
            thrust_defense=data.get("thrust-defense", ""),
            blood_defense=data.get("blood-defense", ""),
            arcane_defense=data.get("arcane-defense", ""),
            fire_defense=data.get("fire-defense", ""),
            bolt_defense=data.get("bolt-defense", ""),
            slow_poison_resist=data.get("slow-poison-resist", ""),
            rapid_poison_resist=data.get("rapid-poison-resist", ""),
            frenzy_resist=data.get("frenzy-resist", ""),
            beasthood=data.get("beasthood", "")
        )

@dataclass
class Boss:
    name: str
    link: str
    drops: str
    HP: str
    blood_echoes: str
    location: str
    required: str

    def display_info(self):
        # Print a summary of the boss's key stats
        info = (
        f"\n{'='*10}\n"
        f"Boss Name: {self.name}\n"
        f"Drops: {self.drops}\n"
        f"HP: {self.HP}\n"
        f"Blood Echoes: {self.blood_echoes}\n"
        f"Location: {self.location}\n"
        f"Required: {self.required}\n"
        f"{'='*10}"
        )
        print(Fore.LIGHTGREEN_EX + info + Style.RESET_ALL)

    @classmethod
    def from_dict(cls, data):
        # Create a Boss instance from a dictionary
        return cls(
            name=data.get("name", ""),
            link=data.get("link", ""),
            drops=data.get("drops", ""),
            HP=data.get("HP", ""),
            blood_echoes=data.get("blood-echoes", ""),
            location=data.get("location", ""),
            required=data.get("required", "")
        )

@dataclass
class NPC:
    name: str
    link: str
    item: str
    drop: str
    location: str
    timezones: str

    def display_info(self):
        # Print a summary of the NPC's key stats
        info = (
        f"\n{'='*10}\n"
        f"NPC Name: {self.name}\n"
        f"Location: {self.location}\n"
        f"Timezones: {self.timezones}\n"
        f"{'='*10}"
        )
        print(Fore.LIGHTRED_EX + info + Style.RESET_ALL)

    @classmethod
    def from_dict(cls, data):
        # Create an NPC instance from a dictionary
        return cls(
            name=data.get("name", ""),
            link=data.get("link", ""),
            item=data.get("item", ""),
            drop=data.get("drop", ""),
            location=data.get("location", ""),
            timezones=data.get("timezones", "")
        )

@dataclass
class Item:
    name: str
    link: str
    effect: str
    num_held: str
    stored: str
    usage_type: str

    def display_info(self):
        # Print a summary of the item's key stats
        info = (
        f"\n{'='*10}\n"
        f"Boss Name: {self.name}\n"
        f"Effect: {self.effect}\n"
        f"No. Held: {self.num_held}\n"
        f"Stored: {self.stored}\n"
        f"Usage Type: {self.usage_type}\n"
        f"{'='*10}"
        )
        print(Fore.LIGHTYELLOW_EX + info + Style.RESET_ALL)

    @classmethod
    def from_dict(cls, data):
        # Create an Item instance from a dictionary
        return cls(
            name=data.get("name", ""),
            link=data.get("link", ""),
            effect=data.get("effect", ""),
            num_held=data.get("num-held", ""),
            stored=data.get("stored", ""),
            usage_type=data.get("usage-type", "")
        )