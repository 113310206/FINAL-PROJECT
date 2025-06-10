from .character import Character
from .skill import Skill, ElementalSkill

FIRE = "FIRE"
WATER = "WATER"
WOOD = "WOOD"

class JobBase:
    def __init__(self, name, level, s, v, ag, d, i, job=None, position=None, element=None):
        if element not in [FIRE, WATER, WOOD]:
            raise ValueError(f"Invalid element '{element}'. Must be FIRE, WATER, or WOOD.")
        self.element = element or FIRE  # 默認值改為 FIRE
        self.name = name
        self.level = level
        self.str = s
        self.vit = v
        self.agl = ag
        self.dex = d
        self.intel = i
        self.job = job
        self.position = position
        self.job_name = name  # 新增 job_name 屬性

    def create_character(self):
        raise NotImplementedError


class Warrior(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="mid", element="FIRE"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        skill_obj = Skill("Power Strike", 10, 40, "A heavy blow to the enemy.")
        elem_skill = ElementalSkill("Flame Slash", 20, 50, "FIRE", "A fiery slash that burns the enemy.")  # 使用 FIRE 變數
        return Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)


class Mage(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="back", element="WATER"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        skill_obj = Skill("Arcane Shield", 15, 0, "Grants a magic shield (no damage).")
        elem_skill = ElementalSkill("Water Blast", 30, 60, "WATER", "A blast of water that soaks the enemy.")  # 使用 WATER 變數
        return Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)


class Archer(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="back", element="WOOD"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        skill_obj = Skill("Arrow Barrage", 15, 20, "Shoots a barrage of arrows.")
        elem_skill = ElementalSkill("Nature's Wrath", 30, 60, "WOOD", "Unleashes the wrath of nature.")  # 使用 WOOD 變數
        return Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)


class Healer(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="back", element="WOOD"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        skill_obj = Skill("Heal", 10, 0, "Restores HP to an ally.")
        elem_skill = ElementalSkill("Earth's Embrace", 20, 50, "WOOD", "A healing spell that restores health.")
        return Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)


class Tank(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="front", element="WOOD"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        skill_obj = Skill("Shield Bash", 10, 30, "Bashes the enemy with a shield.")
        elem_skill = ElementalSkill("Stone Wall", 20, 40, "WOOD", "Creates a wall of stone for defense.")
        return Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)


class KingKnight(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="mid", element="FIRE"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        skill_obj = Skill("Knight's Charge", 15, 50, "Charges at the enemy with a lance.")
        elem_skill = ElementalSkill("Holy Light", 30, 70, "FIRE", "A holy light that damages and heals.")
        return Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)


class Shooter(JobBase):
    def __init__(self, name, level, s, v, ag, d, i, job=None, position="mid", element="WATER"):
        super().__init__(name, level, s, v, ag, d, i, job, position, element)

    def create_character(self):
        skill_obj = Skill("Rapid Fire", 15, 25, "Fires multiple arrows in quick succession.")
        elem_skill = ElementalSkill("Wind Arrow", 30, 55, "WATER", "An arrow infused with the power of water.")  # 修正元素屬性
        return Character(self.name, self.level, self.str, self.vit, self.agl, self.dex, self.intel, skill_obj, elem_skill, self.element, self.job, self.position)