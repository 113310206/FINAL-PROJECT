from .skill import Skill, ElementalSkill

class Character:
    def __init__(self, name, level, str_attr, vit, agl, dex, intel, skill, element_skill, element=None, job=None, position="front"):
        self.name = name
        self.level = level
        self.str = str_attr
        self.vit = vit
        self.agl = agl
        self.dex = dex
        self.intel = intel
        self.hp = 20 + vit * 20
        self.max_hp = self.hp
        self.mp = 50 + intel * 50
        self.max_mp = self.mp
        self.armor = 10 + dex * 20
        self.max_armor = self.armor
        self.attack_power = 10 + str_attr * 30
        self.skill = skill
        self.element_skill = element_skill
        self.element = element
        self.exp = 0
        self.exp_to_next_level = 100 + level ^ 3
        self.equipment = {'weapon': None, 'armor': None, 'accessory': None}
        self.job = job
        self.position = position
        self.damage_boost = 1
        self.skill_tree = None  # �Y�D�{�����Ψ�i�ɤW

    def is_alive(self):
        return self.hp > 0

    def print(self):
        # 修正亂碼，並避免依賴 job 物件的 name
        job_name = getattr(self.job, "job_name", None) or "無職業"
        print(f"{self.name} Lv {self.level} [{job_name}]")
        print(f"ATK: {self.attack_power} | HP: {self.hp}/{self.max_hp} | MP: {self.mp}/{self.max_mp} | Armor: {self.armor}/{self.max_armor}")
        print(f"Element: {self.element or 'None'} | EXP: {self.exp}/{self.exp_to_next_level}")
        print(f"位置: {self.position}")
        print("裝備：")
        for eq in self.equipment.values():
            if eq:
                print(f"  {eq.name} (Lv.{eq.level}, {eq.eq_type}) 屬性加成: {eq.stat_bonus}")
        print("-" * 30)

    def equip(self, equipment):
        # 動態匯入避免循環依賴
        from .equipment import Equipment  # 動態匯入
        if not isinstance(equipment, Equipment):
            print("Invalid equipment type.")
            return
        if self.equipment.get(equipment.eq_type):  # 檢查是否已有同類型裝備
            self.unequip(equipment.eq_type)
        self.equipment[equipment.eq_type] = equipment
        equipment.equip(self)
        print(f"{self.name} 裝備了 {equipment.name} (Lv.{equipment.level})！")

    def unequip(self, eq_type):
        eq = self.equipment.get(eq_type)
        if eq:
            if hasattr(eq, "name"):
                eq.unequip(self)
            self.equipment[eq_type] = None
            print(f"{self.name} 卸下了 {eq.name} (Lv.{eq.level})！")
        else:
            print(f"No equipment of type {eq_type} to unequip.")

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.exp -= self.exp_to_next_level
        self.level += 1
        self.exp_to_next_level = 100 + self.level * 5
        self.max_hp = int(self.max_hp * 1.1)
        self.hp = self.max_hp
        self.max_mp = int(self.max_mp * 1.1)
        self.mp = self.max_mp
        self.attack_power = int(self.attack_power * 1.1)
        self.max_armor = int(self.max_armor * 1.1)
        self.armor = self.max_armor

    def attack(self, target):
        damage = self.attack_power
        target.hp -= damage

    def try_crit(self, target):
        import random
        if random.random() < 0.3:
            damage = int(self.attack_power * 2)
            target.hp -= damage
            print(f"{self.name} 發動了暴擊！對 {target.name} 造成 {damage} 點傷害！")
            return True
        else:
            return False

    def use_skill(self, target):
        if self.skill:
            self.skill.use(self, target)

    def use_elemental_skill(self, target):
        if self.element_skill:
            self.element_skill.use(self, target)

    def upgrade_skill(self):
        if self.skill_tree:
            skill_name = input("輸入要升級的技能名稱：").strip()
            self.skill_tree.upgrade(skill_name)
        else:
            print("此角色沒有技能樹，無法升級技能。")


