class Monster:
    def __init__(self, name, hp, attack, skills=None, behavior=None):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.skills = skills or []
        self.behavior = behavior or "normal"  # e.g. "berserk", "heal", etc.
        self.job = type("Job", (), {"job_name": "怪物"})()  # 讓 monster 有 job 屬性且 job_name 為"怪物"

    def is_alive(self):
        return self.hp > 0

    def act(self, team):
        # Implement monster behavior during battle
        if self.behavior == "berserk" and self.hp < 100:
            print(f"{self.name} enters a berserk state, increasing attack!")
            self.attack *= 2
            self.behavior = "normal"
        elif self.behavior == "heal" and self.hp < 100:
            print(f"{self.name} heals itself!")
            self.hp += 50
        
        # Randomly use a skill if available
        if self.skills and self.is_alive():
            skill = self.skills[0]
            print(f"{self.name} uses skill: {skill.name}!")
            for member in team.members:
                if member.is_alive():
                    member.hp -= skill.damage
                    print(f"{member.name} takes {skill.damage} damage!")

    def print_status(self):
        print(f"{self.name} - HP: {self.hp}, Attack: {self.attack}, Behavior: {self.behavior}")