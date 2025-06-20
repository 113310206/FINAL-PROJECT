# 元素屬性定義
ELEMENTS = ["FIRE", "WATER", "WOOD"]

class JobBase:
    def __init__(self, name, level, s, v, ag, d, i, job=None, position=None, element=None):
        if element is not None and element not in ELEMENTS:
            raise ValueError(f"Invalid element '{element}'. Must be one of {ELEMENTS}.")
        self.element = element
        self.name = name
        self.level = level
        self.str = s
        self.vit = v
        self.agl = ag
        self.dex = d
        self.intel = i
        self.job = job
        self.position = position
        self.job_name = name

    def create_character(self):
        raise NotImplementedError


class Warrior(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="mid", element="FIRE"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        from rpg_game.src.character import Character
        from rpg_game.src.skill import Skill, ElementalSkill
        skill_obj = Skill("Power Strike", 10, 40, "A heavy blow to the enemy.")
        elem_skill = ElementalSkill("Flame Slash", 20, 50, self.element, "A fiery slash that burns the enemy.")
        character = Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)
        # 允許元素屬性可被改變
        character.element = self.element
        return character

class Mage(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="back", element="WATER"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        from rpg_game.src.character import Character
        from rpg_game.src.skill import Skill, ElementalSkill
        skill_obj = Skill("Arcane Shield", 15, 0, "Grants a magic shield (no damage).")
        elem_skill = ElementalSkill("Water Blast", 30, 60, self.element, "A blast of water that soaks the enemy.")
        character = Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)
        character.element = self.element
        return character

class Archer(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="back", element="WOOD"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        from rpg_game.src.character import Character
        from rpg_game.src.skill import Skill, ElementalSkill
        skill_obj = Skill("Arrow Barrage", 15, 20, "Shoots a barrage of arrows.")
        elem_skill = ElementalSkill("Nature's Wrath", 30, 60, self.element, "Unleashes the wrath of nature.")
        character = Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)
        character.element = self.element
        return character

class Healer(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="back", element="WOOD"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        from rpg_game.src.character import Character
        from rpg_game.src.skill import Skill, ElementalSkill
        skill_obj = Skill("Heal", 10, 0, "Restores HP to an ally.")
        elem_skill = ElementalSkill("Earth's Embrace", 20, 50, self.element, "A healing spell that restores health.")
        character = Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)
        character.element = self.element
        return character

class Tank(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="front", element="WOOD"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        from rpg_game.src.character import Character
        from rpg_game.src.skill import Skill, ElementalSkill
        skill_obj = Skill("Shield Bash", 10, 30, "Bashes the enemy with a shield.")
        elem_skill = ElementalSkill("Stone Wall", 20, 40, self.element, "Creates a wall of stone for defense.")
        character = Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)
        character.element = self.element
        return character

class KingKnight(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="mid", element="FIRE"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        from rpg_game.src.character import Character
        from rpg_game.src.skill import Skill, ElementalSkill
        skill_obj = Skill("Knight's Charge", 15, 50, "Charges at the enemy with a lance.")
        elem_skill = ElementalSkill("Holy Light", 30, 70, self.element, "A holy light that damages and heals.")
        character = Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)
        character.element = self.element
        return character

class Shooter(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="mid", element="WATER"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        from rpg_game.src.character import Character
        from rpg_game.src.skill import Skill, ElementalSkill
        skill_obj = Skill("Rapid Fire", 15, 25, "Fires multiple arrows in quick succession.")
        elem_skill = ElementalSkill("Wind Arrow", 30, 55, self.element, "An arrow infused with the power of water.")
        character = Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)
        character.element = self.element
        return character