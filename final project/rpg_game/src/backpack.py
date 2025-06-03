from .equipment import Equipment  # 確保匯入 Equipment 類型
from .character import Character  # 確保匯入 Character 類型

class Backpack:
    def __init__(self):
        self.items = {}

    def add_item(self, item, quantity=1):
        if not isinstance(item, (Equipment, Character)):  # 確保物品是 Equipment 或 Character 類型
            print("Invalid item type. Only equipment or characters can be added to the backpack.")
            return
        if item.name in self.items:
            self.items[item.name]['quantity'] += quantity  # 更新物品數量
        else:
            self.items[item.name] = {'item': item, 'quantity': quantity}  # 存入物品實例和數量
        print(f"Added {quantity}x {item.name} to the backpack.")

    def remove_item(self, item_name, quantity=1):
        if item_name in self.items and self.items[item_name]['quantity'] >= quantity:
            self.items[item_name]['quantity'] -= quantity
            if self.items[item_name]['quantity'] == 0:
                del self.items[item_name]
            print(f"Removed {quantity}x {item_name} from the backpack.")
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
