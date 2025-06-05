from .display import DisplaySystem
from .backpack import Backpack

class Team:
    def __init__(self):
        self.members = []
        self.coin = 1000
        self.exp = 0  # 全隊共享經驗值
        self.total_exp = 0  # 新增總經驗值參數
        self.exp_to_next_level = 500  # 初始化升級所需經驗值
        
        self.backpack = Backpack()  # 修正背包屬性初始化為 Backpack 類型

    def add_character(self, character):
        self.members.append(character)

    def add_coin(self, amount):
        self.coin += amount
        print(f"The team gained {amount} coins! Total coins: {self.coin}")

    def spend_coin(self, amount):
        if self.coin >= amount:
            self.coin -= amount
            print(f"Spent {amount} coins. Remaining coins: {self.coin}")
        else:
            print("Not enough coins.")

    def add_exp(self, amount):
        self.exp += amount
        self.total_exp += amount  # 更新總經驗值
        print(f"The team gained {amount} EXP! Total EXP: {self.exp}/{self.exp_to_next_level}")
        print(f"Total EXP accumulated: {self.total_exp}")  # 顯示總經驗值
        if self.exp >= self.exp_to_next_level:
            self.level_up_team()

    def level_up_team(self):
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)  # 升級所需經驗值增加
        print("The team has leveled up! Distributing level-ups to all members.")
        for member in self.members:
            member.level_up()

    def recruit(self, character):
        if len(self.members) < 4:
            self.members.append(character)
            print(f"{character.name} 加入隊伍！")
        else:
            print("隊伍已滿，無法招募。")

    def fire(self, name):
        for m in self.members:
            if m.name == name:
                self.members.remove(m)
                print(f"{name} 已被移出隊伍。")
                return
        print("找不到該角色。")

    def change_position(self, name, pos):
        for m in self.members:
            if m.name == name:
                if pos not in ("front", "mid", "back"):
                    print("位置只能是 front/mid/back")
                    return
                # 重置舊位置加成（移除 BonusSystem 依賴）
                m.position = pos
                # 應用新位置加成（移除 BonusSystem 依賴）
                print(f"{name} 位置調整為 {pos}。")
                return
        print("找不到該角色。")

    def show_positions(self):
        print("\n=== Positions ===")
        for member in self.members:
            print(f"{member.name}: {member.position}")
        print("=================")

    def print_positions(self):
        DisplaySystem.show_positions(self)

    def add_member(self, character):
        if len(self.members) < 4:
            self.members.append(character)
            print(f"{character.name} 加入隊伍！")
        else:
            print("隊伍已滿，無法加入更多隊員。")

def team_menu(team):
    from rpg_game.src.display import DisplaySystem  # 確保顯示功能可用
    from rpg_game.src.character import Character  # 確保匯入 Character 類型
    while True:
        DisplaySystem.show_team_menu()  # 顯示 Team Management 選單
        choice = input("Choose an option: ").strip()
        if choice == "1":  # View Team
            DisplaySystem.show_team(team, pause=True)
        elif choice == "2":  # View Positions
            team.show_positions()
            input("（按 Enter 繼續）")
        elif choice == "3":  # Change Position
            try:
                name = input("Enter member name: ").strip()
                pos = input("Enter new position (front/mid/back): ").strip().lower()
                if pos not in ["front", "mid", "back"]:
                    print("Invalid position. Please enter 'front', 'mid', or 'back'.")
                    continue
                team.change_position(name, pos)
                print(f"{name}'s position changed to {pos}.")
            except Exception as e:
                print(f"Error: {e}")
            input("（按 Enter 繼續）")
        elif choice == "4":  # Fire Member
            try:
                name = input("Enter member name to fire: ").strip()
                team.fire(name)
                print(f"{name} has been removed from the team.")
            except Exception as e:
                print(f"Error: {e}")
            input("（按 Enter 繼續）")
        elif choice == "5":  # Add Member
            if not team.backpack.items:
                print("The backpack is empty. No members available to add.")
                input("（按 Enter 繼續）")
                continue
            try:
                DisplaySystem.show_backpack(team.backpack)
                try:
                    item_idx = int(input("Enter the item number to add as a member: ")) - 1
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    input("（按 Enter 繼續）")
                    continue
                if 0 <= item_idx < len(team.backpack.items):
                    item_name = list(team.backpack.items.keys())[item_idx]
                    character = team.backpack.items[item_name]['item']
                    if not isinstance(character, Character):
                        print("Selected item is not a character.")
                        input("（按 Enter 繼續）")
                        continue
                    if len(team.members) < 4:
                        team.add_member(character)
                        team.backpack.remove_item(item_name, 1)
                        print(f"{character.name} has been added to the team.")
                    else:
                        print("The team is full. Cannot add more members.")
                else:
                    print("Invalid item selection. Please try again.")
            except Exception as e:
                print(f"Error: {e}")
            input("（按 Enter 繼續）")
        elif choice == "6":  # Return to Main Menu
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            input("（按 Enter 繼續）")