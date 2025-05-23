from dataclasses import dataclass

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
        print(f"Weapon: {self.name} | Damage: {self.base_damage} ({self.damage_type})")

    @classmethod
    def from_dict(cls, data):
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
        print(f"Armor Set: {self.set} | Physical: {self.physical_defense}")

    @classmethod
    def from_dict(cls, data):
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
        print(f"Boss: {self.name} | HP: {self.HP} | Location: {self.location}")

    @classmethod
    def from_dict(cls, data):
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
        print(f"NPC: {self.name} | Location: {self.location}")

    @classmethod
    def from_dict(cls, data):
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
        print(f"Item: {self.name} | Effect: {self.effect}")

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            link=data.get("link", ""),
            effect=data.get("effect", ""),
            num_held=data.get("num-held", ""),
            stored=data.get("stored", ""),
            usage_type=data.get("usage-type", "")
        )