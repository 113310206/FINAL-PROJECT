FIRE = 1
WATER = 2
WOOD = 3

class Monster:
    def __init__(self, name, hp, attack, skills=None, behavior=None, element=None):
        self.element = element or FIRE  # 默認值改為 FIRE
        if self.element not in [FIRE, WATER, WOOD]:
            raise ValueError("Invalid element. Must be FIRE, WATER, or WOOD.")
        self.name = name
        self.hp = hp
        self.attack = attack
        self.skills = skills or []
        self.behavior = behavior or "normal"  # e.g. "berserk", "heal", etc.
        self.job = type("Job", (), {"job_name": "怪物"})()  # 讓 monster 有 job 屬性且 job_name 為"怪物"

    def is_alive(self):
        return self.hp > 0

    def act(self, team):
        from rpg_game.src.display import DisplaySystem, RED, GREEN, BLUE  # 動態匯入顏色
        if self.behavior == "berserk" and self.hp < 100:
            DisplaySystem.show_message(f"{self.name} enters a berserk state, increasing attack!", color=RED)
            self.attack *= 2
            self.behavior = "normal"
        elif self.behavior == "heal" and self.hp < 100:
            DisplaySystem.show_message(f"{self.name} heals itself!", color=GREEN)
            self.hp += 50

        if self.skills and self.is_alive():
            skill = self.skills[0]
            DisplaySystem.show_message(f"{self.name} uses skill: {skill.name}!", color=BLUE)
            for member in team.members:
                if member.is_alive():
                    member.hp -= skill.damage
                    DisplaySystem.show_message(f"{member.name} takes {skill.damage} damage!", color=RED)

    def print_status(self):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        DisplaySystem.show_message(f"{self.name} - HP: {self.hp}, Attack: {self.attack}, Behavior: {self.behavior}, Element: {self.element or 'None'}")