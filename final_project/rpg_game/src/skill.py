FIRE = 1
WATER = 2
WOOD = 3

class Skill:
    def __init__(self, name, cost, damage, desc=""):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.desc = desc

    def use(self, user, target):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        if user.mp >= self.cost:
            user.mp -= self.cost
            if is_teammate(user, target):
                DisplaySystem.show_message(f"{target.name} has been supported by {self.name}!")
            else:
                DisplaySystem.show_message(f"{target.name} takes {self.damage} damage from {self.name}!")
                target.hp -= self.damage
            return True
        else:
            DisplaySystem.show_message(f"{user.name} does not have enough MP to use {self.name}.")
            return False
    
def is_teammate(user, target):
    """判斷 user 和 target 是否為隊友"""
    return hasattr(user, "team") and hasattr(target, "team") and user.team is target.team

class ElementalSkill(Skill):
    def __init__(self, name, cost, damage, element, desc=""):
        if element not in ["FIRE", "WATER", "WOOD"]:  # 確保元素值正確匹配
            raise ValueError(f"Invalid element '{element}'. Must be FIRE, WATER, or WOOD.")
        super().__init__(name, cost, damage, desc)
        self.element = element

    def use(self, user, target):
        """使用元素技能"""
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        if user.mp < self.cost:
            DisplaySystem.show_message(f"{user.name} does not have enough MP to use {self.name}.")
            return False

        user.mp -= self.cost
        if is_teammate(user, target):
            DisplaySystem.show_message(f"{target.name} has been blessed by {self.name}!")
            target.element = self.element
        else:
            total_damage = self.damage
            if user.element and getattr(target, "element", "None"):
                if (user.element, target.element) in [("WATER", "FIRE"), ("FIRE", "WOOD"), ("WOOD", "WATER")]:
                    total_damage *= 2
                    DisplaySystem.show_message("It's super effective!")
            DisplaySystem.show_message(f"{target.name} takes {total_damage} damage from {self.name}!")
            target.hp -= total_damage
        return True

class SupportElementalSkill(Skill):
    def __init__(self, name, cost, element, desc=""):
        if element not in ["FIRE", "WATER", "WOOD"]:  # 確保元素值正確匹配
            raise ValueError(f"Invalid element '{element}'. Must be FIRE, WATER, or WOOD.")
        super().__init__(name, cost, 0, desc)  # damage 固定為 0
        self.element = element

    def use(self, user, target):
        """使用支援元素技能"""
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        if user.mp < self.cost:
            DisplaySystem.show_message(f"{user.name} does not have enough MP to use {self.name}.")
            return False

        user.mp -= self.cost
        if is_teammate(user, target):
            DisplaySystem.show_message(f"{target.name} has been blessed by {self.name}!")
            target.element = self.element
            target.element_boost = True  # 設置元素加成
            return True
        else:
            DisplaySystem.show_message(f"{self.name} 只能對隊友使用！")
            return False

