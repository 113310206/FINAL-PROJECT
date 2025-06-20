import pygame
# 元素屬性定義
ELEMENTS = ["FIRE", "WATER", "WOOD"]

# 元素相剋規則
ELEMENT_ADVANTAGE = {
    ("FIRE", "WOOD"): True,
    ("WOOD", "WATER"): True,
    ("WATER", "FIRE"): True,
}

class Skill:
    def __init__(self, name, cost, damage, desc=""):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.desc = desc

    def use(self, user, target, background=None, extra_draw=None):
        from rpg_game.src.display import DisplaySystem
        if user.mp < self.cost:
            DisplaySystem.show_message(
                f"{user.name} does not have enough MP to use {self.name}.",
                background=background,
                extra_draw=extra_draw
            )
            pygame.time.wait(1200)
            return False
        user.mp -= self.cost
        if is_teammate(user, target):
            DisplaySystem.show_message(
                f"{target.name} has been supported by {self.name}!",
                background=background,
                extra_draw=extra_draw
            )
            pygame.time.wait(1200)
        else:
            DisplaySystem.show_message(
                f"{target.name} takes {self.damage} damage from {self.name}!",
                background=background,
                extra_draw=extra_draw
            )
            pygame.time.wait(1200)
            target.hp -= self.damage
        return True

def is_teammate(user, target):
    return hasattr(user, "team") and hasattr(target, "team") and user.team is target.team

class ElementalSkill(Skill):
    def __init__(self, name, cost, damage, element, desc=""):
        if element not in ELEMENTS:
            raise ValueError(f"Invalid element '{element}'. Must be one of {ELEMENTS}.")
        super().__init__(name, cost, damage, desc)
        self.element = element

    def use(self, user, target, background=None, extra_draw=None):
        from rpg_game.src.display import DisplaySystem
        import pygame
        if user.mp < self.cost:
            DisplaySystem.show_message(
                f"{user.name} does not have enough MP to use {self.name}.",
                background=background,
                extra_draw=extra_draw
            )
            pygame.time.wait(1200)
            return False
        user.mp -= self.cost

        if not hasattr(target, "team") or getattr(target, "team", None) is None:
            total_damage = self.damage
            skill_elem = self.element
            target_elem = getattr(target, "element", None)
            adv_msg = None
            if skill_elem in ELEMENTS and target_elem in ELEMENTS:
                if ELEMENT_ADVANTAGE.get((skill_elem, target_elem), False):
                    total_damage *= 2
                    adv_msg = "Elemental advantage! Damage doubled!"
            target.hp -= total_damage
            # 先顯示多行訊息
            DisplaySystem.clear_screen(background, extra_draw)
            font = pygame.font.Font(None, 32)
            lines = []
            if adv_msg:
                lines.append(adv_msg)
            lines.extend([
                f"{user.name} used {self.name} on {getattr(target, 'name', 'Monster')}!",
                f"Dealt {total_damage} damage.",
                f"MP remaining: {user.mp}/{user.max_mp}"
            ])
            screen = pygame.display.get_surface()
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(400, 220 + i * 40))
                screen.blit(text_surface, text_rect)
            pygame.display.flip()
            # 播放音效
            try:
                pygame.mixer.init()
                pygame.mixer.music.load("open.mp3")
                pygame.mixer.music.play()
                pygame.time.wait(4000)
            except Exception:
                pass
            try:
                pygame.mixer.music.load("hurt.mp3")
                pygame.mixer.music.play()
                pygame.time.wait(1000)
                pygame.mixer.music.stop()
            except Exception:
                pass
            pygame.time.wait(1200)
            return True
        return True

class SupportElementalSkill(Skill):
    def __init__(self, name, cost, element, desc=""):
        if element not in ELEMENTS:
            raise ValueError(f"Invalid element '{element}'. Must be one of {ELEMENTS}.")
        super().__init__(name, cost, 0, desc)
        self.element = element

    def use(self, user, target, background=None, extra_draw=None):
        from rpg_game.src.display import DisplaySystem
        if user.mp < self.cost:
            DisplaySystem.show_message(
                f"{user.name} does not have enough MP to use {self.name}.",
                background=background,
                extra_draw=extra_draw
            )
            pygame.time.wait(1200)
            return False
        user.mp -= self.cost
        if is_teammate(user, target):
            if getattr(user, "element", None) == getattr(target, "element", None):
                if hasattr(target, "apply_status_effect"):
                    target.apply_status_effect("Attack Boost", 1)
                elif hasattr(target, "element_boost"):
                    target.element_boost = True
                DisplaySystem.show_message(
                    f"Synergy! {user.name} and {target.name} have the same element! Effect doubled!\n"
                    f"{target.name}'s attack power is doubled for the next turn!",
                    background=background,
                    extra_draw=extra_draw
                )
                pygame.time.wait(1200)
            old_elem = getattr(target, "element", None)
            target.element_boost = True
            DisplaySystem.show_message(
                f"{target.name}'s element remains {old_elem} and received an element boost!",
                background=background,
                extra_draw=extra_draw
            )
            pygame.time.wait(1200)
            return True
        else:
            DisplaySystem.show_message(
                f"{self.name} can only be used on teammates!",
                background=background,
                extra_draw=extra_draw
            )
            pygame.time.wait(1200)
            return False

