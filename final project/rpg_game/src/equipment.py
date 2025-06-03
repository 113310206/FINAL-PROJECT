

class Equipment:
    def __init__(self, name, eq_type, stat_bonus, level=1):
        self.name = name
        self.eq_type = eq_type  # 'weapon', 'armor', 'accessory'
        self.stat_bonus = stat_bonus  # dict: {'str':2, ...}
        self.level = level

    def equip(self, character):
        # 動態匯入避免循環依賴
        if not hasattr(character, "name"):
            print("Invalid character type.")
            return
        for k, v in self.stat_bonus.items():
            if hasattr(character, k):
                setattr(character, k, getattr(character, k) + v * self.level)
        print(f"{character.name} equipped {self.name} (Lv.{self.level})!")

    def unequip(self, character):
        # 動態匯入避免循環依賴
        if not hasattr(character, "name"):
            print("Invalid character type.")
            return
        for k, v in self.stat_bonus.items():
            if hasattr(character, k):
                setattr(character, k, getattr(character, k) - v * self.level)
        print(f"{character.name} unequipped {self.name} (Lv.{self.level})!")

class EquipmentType:
    def __init__(self, name, eq_type, stat_bonus, level=1):
        self.name = name  # 裝備名稱
        self.eq_type = eq_type  # 裝備類型 ('weapon', 'armor', 'accessory')
        self.stat_bonus = stat_bonus  # 屬性加成
        self.level = level  # 裝備等級

    def create_equipment(self):
        return Equipment(self.name, self.eq_type, self.stat_bonus, self.level)

class excalibur(EquipmentType):
    def __init__(self, level=1):
        super().__init__("Excalibur", "weapon", {"str": 5, "atk": 10}, level)
        self.special_effect = "Deals extra holy damage to undead enemies"

    def use_special_effect(self, target):
        if target.element == "undead":
            print(f"{self.name} deals extra holy damage to {target.name}!")
            target.hp -= 20  # Example of special effect

class thors_hammer(EquipmentType):
    def __init__(self, level=1):
        super().__init__("槌子", "weapon", {"str": 7, "atk": 15}, level)
        self.special_effect = "Chance to stun the target"

    def use_special_effect(self, target):
        import random
        if random.random() < 0.3:  # 30% chance to stun
            print(f"{self.name} stuns {target.name}!")
            target.is_stunned = True  # Assuming target has an is_stunned attribute

class shild(EquipmentType):
    def __init__(self, level=1):
        super().__init__("Shield", "armor", {"vit": 3, "def": 5}, level)
        self.special_effect = "Reduces damage taken from physical attacks"

    def use_special_effect(self, damage):
        reduced_damage = damage * 0.7  # Example of special effect
        print(f"{self.name} reduces damage taken to {reduced_damage}!")
        return reduced_damage
    
class book(EquipmentType):
    def __init__(self, level=1):
        super().__init__("Book of Spells", "accessory", {"intel": 4, "mp": 10}, level)
        self.special_effect = "Increases spell power and mana regeneration"

    def use_special_effect(self, character):
        character.mp += 5 * self.level  # Example of special effect
        print(f"{character.name} gains extra mana from {self.name}!")

class ring(EquipmentType):
    def __init__(self, level=1):
        super().__init__("Ring of Power", "accessory", {"str": 2, "atk": 5}, level)
        self.special_effect = "Increases attack power and critical hit chance"

    def use_special_effect(self, character):
        character.attack_power += 3 * self.level  # Example of special effect
        print(f"{character.name} gains extra attack power from {self.name}!")

