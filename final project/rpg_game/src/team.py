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

