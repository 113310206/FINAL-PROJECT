import pygame
FIRE = 1
WATER = 2
WOOD = 3

class Monster:
    def __init__(self, hp, attack, element=None, skills=None, behavior=None, round_number=1):
        # 檢查元素是否合法（允許 None 或 "FIRE", "WATER", "WOOD"）
        valid_elements = (None, "FIRE", "WATER", "WOOD")
        if element not in valid_elements:
            raise ValueError("Invalid element. Must be FIRE, WATER, or WOOD.")
        self.hp = hp + pow(round_number,2) *50  # 每輪增加生命值
        self.attack = attack + pow(round_number, 2)*5  # 每輪增加攻擊力
        self.element = element
        self.skills = skills or []
        self.behavior = behavior or "normal"
        self.name = f"怪物 (Round {round_number})"
        self.job = type("Job", (), {"job_name": "怪物"})()  # 讓 monster 有 job 屬性且 job_name 為"怪物"

    def is_alive(self):
        return self.hp > 0

    def act(self, team):
        from rpg_game.src.display import DisplaySystem, RED, GREEN, BLUE, battle  # 只匯入顏色與 battle
        # 直接用 DisplaySystem.screen 畫圖，並用固定座標
        def extra_draw():
            screen = DisplaySystem.screen if hasattr(DisplaySystem, "screen") else None
            if screen:
                # 若 display.py 有 image_c1/image_boss 可用就用，否則略過
                try:
                    from rpg_game.src.display import image_c1, image_boss
                    screen.blit(image_c1, (450, 400))
                    screen.blit(image_boss, (850, 300))
                except ImportError:
                    pass

        if self.behavior == "berserk" and self.hp < 100:
            DisplaySystem.show_message(
                f"{self.name} enters a berserk state, increasing attack!", color=RED,
                background=battle,
                extra_draw=extra_draw
            )
            pygame.time.wait(1200)  # 等待1秒
            self.attack *= 2
            self.behavior = "normal"
        elif self.behavior == "heal" and self.hp < 100:
            DisplaySystem.show_message(
                f"{self.name} heals itself!", color=GREEN,
                background=battle,
                extra_draw=extra_draw
            )
            pygame.time.wait(1200)
            self.hp += 50

        if self.skills and self.is_alive():
            skill = self.skills[0]
            DisplaySystem.show_message(
                f"{self.name} uses skill: {skill.name}!", color=BLUE,
                background=battle,
                extra_draw=extra_draw
            )
            pygame.time.wait(1200)
            for member in team.members:
                if member.is_alive():
                    member.hp -= skill.damage
                    DisplaySystem.show_message(
                        f"{member.name} takes {skill.damage} damage!", color=RED,
                        background=battle,
                        extra_draw=extra_draw
                    )
                    pygame.time.wait(1200)
    def print_status(self):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        DisplaySystem.show_message(f"{self.name} - HP: {self.hp}, Attack: {self.attack}, Behavior: {self.behavior}, Element: {self.element or 'None'}")
        pygame.time.wait(1200)  # 等待1秒