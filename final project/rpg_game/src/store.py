import random
from .job import Warrior, Mage, Archer, Healer, Tank, KingKnight, Shooter  # 匯入 JobBase 和具體職業類型
from .skill import Skill, ElementalSkill
from .equipment import Equipment, EquipmentType, excalibur, thors_hammer, shild, book, ring  # 匯入 EquipmentType 和具體裝備類型
from .display import DisplaySystem 
from .backpack import Backpack  # 確保匯入 Backpack 類別

def store(team):
    # 確保 team.backpack 已初始化一次
    if not hasattr(team, 'backpack') or not isinstance(team.backpack, Backpack):
        team.backpack = Backpack()
        print("背包已初始化。")
    
    while True:
        DisplaySystem.show_store_menu(team)  # 使用 DisplaySystem 顯示商店功能
        choice = int(input("Choose an option: "))
        DisplaySystem.clear_screen()  # 清除螢幕，避免訊息被刷掉
        if choice == 6:
            print("Exiting store...\n")
            input("（按 Enter 繼續）")  # 暫停
            break
        if choice in [1, 2, 3, 4, 5]:
            if team.coin < 50:
                print("Not enough coins.\n")
                input("（按 Enter 繼續）")  # 暫停
                continue
            attribute_map = {
                1: "STR",
                2: "VIT",
                3: "AGL",
                4: "DEX",
                5: "INT"
            }
            attribute_name = attribute_map[choice]
            # 選擇要加點的角色
            print("Select a member to apply the attribute point:")
            for idx, member in enumerate(team.members):
                print(f"{idx + 1}. {member.name}")
            m_idx = int(input("輸入角色編號: ")) - 1
            if 0 <= m_idx < len(team.members):
                member = team.members[m_idx]
                team.spend_coin(50)
                # 屬性欄位在角色中以小寫呈現，例如 member.str
                current_value = getattr(member, attribute_name.lower())
                setattr(member, attribute_name.lower(), current_value + 1)
                print(f"{member.name}'s {attribute_name} increased by 1!")
                input("（按 Enter 繼續）")  # 暫停
            else:
                print("Invalid member selection.\n")
                input("（按 Enter 繼續）")
        elif choice == 7:  # Gacha Draw
            if team.coin < 200:
                print("Not enough coins for gacha.\n")
                input("（按 Enter 繼續）")  # 暫停
                continue
            pool_choice = input("Choose a pool: 1 for Character Pool, 2 for Equipment Pool: ").strip()
            if pool_choice == "1":
                gacha_character = gacha_draw_character()
                team.backpack.add_item(gacha_character, 1)  # 將角色直接存入背包
                print(f"Gacha success! {gacha_character.name} has been added to the backpack!\n")
            elif pool_choice == "2":
                gacha_equipment = gacha_draw_equipment()
                team.backpack.add_item(gacha_equipment, 1)  # 將裝備直接存入背包
                print(f"Gacha success! {gacha_equipment.name} has been added to the backpack!\n")
            else:
                print("Invalid pool choice.\n")
                continue
            team.spend_coin(200)
            input("（按 Enter 繼續）")  # 暫停
        else:
            print("Invalid choice.\n")
            input("（按 Enter 繼續）")  # 暫停

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
    return equipment_class(level).create_equipment()  # 使用 create_equipment 方法生成裝備
