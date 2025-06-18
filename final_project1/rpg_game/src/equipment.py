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
        """裝備物品"""
        from rpg_game.src.display import DisplaySystem, RED, GREEN, WHITE, BLACK
        screen = pygame.display.set_mode((1200, 700))
        DisplaySystem.clear_screen(background=battle)
        # 計算面板大小
        font = pygame.font.Font(None, 28)
        info = [
            f"Equipment: {self.name} (Lv.{self.level})",
            f"Type: {self.eq_type}",
            "Stat Bonuses:"
        ]
        
        # 計算文字高度
        text_height = len(info) * 30  # 基本資訊高度
        bonus_height = len(self.stat_bonus) * 25  # 屬性加成高度
        button_height = 50  # 按鈕區域高度
        padding = 40  # 上下邊距
        
        # 計算面板總高度
        panel_height = text_height + bonus_height + button_height + padding
        panel_width = 350  # 固定寬度
        
        # 創建確認面板
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((255, 255, 255, 200))
        screen.blit(panel, (50, 50))

        # 顯示裝備資訊
        y = 70
        for text in info:
            screen.blit(font.render(text, True, BLACK), (70, y))
            y += 30

        # 顯示屬性加成
        y += 10
        for stat, value in self.stat_bonus.items():
            screen.blit(font.render(f"+{value * self.level} {stat}", True, GREEN), (90, y))
            y += 25

        # 確認和取消按鈕
        button_y = y + 20
        confirm_rect = pygame.Rect(70, button_y, 100, 30)
        cancel_rect = pygame.Rect(180, button_y, 100, 30)
        pygame.draw.rect(screen, GREEN, confirm_rect, border_radius=5)
        pygame.draw.rect(screen, RED, cancel_rect, border_radius=5)
        screen.blit(font.render("Confirm", True, WHITE), (85, button_y + 5))
        screen.blit(font.render("Cancel", True, WHITE), (195, button_y + 5))
        pygame.display.flip()

        # 等待玩家選擇
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if confirm_rect.collidepoint(mouse_pos):
                        self._apply_equipment_effects(character)
                        character.equipment[self.eq_type] = self
                        self.is_equipped = True
                        DisplaySystem.show_message(f"{character.name} equipped {self.name}!", background=battle)
                        pygame.time.wait(500)
                        return True
                    elif cancel_rect.collidepoint(mouse_pos):
                        return False
        return False

    def _apply_equipment_effects(self, character):
        """應用裝備效果"""
        # 基本屬性加成
        for stat, value in self.stat_bonus.items():
            if hasattr(character, stat):
                current_value = getattr(character, stat)
                setattr(character, stat, current_value + value * self.level)
        
        # 特殊裝備效果
        if self.eq_type == "weapon":
            character.attack_power += self.stat_bonus.get("atk", 0) * self.level
            character.attack_power += self.stat_bonus.get("str", 0) * self.level  # 力量影響攻擊力
        elif self.eq_type == "armor":
            character.armor += self.stat_bonus.get("def", 0) * self.level
            character.armor += self.stat_bonus.get("vit", 0) * self.level  # 體力影響防禦
        elif self.eq_type == "accessory":
            character.mp += self.stat_bonus.get("mp", 0) * self.level
            character.mp += self.stat_bonus.get("intel", 0) * self.level  # 智力影響魔法值

        # 應用 BonusSystem 的加成效果
        from final_project import BonusSystem
        BonusSystem.apply_equipment_bonus(character, self)
        BonusSystem.apply_weapon_bonus(character, self)
        BonusSystem.apply_position_bonus(character)

    def unequip(self, character):
        """卸下裝備"""
        from rpg_game.src.display import DisplaySystem, RED, GREEN, WHITE, BLACK, BLUE
        screen = pygame.display.set_mode((1200, 700))
        DisplaySystem.clear_screen(background=battle)
        # 計算面板大小
        font = pygame.font.Font(None, 28)
        info = [
            f"Unequip: {self.name} (Lv.{self.level})",
            f"Type: {self.eq_type}",
            "Removing Stats:"
        ]
        
        # 計算文字高度
        text_height = len(info) * 30  # 基本資訊高度
        bonus_height = len(self.stat_bonus) * 25  # 屬性加成高度
        button_height = 50  # 按鈕區域高度
        padding = 40  # 上下邊距
        
        # 計算面板總高度
        panel_height = text_height + bonus_height + button_height + padding
        panel_width = 350  # 固定寬度
        
        # 創建確認面板
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((255, 255, 255, 200))
        screen.blit(panel, (50, 50))

        # 顯示卸下資訊
        y = 70
        for text in info:
            screen.blit(font.render(text, True, BLACK), (70, y))
            y += 30

        # 顯示將要移除的屬性
        y += 10
        for stat, value in self.stat_bonus.items():
            screen.blit(font.render(f"-{value * self.level} {stat}", True, RED), (90, y))
            y += 25

        # 確認和取消按鈕
        button_y = y + 20
        confirm_rect = pygame.Rect(70, button_y, 100, 30)
        cancel_rect = pygame.Rect(180, button_y, 100, 30)
        pygame.draw.rect(screen, RED, confirm_rect, border_radius=5)
        pygame.draw.rect(screen, BLUE, cancel_rect, border_radius=5)
        screen.blit(font.render("Confirm", True, WHITE), (85, button_y + 5))
        screen.blit(font.render("Cancel", True, WHITE), (195, button_y + 5))
        pygame.display.flip()

        # 等待玩家選擇
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if confirm_rect.collidepoint(mouse_pos):
                        self._remove_equipment_effects(character)
                        self.is_equipped = False
                        DisplaySystem.show_message(f"{character.name} unequipped {self.name}!", background=battle)
                        pygame.time.wait(500)
                        return True
                    elif cancel_rect.collidepoint(mouse_pos):
                        return False

    def _remove_equipment_effects(self, character):
        """移除裝備效果"""
        # 移除基本屬性加成
        for stat, value in self.stat_bonus.items():
            if hasattr(character, stat):
                current_value = getattr(character, stat)
                setattr(character, stat, current_value - value * self.level)
        
        # 移除特殊裝備效果
        if self.eq_type == "weapon":
            character.attack_power -= self.stat_bonus.get("atk", 0) * self.level
            character.attack_power -= self.stat_bonus.get("str", 0) * self.level
        elif self.eq_type == "armor":
            character.armor -= self.stat_bonus.get("def", 0) * self.level
            character.armor -= self.stat_bonus.get("vit", 0) * self.level
        elif self.eq_type == "accessory":
            character.mp -= self.stat_bonus.get("mp", 0) * self.level
            character.mp -= self.stat_bonus.get("intel", 0) * self.level

        # 移除 BonusSystem 的加成效果
        from final_project import BonusSystem
        BonusSystem.apply_equipment_bonus(character, self, reverse=True)
        BonusSystem.reset_equipment_bonus(character)
        BonusSystem.reset_position_bonus(character)

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

