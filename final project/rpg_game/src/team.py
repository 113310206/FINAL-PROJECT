from .display import DisplaySystem
from .backpack import Backpack

class Team:
    def __init__(self):
        self.members = []
        self.coin = 1000
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