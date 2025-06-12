import pygame
RED = (255, 0, 0)  # 確保顏色定義存在
image_b = pygame.image.load("battle.jpg")
battle = pygame.transform.scale(image_b, (1200, 700))

class Equipment:
    def __init__(self, name, eq_type, stat_bonus, level=1):
        self.name = name
        self.eq_type = eq_type  # 'weapon', 'armor', 'accessory'
        self.stat_bonus = stat_bonus  # dict: {'str':2, ...}
        self.level = level
        self.is_equipped = False  # 新增屬性，追蹤是否已被裝備

    def equip(self, character):
        """裝備物品並保留物品在背包中"""
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        if self.is_equipped:  # 檢查是否已被其他角色裝備
            DisplaySystem.show_message(f"{self.name} is already equipped by another character.", color=RED, background=battle)
            pygame.time.wait(1200)  # 等待1秒
            return
        for k, v in self.stat_bonus.items():
            if hasattr(character, k):
                setattr(character, k, getattr(character, k) + v * self.level)
        if self.eq_type == "weapon":  # 添加武器攻擊加成    
            character.attack_power += self.stat_bonus.get("atk", 0) * self.level
        elif self.eq_type == "armor":  # 添加防禦加成
            character.armor += self.stat_bonus.get("def", 0) * self.level
        elif self.eq_type == "accessory":  # 添加魔力加成
            character.mp += self.stat_bonus.get("mp", 0) * self.level
        character.equipment[self.eq_type] = self  # 更新角色的裝備
        self.is_equipped = True  # 標記為已裝備
        DisplaySystem.show_message(f"{character.name} equipped {self.name} (Lv.{self.level})!", background=battle)
        pygame.time.wait(1200)  # 等待1秒

    def unequip(self, character):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        for k, v in self.stat_bonus.items():
            if hasattr(character, k):
                setattr(character, k, getattr(character, k) - v * self.level)
        self.is_equipped = False  # 標記為未裝備
        DisplaySystem.show_message(f"{character.name} unequipped {self.name} (Lv.{self.level})!", background=battle)
        pygame.time.wait(1200)  # 等待1秒

    def is_equipped(self):
        """檢查裝備是否已被裝備"""
        return self.is_equipped

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
            from rpg_game.src.display import DisplaySystem
            DisplaySystem.show_message(f"{self.name} deals extra holy damage to {target.name}!")
            target.hp -= 20  # Example of special effect

class thors_hammer(EquipmentType):
    def __init__(self, level=1):
        super().__init__("Thor's Hammer", "weapon", {"str": 7, "atk": 15}, level)
        self.special_effect = "Chance to stun the target"

    def use_special_effect(self, target):
        import random
        if random.random() < 0.3:  # 30% chance to stun
            from rpg_game.src.display import DisplaySystem
            DisplaySystem.show_message(f"{self.name} stuns {target.name}!")
            pygame.time.wait(1200)
            target.is_stunned = True  # Assuming target has an is_stunned attribute

class shild(EquipmentType):
    def __init__(self, level=1):
        super().__init__("Shield", "armor", {"vit": 3, "def": 5}, level)
        self.special_effect = "Reduces damage taken from physical attacks"

    def use_special_effect(self, damage):
        reduced_damage = damage * 0.7  # Example of special effect
        from rpg_game.src.display import DisplaySystem
        DisplaySystem.show_message(f"{self.name} reduces damage taken to {reduced_damage}!")
        pygame.time.wait(1200)
        return reduced_damage
    
class book(EquipmentType):
    def __init__(self, level=1):
        super().__init__("Book of Spells", "accessory", {"intel": 4, "mp": 10}, level)
        self.special_effect = "Increases spell power and mana regeneration"

    def use_special_effect(self, character):
        character.mp += 5 * self.level  # Example of special effect
        from rpg_game.src.display import DisplaySystem
        DisplaySystem.show_message(f"{character.name} gains extra mana from {self.name}!")
        pygame.time.wait(1200)

class ring(EquipmentType):
    def __init__(self, level=1):
        super().__init__("Ring of Power", "accessory", {"str": 2, "atk": 5}, level)
        self.special_effect = "Increases attack power and critical hit chance"

    def use_special_effect(self, character):
        character.attack_power += 3 * self.level
        from rpg_game.src.display import DisplaySystem
        DisplaySystem.show_message(f"{character.name} gains extra mana from {self.name}!")
        pygame.time.wait(1200)

