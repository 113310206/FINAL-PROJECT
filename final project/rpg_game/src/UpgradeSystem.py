class UpgradeSystem:
    @staticmethod
    def level_up(character):
        character.exp -= character.exp_to_next_level
        character.level += 1
        character.exp_to_next_level = 100 + character.level * 5
        character.max_hp = int(character.max_hp * 1.1)
        character.hp = character.max_hp
        character.max_mp = int(character.max_mp * 1.1)
        character.mp = character.max_mp
        character.attack_power = int(character.attack_power * 1.1)
        character.max_armor = int(character.max_armor * 1.1)
        character.armor = character.max_armor
        print(f"{character.name} ¤É¯Å¨ìµ¥¯Å {character.level}¡I")
