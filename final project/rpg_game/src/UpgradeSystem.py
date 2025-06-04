from rpg_game.src.equipment import Equipment  # 確保匯入 Equipment 類型
from rpg_game.src.character import Character  # 確保匯入 Character 類型
from rpg_game.src.backpack import Backpack  # 確保匯入 Backpack 類型

class UpgradeSystem:
    @staticmethod
    def level_up(character):
        # 升級角色等級並提升六屬性
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

        # 提升六屬性
        character.str += 1
        character.vit += 1
        character.agl += 1
        character.dex += 1
        character.intel += 1

        print(f"{character.name} 升級到等級 {character.level}！六屬性提升：STR+1, VIT+1, AGL+1, DEX+1, INT+1")

    @staticmethod
    def upgrade_skill(character, skill_name):
        # 升級角色技能
        if character.skill_tree and skill_name in character.skill_tree.levels:
            character.skill_tree.levels[skill_name] += 1
            print(f"{skill_name} 升級到等級 {character.skill_tree.levels[skill_name]}！")
        else:
            print("技能不存在或角色沒有技能樹。")

    @staticmethod
    def upgrade_equipment(equipment):
        # 升級裝備等級
        if hasattr(equipment, "level"):
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
                for idx, member in enumerate(team.members):
                    print(f"{idx + 1}. {member.name} (Lv.{member.level})")
                member_idx = int(input("輸入角色編號: ")) - 1
                if 0 <= member_idx < len(team.members):
                    member = team.members[member_idx]
                    UpgradeSystem.level_up(member)
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
                for idx, member in enumerate(team.members):
                    print(f"{idx + 1}. {member.name} (Lv.{member.level})")
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
                        member.str += 1
                        print(f"{member.name} 的 STR 提升了 1 點！")
                        input("按 Enter 繼續...")
                    elif attr_choice == "2":
                        member.vit += 1
                        print(f"{member.name} 的 VIT 提升了 1 點！")
                        input("按 Enter 繼續...")
                    elif attr_choice == "3":
                        member.agl += 1
                        print(f"{member.name} 的 AGL 提升了 1 點！")
                        input("按 Enter 繼續...")
                    elif attr_choice == "4":
                        member.dex += 1
                        print(f"{member.name} 的 DEX 提升了 1 點！")
                        input("按 Enter 繼續...")
                    elif attr_choice == "5":
                        member.intel += 1
                        print(f"{member.name} 的 INT 提升了 1 點！")
                        input("按 Enter 繼續...")
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
                item_idx = int(input("輸入物品編號: ")) - 1
                if 0 <= item_idx < len(team.backpack.items):
                    item_name = list(team.backpack.items.keys())[item_idx]
                    equipment = team.backpack.items[item_name]['item']
                    # 修正：檢查物品是否為 Equipment 類型
                    if isinstance(equipment, Equipment):
                        UpgradeSystem.upgrade_equipment(equipment)
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
