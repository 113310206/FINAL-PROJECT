import pygame
image_s = pygame.image.load("store.jpg")
store = pygame.transform.scale(image_s, (1200, 700))

class Backpack:
    def __init__(self, team):
        """初始化背包並綁定隊伍"""
        self.items = {}
        self.team = team  # 新增 team 屬性，用於檢查角色是否已裝備物品

    def add_item(self, item, quantity=1):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        from rpg_game.src.equipment import Equipment  # 匯入 Equipment 類別
        from rpg_game.src.character import Character  # 匯入 Character 類型
        BLUE, RED = (0, 0, 255), (255, 0, 0)  # 動態定義顏色
        if isinstance(item, dict) and item.get("type") == "attribute_point":
            item_name = f"{item['attribute']} Attribute Point"
            if item_name in self.items:
                self.items[item_name]['quantity'] += quantity
            else:
                self.items[item_name] = {'item': item, 'quantity': quantity}
            DisplaySystem.show_message(f"Added {quantity}x {item_name} to the backpack.")
            pygame.time.wait(1200)  # 等待1秒
        elif isinstance(item, (Equipment, Character)):  # 支援角色屬性存入
            if isinstance(item, Equipment):
                # 檢查是否已裝備該物品
                if any(member.is_equipped(item.name) for member in self.team.members):
                    DisplaySystem.show_message(f"{item.name} is equipped and will remain in the backpack.", color=BLUE)
            if item.name in self.items:
                self.items[item.name]['quantity'] += quantity  # 更新物品數量
            else:
                self.items[item.name] = {'item': item, 'quantity': quantity}  # 存入物品實例和數量
            DisplaySystem.show_message(f"Added {quantity}x {item.name} to the backpack.", background=store)
        elif isinstance(item, str):  # 支援直接存入屬性名稱
            if item in self.items:
                self.items[item]['quantity'] += quantity
            else:
                self.items[item] = {'item': {"type": "attribute_point", "attribute": item}, 'quantity': quantity}
            DisplaySystem.show_message(f"Added {quantity}x {item} Attribute Point to the backpack.")
        else:
            DisplaySystem.show_message("Invalid item type. Only equipment, characters, or attribute points can be added to the backpack.", color=RED)

    def remove_item(self, item_name, quantity=1, character=None):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        GREEN, RED = (0, 255, 0), (255, 0, 0)  # 動態定義顏色
        if item_name in self.items and self.items[item_name]['quantity'] >= quantity:
            self.items[item_name]['quantity'] -= quantity
            if self.items[item_name]['quantity'] == 0:
                del self.items[item_name]
            DisplaySystem.show_message(f"Removed {quantity}x {item_name} from the backpack.")
            # 使用屬性點來增加角色屬性強度
            if character and "Attribute Point" in item_name:
                attribute = item_name.split()[0].lower()
                if hasattr(character, attribute):
                    setattr(character, attribute, getattr(character, attribute) + quantity)
                    DisplaySystem.show_message(f"{character.name}'s {attribute.upper()} increased by {quantity}.", color=GREEN)
        else:
            DisplaySystem.show_message(f"Cannot remove {quantity}x {item_name}. Not enough items or item does not exist.", color=RED)

    def return_equipment(self, equipment):
        """將卸下的裝備返回到背包"""
        self.add_item(equipment, 1)

    def show_items(self):
        from rpg_game.src.display import DisplaySystem  # 動態匯入
        if not self.items:
            DisplaySystem.show_message("The backpack is empty.")
        else:
            items_info = "\n".join([f"{item_name}: {data['quantity']}" for item_name, data in self.items.items()])
            DisplaySystem.show_message(f"=== Backpack ===\n{items_info}\n================")

