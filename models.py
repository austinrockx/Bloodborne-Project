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
        # Print a summary of the weapon's key stats
        print(f"Weapon: {self.name} | Base Damage: {self.base_damage} ({self.damage_type}) | Stats Needed: {self.stats_needed}")

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
        print(f"Armor Set: {self.set} | Physical Defense: {self.physical_defense}, {self.blunt_defense}, {self.thrust_defense}, {self.blood_defense} | Elemental Defense: {self.arcane_defense}, {self.fire_defense}, {self.bolt_defense} | Resistances: {self.slow_poison_resist}, {self.rapid_poison_resist}, {self.frenzy_resist} | Beasthood: {self.beasthood}")

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
        print(f"Boss: {self.name} | Drops: {self.drops} | HP: {self.HP} | Blood Echoes: {self.blood_echoes} | Location: {self.location} | Required: {self.required}")

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
        print(f"NPC: {self.name} | Location: {self.location} | Timezones: {self.timezones}")

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
        print(f"Item: {self.name} | Effect: {self.effect} | No. Held: {self.num_held} | Stored: {self.stored} | Usage Type: {self.usage_type}")

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