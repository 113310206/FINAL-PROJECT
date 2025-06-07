from .equipment import Equipment  # 確保匯入 Equipment 類型
from .character import Character  # 確保匯入 Character 類型

class Backpack:
    def __init__(self):
        self.items = {}

    def add_item(self, item, quantity=1):
        if isinstance(item, dict) and item.get("type") == "attribute_point":
            item_name = f"{item['attribute']} Attribute Point"
            if item_name in self.items:
                self.items[item_name]['quantity'] += quantity
            else:
                self.items[item_name] = {'item': item, 'quantity': quantity}
            print(f"Added {quantity}x {item_name} to the backpack.")
        elif isinstance(item, (Equipment, Character)):  # 支援角色屬性存入
            if item.name in self.items:
                self.items[item.name]['quantity'] += quantity  # 更新物品數量
            else:
                self.items[item.name] = {'item': item, 'quantity': quantity}  # 存入物品實例和數量
            print(f"Added {quantity}x {item.name} to the backpack.")
        elif isinstance(item, str):  # 支援直接存入屬性名稱
            if item in self.items:
                self.items[item]['quantity'] += quantity
            else:
                self.items[item] = {'item': {"type": "attribute_point", "attribute": item}, 'quantity': quantity}
            print(f"Added {quantity}x {item} Attribute Point to the backpack.")
        else:
            print("Invalid item type. Only equipment, characters, or attribute points can be added to the backpack.")

    def remove_item(self, item_name, quantity=1, character=None):
        if item_name in self.items and self.items[item_name]['quantity'] >= quantity:
            self.items[item_name]['quantity'] -= quantity
            if self.items[item_name]['quantity'] == 0:
                del self.items[item_name]
            print(f"Removed {quantity}x {item_name} from the backpack.")
            # 使用屬性點來增加角色屬性強度
            if character and "Attribute Point" in item_name:
                attribute = item_name.split()[0].lower()
                if hasattr(character, attribute):
                    setattr(character, attribute, getattr(character, attribute) + quantity)
                    print(f"{character.name}'s {attribute.upper()} increased by {quantity}.")
        else:
            print(f"Cannot remove {quantity}x {item_name}. Not enough items or item does not exist.")

    def show_items(self):
        print("\n=== Backpack ===")
        if not self.items:
            print("The backpack is empty.")
        else:
            for item_name, data in self.items.items():
                print(f"{item_name}: {data['quantity']}")
        print("================\n")

