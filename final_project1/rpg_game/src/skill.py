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

    def use(self, user, target):
        from rpg_game.src.display import DisplaySystem
        if user.mp < self.cost:
            DisplaySystem.show_message(f"{user.name} does not have enough MP to use {self.name}.")
            return False
        user.mp -= self.cost
        if is_teammate(user, target):
            DisplaySystem.show_message(f"{target.name} has been supported by {self.name}!")
        else:
            DisplaySystem.show_message(f"{target.name} takes {self.damage} damage from {self.name}!")
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

    def use(self, user, target):
        from rpg_game.src.display import DisplaySystem
        if user.mp < self.cost:
            DisplaySystem.show_message(f"{user.name} does not have enough MP to use {self.name}.")
            return False
        user.mp -= self.cost

        # 僅攻擊怪物（target 沒有 team 屬性或 team 為 None）
        if not hasattr(target, "team") or getattr(target, "team", None) is None:
            # 判斷元素相剋加成（以技能的元素 self.element 為攻擊屬性）
            total_damage = self.damage
            skill_elem = self.element
            target_elem = getattr(target, "element", None)
            if skill_elem in ELEMENTS and target_elem in ELEMENTS:
                if ELEMENT_ADVANTAGE.get((skill_elem, target_elem), False):
                    total_damage *= 2
                    DisplaySystem.show_message("Elemental advantage! Damage doubled!")
            target.hp -= total_damage
            DisplaySystem.show_message(
                f"{user.name} used {self.name} on {getattr(target, 'name', 'Monster')}! Dealt {total_damage} damage.\n"
                f"MP remaining: {user.mp}/{user.max_mp}"
            )
        else:
            # 對隊友時不做任何事
            DisplaySystem.show_message(
                f"{self.name} can only be used to attack monsters!"
            )
        return True

class SupportElementalSkill(Skill):
    def __init__(self, name, cost, element, desc=""):
        if element not in ELEMENTS:
            raise ValueError(f"Invalid element '{element}'. Must be one of {ELEMENTS}.")
        super().__init__(name, cost, 0, desc)
        self.element = element

    def use(self, user, target):
        from rpg_game.src.display import DisplaySystem
        if user.mp < self.cost:
            DisplaySystem.show_message(f"{user.name} does not have enough MP to use {self.name}.")
            return False
        user.mp -= self.cost
        if is_teammate(user, target):
            # 只進行加成，不覆蓋元素屬性
            # 如果施加者與被施加者同元素，效果加倍
            if getattr(user, "element", None) == getattr(target, "element", None):
                if hasattr(target, "apply_status_effect"):
                    target.apply_status_effect("Attack Boost", 1)
                elif hasattr(target, "element_boost"):
                    target.element_boost = True
                DisplaySystem.show_message(
                    f"Synergy! {user.name} and {target.name} have the same element! Effect doubled!\n"
                    f"{target.name}'s attack power is doubled for the next turn!"
                )
            old_elem = getattr(target, "element", None)
            target.element_boost = True
            DisplaySystem.show_message(
                f"{target.name}'s element remains {old_elem} and received an element boost!"
            )
            return True
        else:
            DisplaySystem.show_message(f"{self.name} 只能對隊友使用！")
            return False

