from rpg_game.src.equipment import Equipment  # Import Equipment type
from rpg_game.src.character import Character  # Import Character type
from rpg_game.src.backpack import Backpack  # Import Backpack type
import pygame
# Remove DisplaySystem import from here

image_upgrade = pygame.image.load("upgrade.jpg")  # 升級系統畫面
upgrade_bg = pygame.transform.scale(image_upgrade, (800, 550))

class UpgradeSystem:
    # Custom experience points required for each level
    EXP_TABLE = {
        1: 100,
        2: 150,
        3: 210,
        4: 280,
        5: 360,
        # Can continue adding more level requirements
    }

    @staticmethod
    def calculate_exp_to_next_level(level):
        # Calculate required exp based on custom table, use default formula if not defined
        return UpgradeSystem.EXP_TABLE.get(level, 100 + level * 10)

    @staticmethod
    def level_up(team, character):
        from rpg_game.src.display import DisplaySystem  # Dynamic import
        # Check if total exp is enough for level up
        if team.total_exp < character.exp_to_next_level:
            DisplaySystem.show_message(
                f"Not enough EXP! Need {character.exp_to_next_level - team.total_exp} more.")
            pygame.time.wait(1200)
            return

        # Level up character and increase six attributes
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

        # Increase six attributes
        character.str += 1
        character.vit += 1
        character.agl += 1
        character.dex += 1
        character.intel += 1

        DisplaySystem.show_message(f"{character.name} reached level {character.level}! All stats +1")
        pygame.time.wait(1200)

    @staticmethod
    def upgrade_attribute(team, character, attribute, cost=50):
        from rpg_game.src.display import DisplaySystem, GREEN
        if team.total_exp < cost:
            DisplaySystem.show_message(
                f"Not enough EXP! Need {cost - team.total_exp} more.")
            pygame.time.wait(1200)
            return

        team.total_exp -= cost
        setattr(character, attribute, getattr(character, attribute) + 1)
        DisplaySystem.show_message(f"{character.name}'s {attribute.upper()} +1", color=GREEN)
        pygame.time.wait(1200)

    @staticmethod
    def upgrade_equipment(team, equipment, cost=100):
        from rpg_game.src.display import DisplaySystem
        if team.total_exp < cost:
            DisplaySystem.show_message(
                f"Not enough EXP! Need {cost - team.total_exp} more.")
            pygame.time.wait(1200)
            return
        if hasattr(equipment, "level"):
            team.total_exp -= cost
            equipment.level += 1
            DisplaySystem.show_message(f"{equipment.name} level {equipment.level}")
            pygame.time.wait(1200)
        else:
            DisplaySystem.show_message("Cannot upgrade")
            pygame.time.wait(1200)


