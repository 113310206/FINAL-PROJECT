import random
from .job import Warrior, Mage, Archer, Healer, Tank, KingKnight, Shooter  # 匯入 JobBase 和具體職業類型
from .skill import Skill, ElementalSkill
from .equipment import Equipment, EquipmentType, excalibur, thors_hammer, shild, book, ring  # 匯入 EquipmentType 和具體裝備類型
from .backpack import Backpack  # 確保匯入 Backpack 類別

def gacha_draw_character():
    job_classes = [Warrior, Mage, Archer, Healer, Tank, KingKnight, Shooter]
    job_class = random.choice(job_classes)
    name = random.choice(["Alice", "Bob", "Cecilia", "David", "Eve", "Frank", "Grace", "Helen"])
    s = random.randint(2, 5)
    v = random.randint(2, 5)
    ag = random.randint(2, 5)
    d = random.randint(2, 5)
    i = random.randint(2, 5)
    level = random.randint(1, 5)
    return job_class(name, level, s, v, ag, d, i).create_character()

def gacha_draw_equipment():
    equipment_classes = [excalibur, thors_hammer, shild, book, ring]
    equipment_class = random.choice(equipment_classes)
    level = random.randint(1, 5)
    return equipment_class(level).create_equipment()
