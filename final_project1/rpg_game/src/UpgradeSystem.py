from rpg_game.src.equipment import Equipment  # 確保匯入 Equipment 類型
from rpg_game.src.character import Character  # 確保匯入 Character 類型
from rpg_game.src.backpack import Backpack  # 確保匯入 Backpack 類型
import pygame
# 從這裡移除 DisplaySystem 的匯入

class UpgradeSystem:
    # 自訂每個等級升級所需的經驗值
    EXP_TABLE = {
        1: 100,
        2: 150,
        3: 210,
        4: 280,
        5: 360,
        # 可以繼續添加更多等級的經驗值需求
    }

    @staticmethod
    def calculate_exp_to_next_level(level):
        # 根據自訂表格計算升級所需經驗值，若未定義則使用預設公式
        return UpgradeSystem.EXP_TABLE.get(level, 100 + level * 10)

    @staticmethod
    def level_up(team, character):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        # 檢查總經驗值是否足夠升級
        if team.total_exp < character.exp_to_next_level:
            DisplaySystem.show_message(f"隊伍的總經驗值不足，無法升級！需要 {character.exp_to_next_level - team.total_exp} 額外經驗值。")
            pygame.time.wait(1200)  # 等待1秒
            return

        # 升級角色等級並提升六屬性
        team.total_exp -= character.exp_to_next_level
        character.level += 1
        character.exp_to_next_level = UpgradeSystem.calculate_exp_to_next_level(character.level)
        character.max_hp = int(character.max_hp * 1.1)
        character.hp = character.max_hp
        character.max_mp = int(character.max_mp * 1.1)
        character.mp = character.max_mp
        character.attack_power = int(character.attack_power * 1.1)
        character.max_armor = int(character.max_armor * 1.1)
        character.armor = character.max_armor

        # 提升六屬性
        character.str += 1
        character.vit += 1
        character.agl += 1
        character.dex += 1
        character.intel += 1

        DisplaySystem.show_message(f"{character.name} 升級到等級 {character.level}！六屬性提升：STR+1, VIT+1, AGL+1, DEX+1, INT+1")
        pygame.time.wait(1200)  # 等待1秒

    @staticmethod
    def upgrade_attribute(team, character, attribute, cost=50):
        from rpg_game.src.display import DisplaySystem, GREEN  # 動態匯入並定義顏色
        # 檢查總經驗值是否足夠提升屬性
        if team.total_exp < cost:
            DisplaySystem.show_message(f"隊伍的總經驗值不足，無法提升屬性！需要 {cost - team.total_exp} 額外經驗值。")
            pygame.time.wait(1200)  # 等待1秒
            return

        # 提升屬性
        team.total_exp -= cost
        setattr(character, attribute, getattr(character, attribute) + 1)
        DisplaySystem.show_message(f"{character.name} 的 {attribute.upper()} 提升了 1 點！", color=GREEN)
        pygame.time.wait(1200)

    @staticmethod
    def upgrade_equipment(team, equipment, cost=100):
        from rpg_game.src.display import DisplaySystem
        if team.total_exp < cost:
            DisplaySystem.show_message(f"隊伍的總經驗值不足，無法升級裝備！需要 {cost - team.total_exp} 額外經驗值。")
            pygame.time.wait(1200)  # 等待1秒
            return
        if hasattr(equipment, "level"):
            team.total_exp -= cost
            equipment.level += 1
            DisplaySystem.show_message(f"{equipment.name} 升級到等級 {equipment.level}！")
            pygame.time.wait(1200)
        else:
            DisplaySystem.show_message("無法升級此裝備。")
            pygame.time.wait(1200)


