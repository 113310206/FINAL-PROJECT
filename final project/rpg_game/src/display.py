import os
import time

class DisplaySystem:
    @staticmethod
    def clear_screen():
        # 清除螢幕
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show_character(character):
        # 只顯示一行簡明資訊，直接印出
        job_name = getattr(character, "job", None)
        if job_name and hasattr(job_name, "job_name"):
            job_name = job_name.job_name
        elif hasattr(character, "name"):
            job_name = character.name
        else:
            job_name = "無職業"
        # 修正：怪物沒有 equipment 屬性時不顯示裝備
        eqs = []
        if hasattr(character, "equipment") and isinstance(character.equipment, dict):
            eqs = [eq.name for eq in character.equipment.values() if eq]
        info = f"{getattr(character, 'name', '-')}" \
            f" | {job_name}" \
            f" | Lv{getattr(character, 'level', '-')}" \
            f" | ATK:{getattr(character, 'attack_power', getattr(character, 'attack', '-'))}" \
            f" HP:{getattr(character, 'hp', '-')}/{getattr(character, 'max_hp', '-') if hasattr(character, 'max_hp') else '-'}" \
            f" MP:{getattr(character, 'mp', '-')}/{getattr(character, 'max_mp', '-') if hasattr(character, 'max_mp') else '-'}" \
            f" Armor:{getattr(character, 'armor', '-')}/{getattr(character, 'max_armor', '-') if hasattr(character, 'max_armor') else '-'}" \
            f" | Elem:{getattr(character, 'element', 'None') or 'None'}" \
            f" | Pos:{getattr(character, 'position', '-')}"
        
        if eqs:
            info += f" | Eq:{','.join(eqs)}"
        print(info)

    @staticmethod
    def show_equipment(equipment):
        print(f"  {equipment.name} (Lv.{equipment.level}, {equipment.eq_type}) 屬性加成: {equipment.stat_bonus}")

    @staticmethod
    def show_monster(monster):
        DisplaySystem.show_character(monster)

    @staticmethod
    def show_attack_message(attacker, target, damage, crit=False, element_boost=False, skill_boost=False):
        DisplaySystem.clear_screen()
        message = f"{attacker.name} attacked {target.name}, dealing {damage} damage!"
        if crit:
            message += " [Critical Hit!]"
        if element_boost:
            message += " [Element Boost!]"
        if skill_boost:
            message += " [Skill Boost!]"
        print(message)
        input("（按 Enter 繼續）")

    @staticmethod
    def show_monster_attack_message(monster, target, damage, crit=False, element_boost=False):
        DisplaySystem.clear_screen()
        if target:
            message = f"{monster.name} attacked {target.name}, dealing {damage} damage!"
        else:
            message = f"{monster.name} performed a group attack, dealing {damage} damage to all members!"
        if crit:
            message += " [Critical Hit!]"
        if element_boost:
            message += " [Element Boost!]"
        print(message)
        input("（按 Enter 繼續）")

    @staticmethod
    def show_skill_boost(boost):
        print(f"Skill boost! Damage x{boost}")

    @staticmethod
    def show_skill_use(user, skill, target, damage, crit=False, element_boost=False):
        DisplaySystem.clear_screen()
        message = f"{user.name} used {skill.name}! {skill.desc}\nDealt {damage} damage to {target.__class__.__name__}!"
        if crit:
            message += " [Critical Hit!]"
        if element_boost:
            message += " [Element Boost!]"
        print(message)
        input("（按 Enter 繼續）")

    @staticmethod
    def show_elementSkill_use(user, skill, target, damage, crit=False, element_boost=False):
        DisplaySystem.clear_screen()
        message = f"{user.name} used {skill.name} ({skill.element})! {skill.desc}\nDealt {damage} damage to {target.__class__.__name__}!"
        if crit:
            message += " [Critical Hit!]"
        if element_boost:
            message += " [Element Boost!]"
        print(message)
        if skill.element:
            print(f"{target.name} is now affected by {skill.element} element.")
            input("（按 Enter 繼續）")
        if isinstance(target, user.__class__):
            print(f"{target.name} has been blessed by {skill.name}!")
            input("（按 Enter 繼續）")
    
    @staticmethod
    def show_main_menu():
        DisplaySystem.clear_screen()
        print("\n=== Main Menu ===")
        print("1. Show Team")
        print("2. Battle")
        print("3. Store")
        print("4. Team Management")
        print("5. Backpack")
        print("6. Exit Game")
    
    @staticmethod
    def show_battle_status(team, monster, pause=False):
        DisplaySystem.clear_screen()
        print("=== Battle Status ===")
        print("\nTeam Status:")
        DisplaySystem.show_team(team, pause=False)
        print("\nMonster Status:")
        DisplaySystem.show_monster(monster)
        print("=====================")
        if pause:
            input("（按 Enter 繼續）")
 
    @staticmethod
    def show_team(team, pause=False):
        DisplaySystem.clear_screen()
        print("=== Team Members ===")
        for member in team.members:
            DisplaySystem.show_character(member)
        print("=====================")
        if pause:
            input("（按 Enter 繼續）")

    @staticmethod
    def show_skill_tree(skill_tree):
        DisplaySystem.clear_screen()
        print("=== Skill Tree ===")
        for skill in skill_tree.skills:
            print(f"{skill.name} (Cost: {skill.cost}, Damage: {skill.damage}) - {skill.desc}")
        print("===================")
        input("（按 Enter 繼續）")

    @staticmethod
    def store(team):
        DisplaySystem.clear_screen()
        print("=== Store ===")
        print("1. Increase STR (50 coins)")
        print("2. Increase VIT (50 coins)")
        print("3. Increase AGL (50 coins)")
        print("4. Increase DEX (50 coins)")
        print("5. Increase INT (50 coins)")
        print("6. Exit Store")
        print("7. Buy Random Equipment (100 coins)")
        print("8. Gacha Draw (200 coins)")
        print(f"Current Coins: {team.coin}")
        print("================")
    
    @staticmethod
    def show_backpack(backpack):
        DisplaySystem.clear_screen()
        print("\n=== Backpack ===")
        if not backpack.items:
            print("The backpack is empty.")
        else:
            for item, quantity in backpack.items.items():
                print(f"{item}: {quantity}")
        print("================\n")
        input("（按 Enter 繼續）")  # 暫停，等待使用者按下 Enter

    @staticmethod
    def show_store_menu(team):
        DisplaySystem.clear_screen()
        print("=== Store ===")
        print("1. Increase STR (50 coins)")
        print("2. Increase VIT (50 coins)")
        print("3. Increase AGL (50 coins)")
        print("4. Increase DEX (50 coins)")
        print("5. Increase INT (50 coins)")
        print("6. Exit Store")
        print("7. Gacha Draw (200 coins)")  # 更新選項編號
        print(f"Current Coins: {team.coin}")
        print("================")
    
    @staticmethod
    def show_team_menu():
        DisplaySystem.clear_screen()
        print("\n=== Team Management ===")
        print("1. View Team")
        print("2. View Positions")
        print("3. Change Position")
        print("4. Fire Member")
        print("5. Add Member")
        print("6. Return to Main Menu")
        print("========================")
