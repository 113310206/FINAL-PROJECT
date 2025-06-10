from rpg_game.src.display import DisplaySystem  # 匯入 DisplaySystem

class Team:
    def __init__(self):
        from rpg_game.src.backpack import Backpack  # 動態匯入
        self.members = []
        self.coin = 1000
        self.exp = 0
        self.total_exp = 0
        self.exp_to_next_level = 500
        self.backpack = Backpack(self)  # 傳入 self 作為 team 參數

    def add_coin(self, amount):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        self.coin += amount
        DisplaySystem.show_message(f"The team gained {amount} coins! Total coins: {self.coin}")

    def spend_coin(self, amount):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        if self.coin >= amount:
            self.coin -= amount
            DisplaySystem.show_message(f"Spent {amount} coins. Remaining coins: {self.coin}")
        else:
            DisplaySystem.show_message("Not enough coins.")

    def add_exp(self, amount):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        self.exp += amount
        self.total_exp += amount
        DisplaySystem.show_message(f"The team gained {amount} EXP! Total EXP: {self.exp}/{self.exp_to_next_level}")
        if self.exp >= self.exp_to_next_level:
            self.level_up_team()

    def level_up_team(self):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        DisplaySystem.show_message("The team has leveled up! Distributing level-ups to all members.")
        for member in self.members:
            member.level_up()

    def recruit(self, character):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        if len(self.members) < 4:
            self.members.append(character)
            DisplaySystem.show_message(f"{character.name} 加入隊伍！")
        else:
            DisplaySystem.show_message("隊伍已滿，無法招募。")

    def fire(self, name):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        for m in self.members:
            if m.name == name:
                self.members.remove(m)
                DisplaySystem.show_message(f"{name} 已被移出隊伍。")
                return
        DisplaySystem.show_message("找不到該角色。")

    def change_position(self, name, pos):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        for m in self.members:
            if m.name == name:
                if pos not in ("front", "mid", "back"):
                    DisplaySystem.show_message("位置只能是 front/mid/back")
                    return
                m.position = pos
                DisplaySystem.show_message(f"{name} 位置調整為 {pos}。")
                return
        DisplaySystem.show_message("找不到該角色。")

    def show_positions(self):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        positions = "\n".join([f"{member.name}: {member.position}" for member in self.members])
        DisplaySystem.show_message(f"=== Positions ===\n{positions}\n=================")

    def add_member(self, character):
        if len(self.members) < 4:
            self.members.append(character)
            DisplaySystem.show_message(f"{character.name} 加入隊伍！")  # 使用 DisplaySystem
        else:
            DisplaySystem.show_message("隊伍已滿，無法加入更多隊員。")

    def print_positions(self):
        self.show_positions()

    def add_character(self, character):
        """新增角色到隊伍並設置 team 屬性"""
        self.members.append(character)
        character.team = self  # 設置角色的 team 屬性
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        DisplaySystem.show_message(f"{character.name} 已加入隊伍！")

