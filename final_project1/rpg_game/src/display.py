import os
import time
import pygame
# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("RPG Game GUI")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((1200, 700))
image = pygame.image.load("background.jpg")
image_s = pygame.image.load("store.jpg")
image_v = pygame.image.load("vectory.jpg")
background = pygame.transform.scale(image, (1200, 700))
store = pygame.transform.scale(image_s, (1200, 700))
vectory = pygame.transform.scale(image_v, (1200, 700))

class DisplaySystem:
    @staticmethod
    def clear_screen(background=None, extra_draw=None):
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(WHITE)
        if extra_draw:
            extra_draw()
        pygame.display.flip()

    @staticmethod
    def show_message(message, color=BLACK, wait_time=0):
        DisplaySystem.clear_screen()
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(400, 300))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        if wait_time and wait_time > 0:
            pygame.time.wait(wait_time)
        else:
            # 等待玩家點擊或按任意鍵繼續
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False

    @staticmethod
    def show_character(character):
        DisplaySystem.clear_screen()
        font = pygame.font.Font(None, 24)
        info_lines = [
            f"Name: {character.name}",
            f"Job: {getattr(character.job, 'job_name', '無職業')}",
            f"Level: {character.level}",
            f"ATK: {character.attack_power}",
            f"HP: {character.hp}/{character.max_hp}",
            f"MP: {character.mp}/{character.max_mp}",
            f"Armor: {character.armor}/{character.max_armor}",
            f"Element: {character.element or 'None'}",
            f"Position: {character.position}",
            f"Equipment: {', '.join([f'{eq.name} (Lv.{eq.level})' for eq in character.equipment.values() if eq]) or 'None'}"
        ]
        for i, line in enumerate(info_lines):
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (50, 50 + i * 30))
        pygame.display.flip()
        pygame.time.wait(2000)

    @staticmethod
    def show_equipment(equipment):
        DisplaySystem.clear_screen()
        font = pygame.font.Font(None, 24)
        info_lines = [
            f"Name: {equipment.name}",
            f"Type: {equipment.eq_type}",
            f"Level: {equipment.level}",
            f"Stat Bonus: {equipment.stat_bonus}"
        ]
        y_offset = 50
        for line in info_lines:
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 30
        pygame.display.flip()
        pygame.time.wait(2000)

    @staticmethod
    def show_monster(monster):
        DisplaySystem.show_character(monster)

    @staticmethod
    def show_attack_message(attacker, target, damage, crit=False, element_boost=False, skill_boost=False):
        message = f"{attacker.name} attacked {target.name}, dealing {damage} damage!"
        if crit:
            message += " [Critical Hit!]"
        if element_boost:
            message += " [Element Advantage!]"
        if skill_boost:
            message += " [Skill Boost!]"
        DisplaySystem.show_message(message)

    @staticmethod
    def show_monster_attack_message(monster, target, damage, crit=False, element_boost=False):
        if target:
            message = f"{monster.name} attacked {target.name}, dealing {damage} damage!"
        else:
            message = f"{monster.name} performed a group attack, dealing {damage} damage to all members!"
        if crit:
            message += " [Critical Hit!]"
        if element_boost:
            message += " [Element Advantage!]"
        DisplaySystem.show_message(message)

    @staticmethod
    def show_skill_use(user, skill, target, damage, crit=False, element_boost=False):
        message = f"{user.name} used {skill.name}! {skill.desc}\nDealt {damage} damage to {target.name}!"
        if crit:
            message += " [Critical Hit!]"
        if element_boost:
            message += " [Element Boost!]"
        DisplaySystem.show_message(message)

    @staticmethod
    def show_elementSkill_use(user, skill, target, damage, crit=False, element_boost=False):
        message = f"{user.name} used {skill.name} ({skill.element})! {skill.desc}\nDealt {damage} damage to {target.name}!"
        if crit:
            message += " [Critical Hit!]"
        if element_boost:
            message += " [Element Boost!]"
        DisplaySystem.show_message(message)

    @staticmethod
    def show_main_menu():
        DisplaySystem.clear_screen()
        font = pygame.font.Font(None, 36)
        options = [
            "1. Show Team",
            "2. Battle",
            "3. Store",
            "4. Team Management",
            "5. Backpack",
            "6. Upgrade Character/Equipment",
            "7. Exit Game"
        ]
        buttons = []
        for i, option in enumerate(options):
            text_surface = font.render(option, True, BLACK)
            text_rect = text_surface.get_rect(topleft=(50, 50 + i * 50))
            screen.blit(text_surface, text_rect)
            buttons.append((text_rect, option))
        pygame.display.flip()
        return buttons

    @staticmethod
    def handle_click(buttons):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for rect, action in buttons:
                        if rect.collidepoint(mouse_pos):
                            return action

    @staticmethod
    def show_team(team):
        DisplaySystem.clear_screen()
        font = pygame.font.Font(None, 24)
        y_offset = 50
        for member in team.members:
            job_name = getattr(member, "job", None)
            job_name = job_name.job_name if job_name and hasattr(job_name, "job_name") else "無職業"
            info = f"{member.name} | {job_name} | Lv{member.level} | ATK:{member.attack_power} | HP:{member.hp}/{member.max_hp} | MP:{member.mp}/{member.max_mp} | Armor:{member.armor}/{member.max_armor} | Elem:{member.element or 'None'} | Pos:{member.position}"
            text_surface = font.render(info, True, BLACK)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 50

        # 新增退出按鈕
        exit_button = pygame.Rect(50, y_offset + 50, 200, 50)
        text_surface = font.render("Exit", True, BLACK)
        screen.blit(text_surface, exit_button.topleft)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if exit_button.collidepoint(mouse_pos):
                        return  # 返回主選單

    @staticmethod
    def show_backpack(backpack, pause=True):
        # 延遲匯入 Backpack
        from rpg_game.src.backpack import Backpack
        from rpg_game.src.character import Character
        from rpg_game.src.equipment import Equipment
        DisplaySystem.clear_screen()
        font = pygame.font.Font(None, 24)
        y_offset = 50
        if not backpack.items:
            DisplaySystem.show_message("The backpack is empty.", color=RED)
            return
        for item_name, data in backpack.items.items():
            item = data['item']
            quantity = data['quantity']
            item_type = "Character" if isinstance(item, Character) else "Equipment" if isinstance(item, Equipment) else "Other"
            info = f"{item_name} ({item_type}) - Quantity: {quantity}"
            text_surface = font.render(info, True, BLACK)
            y_offset += 50
        pygame.display.flip()
        if pause:
            pygame.time.wait(2000)
    
    @staticmethod
    def show_battle_status(team, monster, background_override=None, extra_draw=None):
        DisplaySystem.clear_screen(background_override, extra_draw)
        font = pygame.font.Font(None, 24)

        # 顯示隊伍狀態
        team_y_offset = 50
        text_surface = font.render("=== Team Status ===", True, BLACK)
        screen.blit(text_surface, (50, team_y_offset))
        team_y_offset += 30
        for member in team.members:
            job_name = getattr(member, "job", None)
            job_name = job_name.job_name if job_name and hasattr(job_name, "job_name") else "無職業"
            eqs = [f"{eq.name} (Lv.{eq.level})" for eq in member.equipment.values() if eq]  # 新增裝備資訊
            info = f"{member.name} | {job_name} | Lv{member.level} | ATK:{member.attack_power} | HP:{member.hp}/{member.max_hp} | MP:{member.mp}/{member.max_mp} | Armor:{member.armor}/{member.max_armor} | Elem:{member.element or 'None'} | Pos:{member.position} | Eq:{', '.join(eqs) if eqs else 'None'}"
            text_surface = font.render(info, True, BLACK)
            screen.blit(text_surface, (50, team_y_offset))
            team_y_offset += 30

        # 顯示怪物狀態
        monster_y_offset = team_y_offset + 50
        text_surface = font.render("=== Monster Status ===", True, RED)
        screen.blit(text_surface, (50, monster_y_offset))
        monster_y_offset += 30
        monster_info = f"{monster.name} | ATK:{monster.attack} | HP:{monster.hp} | Elem:{monster.element or 'None'}"
        text_surface = font.render(monster_info, True, RED)
        screen.blit(text_surface, (50, monster_y_offset))

        pygame.display.flip()
    
    @staticmethod
    def show_store_menu(team):
        DisplaySystem.clear_screen()
        print("=== Store ===")
        print("1. Increase STR (50 coins)")
        print("2. Increase VIT (50 coins)")
        print("3. Increase AGL (50 coins)")
        print("4. Increase DEX (50 coins)")
        print("5. Increase INT (50 coins)")
        print("6. Exit Store")
        print("7. Gacha Draw (200 coins)")
        print(f"Current Coins: {team.coin}")
        print("================")
    
    @staticmethod
    def show_team_menu(team):
        from rpg_game.src.character import Character  # 確保匯入 Character 類型
        DisplaySystem.clear_screen()
        font = pygame.font.Font(None, 36)
        options = [
            "1. View Team",
            "2. View Positions",
            "3. Change Position",
            "4. Fire Member",
            "5. Add Member",
            "6. Return to Main Menu"
        ]
        buttons = []
        for i, option in enumerate(options):
            text_surface = font.render(option, True, BLACK)
            text_rect = text_surface.get_rect(topleft=(50, 50 + i * 50))
            screen.blit(text_surface, text_rect)
            buttons.append((text_rect, option))
        pygame.display.flip()

        action = DisplaySystem.handle_click(buttons)
        if action == "1. View Team":
            DisplaySystem.show_team(team)
        elif action == "2. View Positions":
            DisplaySystem.show_message("\n".join([f"{member.name}: {member.position}" for member in team.members]))
        elif action == "3. Change Position":
            DisplaySystem.show_message("Enter member name and new position (front/mid/back).")
            # 顯示隊伍成員
            buttons = []
            for idx, member in enumerate(team.members):
                text_surface = font.render(f"{idx + 1}. {member.name}", True, BLACK)
                text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                screen.blit(text_surface, text_rect)
                buttons.append((text_rect, member))
            pygame.display.flip()
            selected_member = DisplaySystem.handle_click(buttons)
            if selected_member:
                DisplaySystem.show_message("Choose position: front, mid, back.")
                pos_buttons = [
                    (pygame.Rect(50, 50, 200, 50), "front"),
                    (pygame.Rect(50, 100, 200, 50), "mid"),
                    (pygame.Rect(50, 150, 200, 50), "back")
                ]
                for rect, label in pos_buttons:
                    text_surface = font.render(label, True, BLACK)
                    screen.blit(text_surface, rect.topleft)
                pygame.display.flip()
                new_position = DisplaySystem.handle_click(pos_buttons)
                if new_position:
                    team.change_position(selected_member.name, new_position)
        elif action == "4. Fire Member":
            DisplaySystem.show_message("Select a member to fire.")
            buttons = []
            for idx, member in enumerate(team.members):
                text_surface = font.render(f"{idx + 1}. {member.name}", True, BLACK)
                text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                screen.blit(text_surface, text_rect)
                buttons.append((text_rect, member))
            pygame.display.flip()
            selected_member = DisplaySystem.handle_click(buttons)
            if selected_member:
                team.fire(selected_member.name)
        elif action == "5. Add Member":
            DisplaySystem.show_message("Select a character from the backpack to add.")
            if not team.backpack.items:
                DisplaySystem.show_message("The backpack is empty. No characters available to add.")
                return
            buttons = []
            for idx, (item_name, data) in enumerate(team.backpack.items.items()):
                if isinstance(data['item'], Character):
                    text_surface = font.render(f"{idx + 1}. {item_name}", True, BLACK)
                    text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                    screen.blit(text_surface, text_rect)
                    buttons.append((text_rect, data['item']))
            pygame.display.flip()
            selected_character = DisplaySystem.handle_click(buttons)
            if selected_character:
                team.add_member(selected_character)
        elif action == "6. Return to Main Menu":
            return

    @staticmethod
    def upgrade_menu(team):
        from rpg_game.src.equipment import Equipment  # 確保匯入 Equipment 類型
        DisplaySystem.clear_screen()
        font = pygame.font.Font(None, 36)
        options = [
            "1. Upgrade Character Level",
            "2. Enhance Character Attributes",
            "3. Upgrade Equipment",
            "4. Return to Main Menu"
        ]
        buttons = []
        for i, option in enumerate(options):
            text_surface = font.render(option, True, BLACK)
            text_rect = text_surface.get_rect(topleft=(50, 50 + i * 50))
            screen.blit(text_surface, text_rect)
            buttons.append((text_rect, option))
        pygame.display.flip()

        action = DisplaySystem.handle_click(buttons)
        if action == "1. Upgrade Character Level":
            DisplaySystem.show_message("Select a character to upgrade.")
            buttons = []
            for idx, member in enumerate(team.members):
                text_surface = font.render(f"{idx + 1}. {member.name} (Lv.{member.level})", True, BLACK)
                text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                screen.blit(text_surface, text_rect)
                buttons.append((text_rect, member))
            pygame.display.flip()
            selected_member = DisplaySystem.handle_click(buttons)
            if selected_member:
                # 延遲匯入 UpgradeSystem
                from rpg_game.src.UpgradeSystem import UpgradeSystem
                UpgradeSystem.level_up(team, selected_member)
        elif action == "2. Enhance Character Attributes":
            DisplaySystem.show_message("Select a character to enhance attributes.")
            buttons = []
            for idx, member in enumerate(team.members):
                text_surface = font.render(f"{idx + 1}. {member.name}", True, BLACK)
                text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                screen.blit(text_surface, text_rect)
                buttons.append((text_rect, member))
            pygame.display.flip()
            selected_member = DisplaySystem.handle_click(buttons)
            if selected_member:
                DisplaySystem.show_message("Choose an attribute to enhance: STR, VIT, AGL, DEX, INT.")
                attr_buttons = [
                    (pygame.Rect(50, 50, 200, 50), "STR"),
                    (pygame.Rect(50, 100, 200, 50), "VIT"),
                    (pygame.Rect(50, 150, 200, 50), "AGL"),
                    (pygame.Rect(50, 200, 200, 50), "DEX"),
                    (pygame.Rect(50, 250, 200, 50), "INT")
                ]
                for rect, label in attr_buttons:
                    text_surface = font.render(label, True, BLACK)
                    screen.blit(text_surface, rect.topleft)
                pygame.display.flip()
                selected_attr = DisplaySystem.handle_click(attr_buttons)
                if selected_attr:
                    # 延遲匯入 UpgradeSystem
                    from rpg_game.src.UpgradeSystem import UpgradeSystem
                    UpgradeSystem.upgrade_attribute(team, selected_member, selected_attr.lower())
        elif action == "3. Upgrade Equipment":
            if not team.backpack.items:
                DisplaySystem.show_message("The backpack is empty. No equipment available to upgrade.")
                
                return

            DisplaySystem.show_message("Select equipment to upgrade.")
            buttons = []
            for idx, (item_name, data) in enumerate(team.backpack.items.items()):
                if isinstance(data['item'], Equipment):
                    text_surface = font.render(f"{idx + 1}. {item_name} (Lv.{data['item'].level})", True, BLACK)
                    text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                    screen.blit(text_surface, text_rect)
                    buttons.append((text_rect, data['item']))
            pygame.display.flip()
            selected_equipment = DisplaySystem.handle_click(buttons)
            if selected_equipment:
                # 延遲匯入 UpgradeSystem
                from rpg_game.src.UpgradeSystem import UpgradeSystem
                UpgradeSystem.upgrade_equipment(team, selected_equipment)
        elif action == "4. Return to Main Menu":
            return



    @staticmethod
    def team_menu(team):
        from rpg_game.src.display import DisplaySystem  # 確保顯示功能可用
        from rpg_game.src.character import Character  # 確保匯入 Character 類型
        while True:
            DisplaySystem.show_team_menu()  # 顯示 Team Management 選單
            choice = input("Choose an option: ").strip()
            if choice == "1":  # View Team
                DisplaySystem.show_team(team, pause=True)
            elif choice == "2":  # View Positions
                team.show_positions()
                input("（按 Enter 繼續）")
            elif choice == "3":  # Change Position
                try:
                    name = input("Enter member name: ").strip()
                    pos = input("Enter new position (front/mid/back): ").strip().lower()
                    if pos not in ["front", "mid", "back"]:
                        print("Invalid position. Please enter 'front', 'mid', or 'back'.")
                        continue
                    team.change_position(name, pos)
                    print(f"{name}'s position changed to {pos}.")
                except Exception as e:
                    print(f"Error: {e}")
                input("（按 Enter 繼續）")
            elif choice == "4":  # Fire Member
                try:
                    name = input("Enter member name to fire: ").strip()
                    team.fire(name)
                    print(f"{name} has been removed from the team.")
                except Exception as e:
                    print(f"Error: {e}")
                input("（按 Enter 繼續）")
            elif choice == "5":  # Add Member
                if not team.backpack.items:
                    print("The backpack is empty. No members available to add.")
                    input("（按 Enter 繼續）")
                    continue
                try:
                    DisplaySystem.show_backpack(team.backpack)
                    try:
                        item_idx = int(input("Enter the item number to add as a member: ")) - 1
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                        input("（按 Enter 繼續）")
                        continue
                    if 0 <= item_idx < len(team.backpack.items):
                        item_name = list(team.backpack.items.keys())[item_idx]
                        character = team.backpack.items[item_name]['item']
                        if not isinstance(character, Character):
                            print("Selected item is not a character.")
                            input("（按 Enter 繼續）")
                            continue
                        if len(team.members) < 4:
                            team.add_member(character)
                            team.backpack.remove_item(item_name, 1)
                            print(f"{character.name} has been added to the team.")
                        else:
                            print("The team is full. Cannot add more members.")
                    else:
                        print("Invalid item selection. Please try again.")
                except Exception as e:
                    print(f"Error: {e}")
                input("（按 Enter 繼續）")
            elif choice == "6":  # Return to Main Menu
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                input("（按 Enter 繼續）")

    @staticmethod
    def store(team):
        from rpg_game.src.store import gacha_draw_character, gacha_draw_equipment  # 確保匯入 Gacha 函數
        screen.blit(store, (0, 0))  # 使用背景圖片
        pygame.display.flip()
        while True:

            font = pygame.font.Font(None, 36)
            options = [
                "1. Increase STR (50 coins)",
                "2. Increase VIT (50 coins)",
                "3. Increase AGL (50 coins)",
                "4. Increase DEX (50 coins)",
                "5. Increase INT (50 coins)",
                "6. Exit Store",
                "7. Gacha Draw (200 coins)"
            ]
            buttons = []
            for i, option in enumerate(options):
                text_surface = font.render(option, True, BLACK)
                text_rect = text_surface.get_rect(topleft=(50, 50 + i * 50))
                screen.blit(text_surface, text_rect)
                buttons.append((text_rect, option))
            pygame.display.flip()

            action = DisplaySystem.handle_click(buttons)
            if action == "6. Exit Store":
                break
            elif action.startswith("1. Increase STR") or action.startswith("2. Increase VIT") or action.startswith("3. Increase AGL") or action.startswith("4. Increase DEX") or action.startswith("5. Increase INT"):
                attribute_map = {
                    "1. Increase STR (50 coins)": "str",
                    "2. Increase VIT (50 coins)": "vit",
                    "3. Increase AGL (50 coins)": "agl",
                    "4. Increase DEX (50 coins)": "dex",
                    "5. Increase INT (50 coins)": "intel"
                }
                attribute = attribute_map[action]
                if team.coin < 50:
                    DisplaySystem.show_message("Not enough coins.", color=RED)
                    continue
                DisplaySystem.show_message(f"Select a member to increase {attribute.upper()}.")
                buttons = []
                for idx, member in enumerate(team.members):
                    text_surface = font.render(f"{idx + 1}. {member.name}", True, BLACK)
                    text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                    screen.blit(text_surface, text_rect)
                    buttons.append((text_rect, member))
                pygame.display.flip()
                selected_member = DisplaySystem.handle_click(buttons)
                if selected_member:
                    team.spend_coin(50)
                    setattr(selected_member, attribute, getattr(selected_member, attribute) + 1)
                    DisplaySystem.show_message(f"{selected_member.name}'s {attribute.upper()} increased by 1!", color=GREEN)
            elif action == "7. Gacha Draw (200 coins)":
                if team.coin < 200:
                    DisplaySystem.show_message("Not enough coins for gacha.", color=RED)
                    continue
                DisplaySystem.clear_screen()
                buttons = [
                    (pygame.Rect(50, 50, 200, 50), "Character Pool"),
                    (pygame.Rect(50, 100, 200, 50), "Equipment Pool")
                ]
                for rect, label in buttons:
                    text_surface = font.render(label, True, BLACK)
                    screen.blit(text_surface, rect.topleft)
                pygame.display.flip()
                pool_choice = DisplaySystem.handle_click(buttons)
                if pool_choice == "Character Pool":
                    gacha_character = gacha_draw_character()
                    team.backpack.add_item(gacha_character, 1)
                    DisplaySystem.show_message(f"Gacha success! {gacha_character.name} added to backpack!", color=GREEN)
                elif pool_choice == "Equipment Pool":
                    gacha_equipment = gacha_draw_equipment()
                    team.backpack.add_item(gacha_equipment, 1)
                    DisplaySystem.show_message(f"Gacha success! {gacha_equipment.name} added to backpack!", color=GREEN)
                team.spend_coin(200)
            else:
                print("Invalid choice. Please enter a valid option.\n")
                input("（按 Enter 繼續）")
    @staticmethod
    def backpack_menu(backpack):
        from rpg_game.src.character import Character  # 確保匯入 Character 類型
        from rpg_game.src.backpack import Backpack  # 確保匯入 Backpack 類型
        from rpg_game.src.equipment import Equipment  # 確保匯入 Equipment 類型
        while True:
            DisplaySystem.clear_screen()
            font = pygame.font.Font(None, 36)
            options = [
                "1. View Backpack",
                "2. Use Item",
                "3. Return to Main Menu"
            ]
            buttons = []
            for i, option in enumerate(options):
                text_surface = font.render(option, True, BLACK)
                text_rect = text_surface.get_rect(topleft=(50, 50 + i * 50))
                screen.blit(text_surface, text_rect)
                buttons.append((text_rect, option))
            pygame.display.flip()

            action = DisplaySystem.handle_click(buttons)
            if action == "3. Return to Main Menu":
                break
            elif action == "1. View Backpack":
                DisplaySystem.clear_screen()
                font = pygame.font.Font(None, 24)
                y_offset = 50
                if not backpack.items:  # 修正此處，直接使用 backpack.items
                    DisplaySystem.show_message("The backpack is empty.", color=RED)
                    continue
                for item_name, data in backpack.items.items():
                    item = data['item']
                    quantity = data['quantity']
                    item_type = "Character" if isinstance(item, Character) else "Equipment" if isinstance(item, Equipment) else "Other"
                    info = f"{item_name} ({item_type}) - Quantity: {quantity}"
                    text_surface = font.render(info, True, BLACK)
                    screen.blit(text_surface, (50, y_offset))
                    y_offset += 50
                pygame.display.flip()
                pygame.time.wait(2000)
            elif action == "2. Use Item":
                if not backpack.items:  # 修正此處，直接使用 backpack.items
                    DisplaySystem.show_message("The backpack is empty.", color=RED)
                    continue
                DisplaySystem.show_message("Select an item to use.")
                buttons = []
                for idx, (item_name, data) in enumerate(backpack.items.items()):  # 修正此處，直接使用 backpack.items
                    text_surface = font.render(f"{idx + 1}. {item_name} - Quantity: {data['quantity']}", True, BLACK)
                    text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                    screen.blit(text_surface, text_rect)
                    buttons.append((text_rect, item_name))
                pygame.display.flip()
                selected_item = DisplaySystem.handle_click(buttons)
                if selected_item:
                    item_data = backpack.items[selected_item]  # 修正此處，直接使用 backpack.items
                    item = item_data['item']
                    if isinstance(item, Character):
                        DisplaySystem.show_message(f"Cannot use {selected_item} directly.")
                    elif isinstance(item, Equipment):
                        DisplaySystem.show_message(f"Entering upgrade system for {selected_item}.")
                        DisplaySystem.upgrade_menu(backpack)
                    else:
                        DisplaySystem.show_message(f"Using {selected_item}.")
                        backpack.remove_item(selected_item, 1)
