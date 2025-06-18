GREEN = (0, 255, 0)

ELEMENTS = ["FIRE", "WATER", "WOOD"]

class Character:
    def __init__(self, name, level, str_attr, vit, agl, dex, intel, skill, element_skill, element=None, job=None, position="front", team=None):
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
        # 元素屬性系統
        self.original_element = element if element in ELEMENTS else "FIRE"
        self.element = self.original_element
        self.exp = 0
        self.exp_to_next_level = 100 + level ^ 3
        self.equipment = {'weapon': None, 'armor': None, 'accessory': None}
        self.job = job
        self.position = position
        self.damage_boost = 1
        self.skill_tree = None 
        self.team = team  # 新增 team 屬性，用於辨認隊友
        self.element_boost = False  # 初始化元素加成屬性

    def is_alive(self):
        return self.hp > 0

    def print(self):
        job_name = getattr(self.job, "job_name", None) or "No Job"
        print(f"{self.name} Lv {self.level} [{job_name}]")
        print(f"ATK: {self.attack_power} | HP: {self.hp}/{self.max_hp} | MP: {self.mp}/{self.max_mp} | Armor: {self.armor}/{self.max_armor}")
        print(f"Element: {self.element or 'None'} | EXP: {self.exp}/{self.exp_to_next_level}")
        print(f"位置: {self.position}")
        print("裝備：")
        for eq_type, eq in self.equipment.items():
            if eq:
                print(f"  {eq_type.capitalize()}: {eq.name} (Lv.{eq.level}, {eq.eq_type}) 屬性加成: {eq.stat_bonus}")
            else:
                print(f"  {eq_type.capitalize()}: 無")
        print("-" * 30)

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

    def upgrade_skill(self):
        if self.skill_tree:
            skill_name = input("輸入要升級的技能名稱：").strip()
            self.skill_tree.upgrade(skill_name)
        else:
            print("此角色沒有技能樹，無法升級技能。")

    def is_equipped(self, equipment_name):
        return any(eq and eq.name == equipment_name for eq in self.equipment.values())

    def overwrite_element(self, new_element):
        """直接覆蓋角色的元素屬性，不顯示訊息"""
        if new_element in ELEMENTS:
            self.element = new_element

    def reset_element(self):
        """重置角色元素屬性為原始元素"""
        self.element = self.original_element

    def take_damage(self, damage):
        """處理閃避、減傷與傷害結算。dex 越高越容易閃避攻擊，護甲減傷。"""
        import random
        dodge_chance = min(0.5, self.dex * 0.03)  # 最高 50% 閃避率，每點 dex 增加 3%
        if random.random() < dodge_chance:
            from rpg_game.src.display import DisplaySystem
            DisplaySystem.show_message(f"{self.name} dodged the attack!")
            return False  # 沒有受傷

        # 護甲減傷系統：護甲值大於0時減少80%傷害
        if self.armor > 0:
            reduced_damage = int(damage * 0.2)
            armor_cost = int(damage * 0.8)
            self.armor = max(0, self.armor - armor_cost)
            self.hp -= reduced_damage
            from rpg_game.src.display import DisplaySystem
            DisplaySystem.show_message(f"{self.name} blocked part of the damage, reducing it to {reduced_damage} and consuming {armor_cost} armor points!")
        else:
            self.hp -= damage
        return True  # 受傷