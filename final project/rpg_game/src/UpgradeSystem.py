from rpg_game.src.equipment import Equipment  # 確保匯入 Equipment 類型
from rpg_game.src.character import Character  # 確保匯入 Character 類型
from rpg_game.src.backpack import Backpack  # 確保匯入 Backpack 類型

class UpgradeSystem:
    # 自訂每個等級升級所需的經驗值
    EXP_TABLE = {
        1: 100,
        2: 150,
        3: 210,
        4: 280,
        5: 360,
        # 可以繼續添加更多等級的經驗值需求
    }

    @staticmethod
    def calculate_exp_to_next_level(level):
        # 根據自訂表格計算升級所需經驗值，若未定義則使用預設公式
        return UpgradeSystem.EXP_TABLE.get(level, 100 + level * 10)

    @staticmethod
    def level_up(team, character):
        # 檢查總經驗值是否足夠升級
        
        if team.total_exp < character.exp_to_next_level:
            print(f"隊伍的總經驗值不足，無法升級！需要 {character.exp_to_next_level - team.total_exp} 額外經驗值。")
            return

        # 升級角色等級並提升六屬性
        
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

        # 提升六屬性
        character.str += 1
        character.vit += 1
        character.agl += 1
        character.dex += 1
        character.intel += 1

        print(f"{character.name} 升級到等級 {character.level}！六屬性提升：STR+1, VIT+1, AGL+1, DEX+1, INT+1")

    @staticmethod
    def upgrade_attribute(team, character, attribute, cost=50):
        # 檢查總經驗值是否足夠提升屬性
        if team.total_exp < cost:
            print(f"隊伍的總經驗值不足，無法提升屬性！需要 {cost - team.total_exp} 額外經驗值。")
            return

        # 提升屬性
        team.total_exp -= cost
        setattr(character, attribute, getattr(character, attribute) + 1)
        print(f"{character.name} 的 {attribute.upper()} 提升了 1 點！")

    @staticmethod
    def upgrade_equipment(team, equipment, cost=100):
        # 檢查總經驗值是否足夠升級裝備
        if team.total_exp < cost:
            print(f"隊伍的總經驗值不足，無法升級裝備！需要 {cost - team.total_exp} 額外經驗值。")
            return

        # 升級裝備等級
        if hasattr(equipment, "level"):
            team.total_exp -= cost
            equipment.level += 1
            print(f"{equipment.name} 升級到等級 {equipment.level}！")
        else:
            print("無法升級此裝備。")

def upgrade_menu(team):
    while True:
        from rpg_game.src.display import DisplaySystem  # 確保顯示功能可用
        DisplaySystem.show_upgrade_menu()  # 顯示升級選單
        choice = input("選擇操作: ").strip()
        if choice == "1":
            try:
                print("選擇角色：")
                print(f"隊伍總經驗值: {team.total_exp}")
                for idx, member in enumerate(team.members):
                    print(f"{idx + 1}. {member.name} (Lv.{member.level}, EXP to Next Level: {member.exp_to_next_level})")
                member_idx = int(input("輸入角色編號: ")) - 1
                if 0 <= member_idx < len(team.members):
                    member = team.members[member_idx]
                    UpgradeSystem.level_up(team, member)
                    input("按 Enter 繼續...")
                    DisplaySystem.clear_screen()
                else:
                    print("無效的角色選擇。\n")
                    input("按 Enter 繼續...")
            except ValueError:
                print("輸入錯誤，請輸入有效的編號。\n")
                input("按 Enter 繼續...")
        elif choice == "2":
            try:
                print("選擇角色：")
                print(f"隊伍總經驗值: {team.total_exp}")
                for idx, member in enumerate(team.members):
                    print(f"{idx + 1}. {member.name}")
                member_idx = int(input("輸入角色編號: ")) - 1
                if 0 <= member_idx < len(team.members):
                    member = team.members[member_idx]
                    print("選擇要提升的屬性：")
                    print("1. STR (力量)")
                    print("2. VIT (體力)")
                    print("3. AGL (敏捷)")
                    print("4. DEX (技巧)")
                    print("5. INT (智力)")
                    attr_choice = input("輸入屬性編號: ").strip()
                    if attr_choice == "1":
                        UpgradeSystem.upgrade_attribute(team, member, "str")
                    elif attr_choice == "2":
                        UpgradeSystem.upgrade_attribute(team, member, "vit")
                    elif attr_choice == "3":
                        UpgradeSystem.upgrade_attribute(team, member, "agl")
                    elif attr_choice == "4":
                        UpgradeSystem.upgrade_attribute(team, member, "dex")
                    elif attr_choice == "5":
                        UpgradeSystem.upgrade_attribute(team, member, "intel")
                    else:
                        print("無效的屬性選擇。\n")
                    input("按 Enter 繼續...")
                else:
                    print("無效的角色選擇。\n")
                    input("按 Enter 繼續...")
            except ValueError:
                print("輸入錯誤，請輸入有效的編號。\n")
                input("按 Enter 繼續...")
        elif choice == "3":
            try:
                DisplaySystem.show_backpack(team.backpack)
                if not team.backpack.items:
                    continue
                print(f"隊伍總經驗值: {team.total_exp}")
                item_idx = int(input("輸入物品編號: ")) - 1
                if 0 <= item_idx < len(team.backpack.items):
                    item_name = list(team.backpack.items.keys())[item_idx]
                    equipment = team.backpack.items[item_name]['item']
                    # 檢查物品是否為 Equipment 類型
                    if isinstance(equipment, Equipment):
                        UpgradeSystem.upgrade_equipment(team, equipment)
                    else:
                        print(f"{item_name} 不是可升級的裝備。\n")
                else:
                    print("無效的物品選擇。\n")
                input("按 Enter 繼續...")
            except ValueError:
                print("輸入錯誤，請輸入有效的編號。\n")
                input("按 Enter 繼續...")
        elif choice == "4":
            break
        else:
            print("無效的選擇，請輸入 1, 2, 3 或 4。\n")
            input("按 Enter 繼續...")
