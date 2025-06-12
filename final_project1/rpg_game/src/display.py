import os
import time
import pygame
# 初始化 pygame
if not pygame.get_init():
    pygame.init()
if not pygame.display.get_init():
    pygame.display.init()
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("RPG Game GUI")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((1200, 700))
image_link = pygame.image.load("link.jpg")  # 進入畫面
image_s = pygame.image.load("store.jpg")
image_v = pygame.image.load("vectory.jpg")
image_b = pygame.image.load("battle.jpg")
image_bg = pygame.image.load("background.jpg")  # 主畫面背景
image_backpack = pygame.image.load("backpack.jpg")  # 背包畫面
image_team = pygame.image.load("team.jpg")  # Team Management 畫面
image_upgrade = pygame.image.load("upgrade.jpg")  # 升級系統畫面
background = pygame.transform.scale(image_bg, (1200, 700))  # 主畫面設為 ground.jpg
backpack_bg = pygame.transform.scale(image_backpack, (1200, 700))
team_bg = pygame.transform.scale(image_team, (1200, 700))
# 將 upgrade_bg 調整為右側顯示
upgrade_bg = pygame.transform.scale(image_upgrade, (800, 550))
store = pygame.transform.scale(image_s, (1200, 700))
vectory = pygame.transform.scale(image_v, (1200, 700))
battle = pygame.transform.scale(image_b, (1200, 700))

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
    def show_message(message, color=BLACK, wait_time=0, background=None, extra_draw=None):
        # 僅顯示訊息與背景，不自動撥放音效、不自動跳畫面
        DisplaySystem.clear_screen(background, extra_draw)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(400, 300))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

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
    def show_attack_message(attacker, target, damage, crit=False, element_boost=False, skill_boost=False, background=None, extra_draw=None):
        import pygame  # 修正 UnboundLocalError
        # 若未指定 extra_draw，預設同時顯示 cat_open/boss1 疊加在畫面
        if extra_draw is None:
            def extra_draw():
                try:
                    import sys
                    main_mod = sys.modules.get("__main__")
                    # 先顯示 battle 選單用的 cat1/boss
                    if main_mod and hasattr(main_mod, "cat1") and hasattr(main_mod, "boss") and hasattr(main_mod, "screen"):
                        main_mod.screen.blit(main_mod.cat1, (450, 400))
                        main_mod.screen.blit(main_mod.boss, (850, 300))
                    # 疊加顯示 cat_open/boss1
                    if main_mod and hasattr(main_mod, "cat_open") and hasattr(main_mod, "boss1") and hasattr(main_mod, "screen"):
                        main_mod.screen.blit(main_mod.cat_open, (450, 400))
                        main_mod.screen.blit(main_mod.boss1, (850, 300))
                except Exception:
                    pass
        # 統一顯示與音效邏輯
        # 組合多行訊息
        lines = [
            f"{attacker.name} attacked {target.name if target else 'All'}!",
            f"Dealt {damage} damage."
        ]
        if crit:
            lines.append("[Critical Hit!]")
        if element_boost:
            lines.append("[Element Advantage!]")
        if skill_boost:
            lines.append("[Skill Boost!]")
        # 先顯示畫面
        DisplaySystem.clear_screen(background, extra_draw)
        font = pygame.font.Font(None, 32)
        screen_obj = pygame.display.get_surface()
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(400, 250 + i * 40))
            screen_obj.blit(text_surface, text_rect)
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

    @staticmethod
    def show_skill_use(user, skill, target, damage, crit=False, element_boost=False, background=None, extra_draw=None):
        import pygame  # 修正 UnboundLocalError
        if extra_draw is None:
            def extra_draw():
                try:
                    import sys
                    main_mod = sys.modules.get("__main__")
                    if main_mod and hasattr(main_mod, "cat1") and hasattr(main_mod, "boss") and hasattr(main_mod, "screen"):
                        main_mod.screen.blit(main_mod.cat1, (450, 400))
                        main_mod.screen.blit(main_mod.boss, (850, 300))
                    if main_mod and hasattr(main_mod, "cat_open") and hasattr(main_mod, "boss1") and hasattr(main_mod, "screen"):
                        main_mod.screen.blit(main_mod.cat_open, (450, 400))
                        main_mod.screen.blit(main_mod.boss1, (850, 300))
                except Exception:
                    pass
        # 統一顯示與音效邏輯
        message = f"{user.name} used {skill.name}! {skill.desc}\nDealt {damage} damage to {target.name}!"
        if crit:
            message += " [Critical Hit!]"
        if element_boost:
            message += " [Element Boost!]"
        DisplaySystem.clear_screen(background, extra_draw)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(400, 300))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        # 自動播放 open.mp3
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("open.mp3")
            pygame.mixer.music.play()
            pygame.time.wait(4000)
        except Exception:
            pass
        # 自動播放 hurt.mp3
        try:
            pygame.mixer.music.load("hurt.mp3")
            pygame.mixer.music.play()
            pygame.time.wait(1000)
            pygame.mixer.music.stop()
        except Exception:
            pass

    @staticmethod
    def show_elementSkill_use(user, skill, target, damage, crit=False, element_boost=False, background=None, extra_draw=None):
        import pygame  # 修正 UnboundLocalError
        if extra_draw is None:
            def extra_draw():
                try:
                    import sys
                    main_mod = sys.modules.get("__main__")
                    if main_mod and hasattr(main_mod, "cat1") and hasattr(main_mod, "boss") and hasattr(main_mod, "screen"):
                        main_mod.screen.blit(main_mod.cat1, (450, 400))
                        main_mod.screen.blit(main_mod.boss, (850, 300))
                    if main_mod and hasattr(main_mod, "cat_open") and hasattr(main_mod, "boss1") and hasattr(main_mod, "screen"):
                        main_mod.screen.blit(main_mod.cat_open, (450, 400))
                        main_mod.screen.blit(main_mod.boss1, (850, 300))
                except Exception:
                    pass
        # 統一顯示與音效邏輯
        message = f"{user.name} used {skill.name}! {skill.desc}\nDealt {damage} damage to {target.name}!"
        if crit:
            message += " [Critical Hit!]"
        if element_boost:
            message += " [Element Boost!]"
        DisplaySystem.clear_screen(background, extra_draw)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(400, 300))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        # 自動播放 open.mp3
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("open.mp3")
            pygame.mixer.music.play()
            pygame.time.wait(4000)
        except Exception:
            pass
        # 自動播放 hurt.mp3
        try:
            pygame.mixer.music.load("hurt.mp3")
            pygame.mixer.music.play()
            pygame.time.wait(1000)
            pygame.mixer.music.stop()
        except Exception:
            pass

    @staticmethod
    def show_main_menu():
        # 顯示主畫面背景
        DisplaySystem.clear_screen(background)
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
            text_surface = font.render(option, True, WHITE)
            text_rect = text_surface.get_rect(topleft=(50, 50 + i * 40))
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
        DisplaySystem.clear_screen(team_bg)
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
            pygame.time.wait(2000)
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
        while True:
            DisplaySystem.clear_screen(team_bg)
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
                DisplaySystem.show_message("\n".join([f"{member.name}: {member.position}" for member in team.members]), background=team_bg)
                pygame.time.wait(2000)  # 等待2秒
            elif action == "3. Change Position":
                DisplaySystem.show_message("Enter member name and new position (front/mid/back).", background=team_bg)
                # 顯示隊伍成員
                buttons2 = []
                for idx, member in enumerate(team.members):
                    text_surface = font.render(f"{idx + 1}. {member.name}", True, BLACK)
                    text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                    screen.blit(text_surface, text_rect)
                    buttons2.append((text_rect, member))
                pygame.display.flip()
                selected_member = DisplaySystem.handle_click(buttons2)
                if selected_member:
                    DisplaySystem.show_message("Choose position: front, mid, back.", background=team_bg)
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
                DisplaySystem.show_message("Select a member to fire.", background=team_bg)
                buttons2 = []
                for idx, member in enumerate(team.members):
                    text_surface = font.render(f"{idx + 1}. {member.name}", True, BLACK)
                    text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                    screen.blit(text_surface, text_rect)
                    buttons2.append((text_rect, member))
                pygame.display.flip()
                selected_member = DisplaySystem.handle_click(buttons2)
                if selected_member:
                    team.fire(selected_member.name)
            elif action == "5. Add Member":
                DisplaySystem.show_message("Select a character from the backpack to add.", background=team_bg)
                if not team.backpack.items:
                    DisplaySystem.show_message("The backpack is empty. No characters available to add.", background=team_bg)
                    pygame.time.wait(2000)
                    continue
                buttons2 = []
                for idx, (item_name, data) in enumerate(team.backpack.items.items()):
                    if isinstance(data['item'], Character):
                        text_surface = font.render(f"{idx + 1}. {item_name}", True, BLACK)
                        text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                        screen.blit(text_surface, text_rect)
                        buttons2.append((text_rect, data['item']))
                # 加入退出按鈕
                exit_rect = pygame.Rect(50, 50 + len(buttons2) * 50, 200, 50)
                exit_text = font.render("Exit", True, RED)
                screen.blit(exit_text, exit_rect.topleft)
                buttons2.append((exit_rect, "Exit"))
                pygame.display.flip()
                selected_character = DisplaySystem.handle_click(buttons2)
                if selected_character == "Exit":
                    continue
                if selected_character:
                    team.add_member(selected_character)
            elif action == "6. Return to Main Menu":
                return

    @staticmethod
    def store(team):
        from rpg_game.src.store import gacha_draw_character, gacha_draw_equipment
        # 進入商店時顯示 store.jpg
        DisplaySystem.clear_screen(store)
        pygame.display.flip()
        font = pygame.font.Font(None, 36)
        while True:
            DisplaySystem.clear_screen(store)
            options = [
                "1. Increase STR (50 coins)",
                "2. Increase VIT (50 coins)",
                "3. Increase AGL (50 coins)",
                "4. Increase DEX (50 coins)",
                "5. Increase INT (50 coins)",
                "6. Gacha Draw (200 coins)",
                "7. Exit Store"
            ]
            buttons = []
            for i, option in enumerate(options):
                text_surface = font.render(option, True, BLACK)
                text_rect = text_surface.get_rect(topleft=(50, 50 + i * 50))
                screen.blit(text_surface, text_rect)
                buttons.append((text_rect, option))
            # 顯示目前金幣
            coin_surface = font.render(f"Current Coins: {team.coin}", True, BLUE)
            screen.blit(coin_surface, (800, 50))
            pygame.display.flip()

            action = DisplaySystem.handle_click(buttons)
            if action == "7. Exit Store":
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
                    DisplaySystem.show_message("Not enough coins.", color=RED, background=store)
                    pygame.time.wait(1200)
                    continue
                # 先顯示選擇成員畫面
                DisplaySystem.clear_screen(store)
                buttons2 = []
                for idx, member in enumerate(team.members):
                    text_surface = font.render(f"{idx + 1}. {member.name}", True, BLACK)
                    text_rect = text_surface.get_rect(topleft=(50, 150 + idx * 50))
                    screen.blit(text_surface, text_rect)
                    buttons2.append((text_rect, member))
                coin_surface = font.render(f"Current Coins: {team.coin}", True, BLUE)
                screen.blit(coin_surface, (800, 50))
                # 加入退出按鈕
                exit_rect = pygame.Rect(50, 150 + len(buttons2) * 50, 200, 50)
                exit_text = font.render("Exit", True, RED)
                screen.blit(exit_text, exit_rect.topleft)
                buttons2.append((exit_rect, "Exit"))
                pygame.display.flip()
                selected_member = DisplaySystem.handle_click(buttons2)
                if selected_member == "Exit":
                    continue
                if selected_member:
                    DisplaySystem.clear_screen(store)
                    team.spend_coin(50)
                    setattr(selected_member, attribute, getattr(selected_member, attribute) + 1)
                    # 直接在原畫面顯示提示，不再清空畫面
                    msg = f"{selected_member.name}'s {attribute.upper()} increased by 1!"
                    text_surface = font.render(msg, True, GREEN)
                    screen.blit(text_surface, (50, 500))
                    pygame.display.flip()
                    pygame.time.wait(1200)
            elif action == "6. Gacha Draw (200 coins)":
                if team.coin < 200:
                    DisplaySystem.show_message("Not enough coins for gacha.", color=RED, background=store)
                    pygame.time.wait(1200)
                    continue
                DisplaySystem.clear_screen(store)
                gacha_buttons = [
                    (pygame.Rect(50, 200, 300, 60), "Character Pool"),
                    (pygame.Rect(400, 200, 300, 60), "Equipment Pool")
                ]
                # 加入退出按鈕
                exit_rect = pygame.Rect(50, 300, 200, 50)
                exit_text = font.render("Exit", True, RED)
                screen.blit(exit_text, exit_rect.topleft)
                gacha_buttons.append((exit_rect, "Exit"))
                for rect, label in gacha_buttons[:-1]:
                    text_surface = font.render(label, True, BLACK)
                    screen.blit(text_surface, rect.topleft)
                pygame.display.flip()
                pool_choice = DisplaySystem.handle_click(gacha_buttons)
                if pool_choice == "Exit":
                    continue
                if pool_choice == "Character Pool":
                    gacha_character = gacha_draw_character()
                    team.backpack.add_item(gacha_character, 1)
                    DisplaySystem.show_message(f"Gacha success! {gacha_character.name} added to backpack!", color=GREEN, background=store)
                    pygame.time.wait(1200)
                elif pool_choice == "Equipment Pool":
                    gacha_equipment = gacha_draw_equipment()
                    team.backpack.add_item(gacha_equipment, 1)
                    DisplaySystem.show_message(f"Gacha success! {gacha_equipment.name} added to backpack!", color=GREEN, background=store)
                    pygame.time.wait(1200)             
                team.spend_coin(200)
                pygame.time.wait(1200)
            else:
                DisplaySystem.show_message("Invalid choice. Please enter a valid option.", color=RED, background=store)
                pygame.time.wait(1200)

    @staticmethod
    def backpack_menu(backpack):
        from rpg_game.src.character import Character  # 確保匯入 Character 類型
        from rpg_game.src.backpack import Backpack  # 確保匯入 Backpack 類型
        from rpg_game.src.equipment import Equipment  # 確保匯入 Equipment 類型
        while True:
            DisplaySystem.clear_screen(backpack_bg)
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
                DisplaySystem.clear_screen(backpack_bg)
                font = pygame.font.Font(None, 24)
                y_offset = 50
                if not backpack.items:
                    DisplaySystem.show_message("The backpack is empty.", color=RED, background=backpack_bg)
                    pygame.time.wait(2000)
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
                if not backpack.items:
                    DisplaySystem.show_message("The backpack is empty.", color=RED, background=backpack_bg)
                    pygame.time.wait(2000)
                    continue
                DisplaySystem.show_message("Select an item to use.", background=backpack_bg)
                buttons = []
                for idx, (item_name, data) in enumerate(backpack.items.items()):
                    text_surface = font.render(f"{idx + 1}. {item_name} - Quantity: {data['quantity']}", True, BLACK)
                    text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                    screen.blit(text_surface, text_rect)
                    buttons.append((text_rect, item_name))
                # 加入退出按鈕
                exit_rect = pygame.Rect(50, 50 + len(buttons) * 50, 200, 50)
                exit_text = font.render("Exit", True, RED)
                screen.blit(exit_text, exit_rect.topleft)
                buttons.append((exit_rect, "Exit"))
                pygame.display.flip()
                selected_item = DisplaySystem.handle_click(buttons)
                if selected_item == "Exit":
                    continue
                if selected_item:
                    item_data = backpack.items[selected_item]
                    item = item_data['item']
                    if isinstance(item, Character):
                        DisplaySystem.show_message(f"Entering upgrade system for {selected_item}.", background=backpack_bg)
                        pygame.time.wait(1000)
                        DisplaySystem.upgrade_menu(backpack)
                    elif isinstance(item, Equipment):
                        DisplaySystem.show_message(f"Entering upgrade system for {selected_item}.", background=backpack_bg)
                        pygame.time.wait(1000)
                        DisplaySystem.upgrade_menu(backpack)
                    else:
                        DisplaySystem.show_message(f"Using {selected_item}.", background=backpack_bg)
                        backpack.remove_item(selected_item, 1)

    @staticmethod
    def upgrade_menu(team):
        from rpg_game.src.equipment import Equipment  # 確保匯入 Equipment 類型
        # 進入升級系統時先清空畫面
        screen.fill(WHITE)
        pygame.display.flip()
        while True:
            # upgrade_bg 顯示在右側一點 (x=375, y=90)
            screen.fill(WHITE)
            screen.blit(upgrade_bg, (375, 90))
            pygame.display.flip()
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
                while True:
                    screen.fill(WHITE)
                    screen.blit(upgrade_bg, (375, 90))
                    pygame.display.flip()
                    DisplaySystem.show_message("Select a character to upgrade.")
                    font = pygame.font.Font(None, 36)
                    buttons2 = []
                    for idx, member in enumerate(team.members):
                        text_surface = font.render(f"{idx + 1}. {member.name} (Lv.{member.level})", True, BLACK)
                        text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                        screen.blit(text_surface, text_rect)
                        buttons2.append((text_rect, member))
                    exit_rect = pygame.Rect(50, 50 + len(buttons2) * 50, 200, 50)
                    exit_text = font.render("Exit", True, RED)
                    screen.blit(exit_text, exit_rect.topleft)
                    buttons2.append((exit_rect, "Exit"))
                    pygame.display.flip()
                    selected_member = DisplaySystem.handle_click(buttons2)
                    if selected_member == "Exit":
                        break
                    if selected_member:
                        from rpg_game.src.UpgradeSystem import UpgradeSystem
                        UpgradeSystem.level_up(team, selected_member)
                        break
                continue
            elif action == "2. Enhance Character Attributes":
                while True:
                    screen.fill(WHITE)
                    screen.blit(upgrade_bg, (375, 90))
                    pygame.display.flip()
                    DisplaySystem.show_message("Select a character to enhance attributes.")
                    font = pygame.font.Font(None, 36)
                    buttons2 = []
                    for idx, member in enumerate(team.members):
                        text_surface = font.render(f"{idx + 1}. {member.name}", True, BLACK)
                        text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                        screen.blit(text_surface, text_rect)
                        buttons2.append((text_rect, member))
                    exit_rect = pygame.Rect(50, 50 + len(buttons2) * 50, 200, 50)
                    exit_text = font.render("Exit", True, RED)
                    screen.blit(exit_text, exit_rect.topleft)
                    buttons2.append((exit_rect, "Exit"))
                    pygame.display.flip()
                    selected_member = DisplaySystem.handle_click(buttons2)
                    if selected_member == "Exit":
                        break
                    if selected_member:
                        while True:
                            screen.fill(WHITE)
                            screen.blit(upgrade_bg, (375, 90))
                            pygame.display.flip()
                            DisplaySystem.show_message("Choose an attribute to enhance: STR, VIT, AGL, DEX, INT.")
                            font = pygame.font.Font(None, 36)
                            attr_buttons = [
                                (pygame.Rect(50, 50, 200, 50), "STR"),
                                (pygame.Rect(50, 100, 200, 50), "VIT"),
                                (pygame.Rect(50, 150, 200, 50), "AGL"),
                                (pygame.Rect(50, 200, 200, 50), "DEX"),
                                (pygame.Rect(50, 250, 200, 50), "INT")
                            ]
                            exit_rect = pygame.Rect(50, 300, 200, 50)
                            exit_text = font.render("Exit", True, RED)
                            screen.blit(exit_text, exit_rect.topleft)
                            attr_buttons.append((exit_rect, "Exit"))
                            for rect, label in attr_buttons[:-1]:
                                text_surface = font.render(label, True, BLACK)
                                screen.blit(text_surface, rect.topleft)
                            pygame.display.flip()
                            selected_attr = DisplaySystem.handle_click(attr_buttons)
                            if selected_attr == "Exit":
                                break
                            if selected_attr:
                                from rpg_game.src.UpgradeSystem import UpgradeSystem
                                UpgradeSystem.upgrade_attribute(team, selected_member, selected_attr.lower())
                                break
                        break
                continue
            elif action == "3. Upgrade Equipment":
                while True:
                    screen.fill(WHITE)
                    screen.blit(upgrade_bg, (375, 90))
                    pygame.display.flip()
                    if not hasattr(team, "backpack") or not team.backpack.items:
                        DisplaySystem.show_message("The backpack is empty. No equipment available to upgrade.")
                        screen.blit(upgrade_bg, (375, 90))
                        pygame.time.wait(2000)
                        break

                    DisplaySystem.show_message("Select equipment to upgrade.")
                    font = pygame.font.Font(None, 36)
                    buttons2 = []
                    for idx, (item_name, data) in enumerate(team.backpack.items.items()):
                        if isinstance(data['item'], Equipment):
                            text_surface = font.render(f"{idx + 1}. {item_name} (Lv.{data['item'].level})", True, BLACK)
                            text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                            screen.blit(text_surface, text_rect)
                            buttons2.append((text_rect, data['item']))
                    exit_rect = pygame.Rect(50, 50 + len(buttons2) * 50, 200, 50)
                    exit_text = font.render("Exit", True, RED)
                    screen.blit(exit_text, exit_rect.topleft)
                    buttons2.append((exit_rect, "Exit"))
                    pygame.display.flip()
                    selected_equipment = DisplaySystem.handle_click(buttons2)
                    if selected_equipment == "Exit":
                        break
                    if selected_equipment:
                        from rpg_game.src.UpgradeSystem import UpgradeSystem
                        UpgradeSystem.upgrade_equipment(team, selected_equipment)
                        break
                continue
            elif action == "4. Return to Main Menu":
                return
