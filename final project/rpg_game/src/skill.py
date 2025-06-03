class Skill:
    def __init__(self, name, cost, damage, desc=""):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.desc = desc

    def use(self, user, target):
        from .display import DisplaySystem  # 避免循環引用
        if user.mp >= self.cost:
            user.mp -= self.cost
            if is_teammate(user, target):
                DisplaySystem.show_skill_use(user, self, target, 0)
                print(f"{target.name} has been supported by {self.name}!")
            else:
                DisplaySystem.show_skill_use(user, self, target, self.damage)
                target.hp -= self.damage
            return True
        else:
            DisplaySystem.show_mp_not_enough(user, self)
            return False
    
def is_teammate(user, target):
    # 假設隊友的判斷邏輯是基於 team 屬性
    return hasattr(user, "team") and hasattr(target, "team") and user.team == target.team

class ElementalSkill(Skill):
    def __init__(self, name, cost, damage, element, desc=""):
        super().__init__(name, cost, damage, desc)
        self.element = element

    def use(self, user, target):
        from .display import DisplaySystem  # 避免循環引用
        if user.mp < self.cost:
            DisplaySystem.show_mp_not_enough(user, self)
            return False

        user.mp -= self.cost
        if is_teammate(user, target):
            DisplaySystem.show_elementSkill_use(user, self, target, 0)  # 顯示技能使用但不造成傷害
            print(f"{target.name} has been blessed by {self.name}!")
            target.element = self.element  # 僅改變屬性
        else:
            total_damage = self.damage
            if user.element and target.element:
                if (user.element, target.element) in [("WATER", "FIRE"), ("FIRE", "WOOD"), ("WOOD", "WATER")]:
                    total_damage *= 2
                    print("It's super effective!")
            DisplaySystem.show_elementSkill_use(user, self, target, total_damage)
            if is_teammate(user, target):
                return False
            else:
                target.hp -= total_damage  # 對敵人造成傷害
            target.element = self.element
        return True

class SupportElementalSkill(Skill):
    def __init__(self, name, cost, element, desc=""):
        super().__init__(name, cost, 0, desc)  # damage 固定為 0
        self.element = element

    def use(self, user, target):
        from .display import DisplaySystem  # 避免循環引用
        if user.mp < self.cost:
            DisplaySystem.show_mp_not_enough(user, self)
            return False

        user.mp -= self.cost
        if is_teammate(user, target):
            DisplaySystem.show_elementSkill_use(user, self, target, 0)  # 顯示技能使用但不造成傷害
            print(f"{target.name} has been blessed by {self.name}!")
            target.element = self.element  # 僅改變屬性
            return True
        else:
            print(f"{self.name} 只能對隊友使用！")
            return False

