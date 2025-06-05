from rpg_game.src.character import Character
from rpg_game.src.job import Warrior, Mage, Archer, Healer, Tank, KingKnight, Shooter
from rpg_game.src.equipment import Equipment
from rpg_game.src.skill import Skill, ElementalSkill, SupportElementalSkill
from rpg_game.src.team import Team, team_menu  # 更新匯入，包含 team_menu
from rpg_game.src.display import DisplaySystem
from rpg_game.src.store import store
from rpg_game.src.backpack import Backpack, backpack_menu
from rpg_game.src.UpgradeSystem import UpgradeSystem, upgrade_menu
import random
import time

class Monster:
    def __init__(self, hp, attack, element=None, skills=None, behavior=None):
        self.hp = hp
        self.attack = attack
        self.element = element
        self.skills = skills or []
        self.behavior = behavior or "normal"
        self.name = "怪物"
        self.job = type("Job", (), {"job_name": "怪物"})()  # 讓 monster 有 job 屬性且 job_name 為"怪物"

    def print(self):
        DisplaySystem.show_monster(self)

    def try_crit(self):
        return random.random() < 0.25

    def act(self, team):
        # 怪物行為模式
        if self.behavior == "berserk" and self.hp < 100:
            print("怪物進入狂暴狀態，攻擊力提升！")
            self.attack *= 2
            self.behavior = "normal"
        elif self.behavior == "heal" and self.hp < 100:
            print("怪物自我治療！")
            self.hp += 50
        else:
            # 怪物攻撃（技能或普通攻擊，只執行一次）
            if self.skills and random.random() < 0.5:
                skill = random.choice(self.skills)
                print(f"怪物使用技能：{skill.name}！")
                for m in team.members:
                    if m.is_alive():
                        m.hp -= skill.damage
                DisplaySystem.show_monster_attack_message(self, None, skill.damage)
            else:
                crit = self.try_crit()
                element_boost = any(m.element == self.element for m in team.members if m.is_alive())
                if random.random() < 0.5:  # 隨機選擇單一目標攻擊或全體攻擊
                    target = random.choice([m for m in team.members if m.is_alive()])
                    total_damage = self.attack * (2 if crit else 1) * (1.5 if element_boost else 1)
                    target.hp -= total_damage
                    DisplaySystem.show_monster_attack_message(self, target, total_damage, crit=crit, element_boost=element_boost)
                else:
                    print("怪物進行全體攻擊！")
                    total_damage = (self.attack // 2) * (2 if crit else 1) * (1.5 if element_boost else 1)
                    for m in team.members:
                        if m.is_alive():
                            m.hp -= total_damage
                    DisplaySystem.show_monster_attack_message(self, None, total_damage, crit=crit, element_boost=element_boost)

class BonusSystem:
    @staticmethod
    def apply_equipment_bonus(character, equipment, reverse=False):
        factor = -1 if reverse else 1
        for k, v in equipment.stat_bonus.items():
            if hasattr(character, k):
                setattr(character, k, getattr(character, k) + factor * v * equipment.level)

    @staticmethod
    def apply_weapon_bonus(character, weapon):
        if weapon.eq_type == "weapon":
            character.attack_power += weapon.stat_bonus.get("str", 0) * weapon.level

    @staticmethod
    def apply_job_bonus(character, job):
        for k, v in job.stat_bonus.items():
            if hasattr(character, k):
                setattr(character, k, getattr(character, k) + v)

    @staticmethod
    def reset_equipment_bonus(character):
        for eq in character.equipment.values():
            if eq:
                BonusSystem.apply_equipment_bonus(character, eq, reverse=True)

    @staticmethod
    def apply_position_bonus(character):
        # 定義站位加成
        position_bonus = {
            "front": {"str": 2, "vit": 2},
            "mid": {"dex": 2, "agl": 2},
            "back": {"intel": 3, "mp": 5}
        }
        if character.position in position_bonus:
            for k, v in position_bonus[character.position].items():
                if hasattr(character, k):
                    setattr(character, k, getattr(character, k) + v)
            print(f"{character.name} 在 {character.position} 位置獲得加成：{position_bonus[character.position]}")

    @staticmethod
    def reset_position_bonus(character):
        # 定義站位加成（重置時使用）
        position_bonus = {
            "front": {"str": 2, "vit": 2},
            "mid": {"dex": 2, "agl": 2},
            "back": {"intel": 3, "mp": 5}
        }
        if character.position in position_bonus:
            for k, v in position_bonus[character.position].items():
                if hasattr(character, k):
                    setattr(character, k, getattr(character, k) - v)
            print(f"{character.name} 在 {character.position} 位置的加成已重置。")

def random_character(team):
    role = random.randint(1, 7)
    print("Enter character details (name, str, vit, agl, dex, intel): ")
    print("The total attribute points cannot exceed 15.")
    print("And the maximum value for each attribute is 10.")
    while True:
        name = input("Name: ").strip()
        try:
            s, v, ag, d, i = map(int, input("Attributes (str vit agl dex intel): ").split())
        except:
            print("Invalid input. Please try again.")
            continue
        if not name:
            print("Name cannot be empty. Please try again.")
        elif s + v + ag + d + i > 15:
            print("Total attribute points exceed 15. Please try again.")
        elif any(x > 10 or x < 0 for x in [s, v, ag, d, i]):
            print("Each attribute must be 0~10. Please try again.")
        else:
            break
    level = 3
    if role == 1:
        job_obj = Warrior(name, level, s, v, ag, d, i)
    elif role == 2:
        job_obj = Mage(name, level, s, v, ag, d, i)
    elif role == 3:
        job_obj = Archer(name, level, s, v, ag, d, i)
    elif role == 4:
        job_obj = Healer(name, level, s, v, ag, d, i)
    elif role == 5:
        job_obj = Tank(name, level, s, v, ag, d, i)
    elif role == 6:
        job_obj = KingKnight(name, level, s, v, ag, d, i)
    else:
        job_obj = Shooter(name, level, s, v, ag, d, i)
    new_character = job_obj.create_character()
    team.backpack.add_item(name)  # 將角色放入背包
    print(f"{name} has been added to the backpack.\n")

def get_valid_choice():
    while True:
        choice = input().strip().upper()
        if choice in ("Y", "N"):
            return choice == "Y"
        print("Invalid input. Please enter 'Y' or 'N'.")

class Battle:
    def __init__(self, team, monster):
        self.team = team
        self.monster = monster

    def start(self):
        while True:
            # 每回合開始都顯示隊伍與怪物狀態
            DisplaySystem.show_battle_status(self.team, self.monster)
            # 玩家回合
            for idx, member in enumerate(self.team.members):
                if not member.is_alive():
                    continue
                while True:  # 增加循環以保持角色動作
                    # 每個角色行動前都顯示隊伍與怪物狀態
                    DisplaySystem.show_battle_status(self.team, self.monster)
                    print(f"\nIt's {member.name}'s turn.")
                    print("1. Normal Attack\n2. Use Skill" 
                          "\n3. Use Element Skill   " 
                          "\n4. Use Element Skill on Teammate   " 
                          "\n5. Upgrade Skill       " 
                          "\n6. Equip/Unequip" 
                          "\n7. View Backpack "
                          "\n8. Upgrade Syetem " 
                          "\n9. Skip Turn")
                    try:
                        action = int(input("Choose an action: "))
                    except ValueError:
                        print("Invalid input. Please enter a valid number between 1 and 9.")
                        input("（按 Enter 繼續）")
                        continue  # 不消耗回合，保持角色動作

                    if action == 1:
                        if isinstance(self.monster, member.__class__):  # 判斷是否是隊友
                            print(f"{member.name} cannot attack teammate {self.monster.name}.")
                        else:
                            crit = member.try_crit(self.monster)
                            total_damage = member.attack_power
                            if crit:
                                total_damage *= 2
                            DisplaySystem.show_attack_message(member, self.monster, total_damage, crit=crit)
                            self.monster.hp -= total_damage
                        break  # 結束循環，消耗回合
                    elif action == 2:
                        if member.skill:
                            crit = member.try_crit(self.monster)
                            total_damage = member.skill.damage
                            if crit:
                                total_damage *= 2
                            DisplaySystem.show_skill_use(member, member.skill, self.monster, total_damage, crit=crit)
                            self.monster.hp -= total_damage
                        break  # 結束循環，消耗回合
                    elif action == 3:
                        if member.element_skill:
                            crit = member.try_crit(self.monster)
                            # 判斷屬性相剋加成
                            element_boost = False
                            if member.element_skill.element and self.monster.element:
                                if member.element_skill.element == "FIRE" and self.monster.element == "WOOD":
                                    element_boost = True
                                elif member.element_skill.element == "WATER" and self.monster.element == "FIRE":
                                    element_boost = True
                                elif member.element_skill.element == "WOOD" and self.monster.element == "WATER":
                                    element_boost = True
                            total_damage = member.element_skill.damage
                            if crit:
                                total_damage *= 2
                            if element_boost:
                                total_damage *= 1.5
                            DisplaySystem.show_elementSkill_use(member, member.element_skill, self.monster, total_damage, crit=crit, element_boost=element_boost)
                            self.monster.hp -= total_damage
                        break  # 結束循環，消耗回合
                    elif action == 4:
                        teammates = [m for m in self.team.members if m.is_alive() and m != member]
                        if not teammates:
                            print("沒有可用的隊友進行祝福。\n")
                            continue
                        print("選擇一位隊友進行祝福：")
                        for i, t in enumerate(teammates):
                            print(f"{i+1}. {t.name}")
                        try:
                            t_idx = int(input("選擇隊友編號: ")) - 1
                            if 0 <= t_idx < len(teammates):
                                support_skill = SupportElementalSkill(member.element_skill.name, member.element_skill.cost, member.element_skill.element, member.element_skill.desc)
                                # 判斷屬性相同加成
                                element_boost = teammates[t_idx].element and support_skill.element and teammates[t_idx].element == support_skill.element
                                if element_boost:
                                    print("屬性相同！效果加倍！")
                                support_skill.use(member, teammates[t_idx])
                                DisplaySystem.show_elementSkill_use(member, support_skill, teammates[t_idx], 0, element_boost=element_boost)
                                print(f"{teammates[t_idx].name} 的屬性已被改變為 {support_skill.element}！")
                            else:
                                print("無效的隊友選擇。\n")
                        except ValueError:
                            print("輸入錯誤，請輸入有效的編號。\n")
                        break  # 結束循環，消耗回合
                    elif action == 5:
                        upgrade_menu(team)
                        continue  # 不消耗回合，保持角色動作
                    elif action == 6:
                        if not team.backpack.items:
                            print("The backpack is empty. No equipment available.")
                            input("（按 Enter 繼續）")
                            continue
                        print("1. 裝備 2. 卸下")
                        try:
                            sub = int(input("選擇: "))
                        except ValueError:
                            print("Invalid input. Please enter 1 or 2.")
                            input("（按 Enter 繼續）")
                            continue
                        if sub == 1:
                            DisplaySystem.show_backpack(team.backpack, pause=False)  # 傳入 pause=False
                            try:
                                item_idx = int(input("輸入物品編號: ")) - 1
                            except ValueError:
                                print("Invalid input. Please enter a valid number.")
                                input("（按 Enter 繼續）")
                                continue
                            if 0 <= item_idx < len(team.backpack.items):
                                item_name = list(team.backpack.items.keys())[item_idx]
                                equipment = team.backpack.items[item_name]['item']
                                if not isinstance(equipment, Equipment):
                                    print("選擇的物品不是裝備。\n")
                                    continue
                                member.equip(equipment)
                                BonusSystem.apply_weapon_bonus(member, equipment)
                                team.backpack.remove_item(item_name, 1)
                            else:
                                print("無效的物品選擇。\n")
                        elif sub == 2:
                            eq_type = input("輸入要卸下的裝備類型（weapon/armor/accessory）：")
                            member.unequip(eq_type)
                            if eq_type == "weapon":
                                BonusSystem.reset_equipment_bonus(member)
                        else:
                            print("Invalid choice. Please enter 1 or 2.")
                            input("（按 Enter 繼續）")
                        continue  # 不消耗回合，保持角色動作
                    elif action == 7:
                        DisplaySystem.show_backpack(team.backpack)
                        continue  # 不消耗回合，保持角色動作
                    elif action == 8:
                        upgrade_menu(team)
                    elif action == 9:
                        print(f"{member.name} skipped their turn.\n")
                        input("（按 Enter 繼續）")
                        break  # 結束循環，消耗回合
                    else:
                        print("Invalid choice. Please enter a number between 1 and 9.")
                        input("（按 Enter 繼續）")
                        continue  # 不消耗回合，保持角色動作
                
                if self.monster.hp <= 0:
                    DisplaySystem.show_team(self.team, pause=False)
                    exp_reward = 1000
                    coin_reward = 100
                    print("\nThe team has defeated the monster!\nVictory!\n")
                    print(f"Rewards: {exp_reward} EXP, {coin_reward} Coins")
                    self.team.add_exp(exp_reward)  # 更新總經驗值
                    self.team.total_exp += exp_reward  # 更新總經驗值累積
                    self.team.add_coin(coin_reward)
                    input("（按 Enter 繼續）")
                    return
                
                # 每個角色行動後顯示隊伍與怪物狀態
                DisplaySystem.show_team(self.team, pause=False)
                DisplaySystem.show_monster(self.monster)
            # 怪物回合
            print("\nMonster's turn!\n")
            # 怪物攻擊只顯示一次
            self.monster.act(self.team)
            # 回合結束重置所有角色的攻擊加成
            for m in self.team.members:
                if hasattr(m, "damage_boost") and m.damage_boost > 1:
                    m.damage_boost = 1
            if all(not m.is_alive() for m in self.team.members):
                print("\nThe team has been defeated...\nGAME OVER\n")
                DisplaySystem.show_team(self.team)
                DisplaySystem.show_monster(self.monster)
                input("（按 Enter 退出）")
                return
            # 每回合結束後顯示隊伍與怪物狀態
            DisplaySystem.show_team(self.team, pause=False)
            DisplaySystem.show_monster(self.monster)

if __name__ == "__main__":
    team = Team()
    print("Welcome to the RPG Game!")
    print("You will start with a Warrior character named 'YOU'.")
    
    # 創建初始角色
    archer1 = Archer("1", 1, 5, 5, 5, 5, 5)  # 創建 Archer 實例
    team.add_character(archer1.create_character())  # 調用 create_character 方法
    warrior= Warrior("2", 1, 5, 5, 5, 5, 5)  # 創建第二個 Archer 實例
    team.add_character(warrior.create_character())  # 調用 create_character 方法
    
    while True:
        DisplaySystem.show_main_menu()
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            DisplaySystem.show_team(team, pause=True)
        elif choice == "2":
            monster = Monster(5, 1, "WATER", [Skill("Fireball", 1, 1)], "berserk")
            battle = Battle(team, monster)
            battle.start()
        elif choice == "3":
            store(team)
        elif choice == "4":
            team_menu(team)  # 改為從 team 模組中調用
        elif choice == "5":
            backpack_menu(team)
        elif choice == "6":
            upgrade_menu(team)
        elif choice == "7":
            print("Exiting game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
            input("（按 Enter 繼續）")


