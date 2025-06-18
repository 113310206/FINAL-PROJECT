import pygame
image_s = pygame.image.load("store.jpg")
store = pygame.transform.scale(image_s, (1200, 700))

class Backpack:
    def __init__(self, team):
        """Initialize backpack and bind to team"""
        self.items = {}
        self.team = team  # Add team attribute to check if item is equipped

    def add_item(self, item, quantity=1):
        from rpg_game.src.display import DisplaySystem
        from rpg_game.src.equipment import Equipment
        from rpg_game.src.character import Character
        BLUE, RED = (0, 0, 255), (255, 0, 0)
        if isinstance(item, dict) and item.get("type") == "attribute_point":
            item_name = f"{item['attribute']} Point"
            if item_name in self.items:
                self.items[item_name]['quantity'] += quantity
            else:
                self.items[item_name] = {'item': item, 'quantity': quantity}
            DisplaySystem.show_message(f"+{quantity} {item_name}")
            pygame.time.wait(1200)
        elif isinstance(item, (Equipment, Character)):
            if isinstance(item, Equipment):
                if any(member.is_equipped(item.name) for member in self.team.members):
                    DisplaySystem.show_message(f"{item.name} equipped", color=BLUE)
            if item.name in self.items:
                self.items[item.name]['quantity'] += quantity
            else:
                self.items[item.name] = {'item': item, 'quantity': quantity}
            DisplaySystem.show_message(f"+{quantity} {item.name}", background=store)
        elif isinstance(item, str):
            if item in self.items:
                self.items[item]['quantity'] += quantity
            else:
                self.items[item] = {'item': {"type": "attribute_point", "attribute": item}, 'quantity': quantity}
            DisplaySystem.show_message(f"+{quantity} {item} Point")
        else:
            DisplaySystem.show_message("Invalid item", color=RED)

    def remove_item(self, item_name, quantity=1, character=None):
        from rpg_game.src.display import DisplaySystem
        GREEN, RED = (0, 255, 0), (255, 0, 0)
        if item_name in self.items and self.items[item_name]['quantity'] >= quantity:
            self.items[item_name]['quantity'] -= quantity
            if self.items[item_name]['quantity'] == 0:
                del self.items[item_name]
            DisplaySystem.show_message(f"-{quantity} {item_name}")
            if character and "Point" in item_name:
                attribute = item_name.split()[0].lower()
                if hasattr(character, attribute):
                    setattr(character, attribute, getattr(character, attribute) + quantity)
                    DisplaySystem.show_message(f"{character.name} {attribute.upper()} +{quantity}", color=GREEN)
        else:
            DisplaySystem.show_message(f"Not enough {item_name}", color=RED)

    def return_equipment(self, equipment):
        """Return unequipped item to backpack"""
        self.add_item(equipment, 1)

    def show_items(self):
        from rpg_game.src.display import DisplaySystem
        if not self.items:
            DisplaySystem.show_message("Empty")
        else:
            items_info = "\n".join([f"{item_name}: {data['quantity']}" for item_name, data in self.items.items()])
            DisplaySystem.show_message(f"=== Items ===\n{items_info}\n============")

