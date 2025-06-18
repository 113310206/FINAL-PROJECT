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
BLUE = (0, 185, 220)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
PINK = (255, 192, 203)

screen = pygame.display.set_mode((1200, 700))
image_link = pygame.image.load("link.jpg")  # 進入畫面
image_s = pygame.image.load("store.jpg")
image_v = pygame.image.load("vectory.jpg")
image_b = pygame.image.load("battle.jpg")
image_bg = pygame.image.load("background1.jpg")  # 主畫面背景
image_backpack = pygame.image.load("backpack.jpg")  # 背包畫面
image_team = pygame.image.load("team.jpg")  # Team Management 畫面
image_upgrade = pygame.image.load("upgrade.jpg")  # 升級系統畫面
background = pygame.transform.scale(image_bg, (1200, 700))  # 主畫面設為 ground.jpg
backpack_bg = pygame.transform.scale(image_backpack, (1200, 700))
team_bg = pygame.transform.scale(image_team, (1200, 700))
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
    def show_message(message, color=BLACK, wait_time=0, background=None, extra_draw=None, position=(350, 250)):
        # 僅顯示訊息與背景，不自動撥放音效、不自動跳畫面
        DisplaySystem.clear_screen(background, extra_draw)
        
        # 創建訊息文字
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=position)
        
        # 創建透明白底
        padding = 20  # 文字周圍的內邊距
        bg_width = text_rect.width + padding * 2
        bg_height = text_rect.height + padding * 2
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 120))  # 白色，透明度120
        
        # 計算背景位置（使文字居中）
        bg_rect = bg_surface.get_rect(center=position)
        
        # 先畫背景，再畫文字
        screen.blit(bg_surface, bg_rect)
        screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        if wait_time > 0:
            pygame.time.wait(wait_time)

    @staticmethod
    def create_panel(width, height, x, y, alpha=120):
        """創建統一的半透明面板"""
        panel_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        panel_surface.fill((255, 255, 255, alpha))
        return panel_surface, (x, y)

    @staticmethod
    def show_character(character):
        DisplaySystem.clear_screen()
        font = pygame.font.Font(None, 24)
        info_lines = [
            f"Name: {character.name}",
            f"Job: {getattr(character.job, 'job_name', 'No Job')}",
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
            text_surface = font.render(line, True, WHITE)
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
        DisplaySystem.clear_screen(background, extra_draw)
        font = pygame.font.Font(None, 32)

        # 計算訊息行數
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

        # 計算 panel 大小
        panel_width = 600
        panel_height = 40 + len(lines) * 30  # 上邊距+訊息行+下邊距
        panel_x, panel_y = 300, 200  # 置中顯示
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((255, 255, 255, 180))  # 白底，透明度180
        screen.blit(panel_surface, (panel_x, panel_y))

        # 顯示訊息
        y_offset = panel_y + 20
        for line in lines:
            text_surface = font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(panel_x + panel_width//2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 40

        pygame.display.flip()
        # 播放音效部分保持不變
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
        DisplaySystem.clear_screen(background, extra_draw)
        font = pygame.font.Font(None, 32)

        # 組合訊息
        lines = [
            f"{user.name} used {skill.name}!",
            skill.desc,
            f"Dealt {damage} damage to {target.name}!"
        ]
        if crit:
            lines.append("[Critical Hit!]")
        if element_boost:
            lines.append("[Element Boost!]")

        # 計算 panel 大小
        panel_width = 600
        panel_height = 40 + len(lines) * 30 # 上邊距+訊息行+下邊距
        panel_x, panel_y = 300, 200  # 置中顯示
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((255, 255, 255, 180))  # 白底，透明度180
        screen.blit(panel_surface, (panel_x, panel_y))

        # 顯示訊息
        y_offset = panel_y + 20
        for line in lines:
            text_surface = font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(panel_x + panel_width//2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 40

        pygame.display.flip()
        # 播放音效部分保持不變
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
    def show_elementSkill_use(user, skill, target, damage, crit=False, element_boost=False, background=None, extra_draw=None):
        DisplaySystem.clear_screen(background, extra_draw)
        font = pygame.font.Font(None, 32)

        # 組合訊息
        lines = [
            f"{user.name} used {skill.name}!",
            skill.desc,
            f"Dealt {damage} damage to {target.name}!"
        ]
        if crit:
            lines.append("[Critical Hit!]")
        if element_boost:
            lines.append("[Element Boost!]")

        # 計算 panel 大小
        panel_width = 600
        panel_height = 40 + len(lines) * 30# 上邊距+訊息行+下邊距
        panel_x, panel_y = 300, 200  # 置中顯示
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((255, 255, 255, 180))  # 白底，透明度180
        screen.blit(panel_surface, (panel_x, panel_y))

        # 顯示訊息
        y_offset = panel_y + 20
        for line in lines:
            text_surface = font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(panel_x + panel_width//2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 40

        pygame.display.flip()
        # 播放音效部分保持不變
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
            text_rect = text_surface.get_rect(topleft=(700, 150 + i * 60))  # 0 是最左邊
            screen.blit(text_surface, text_rect)
            buttons.append((text_rect, option))
        pygame.display.flip()
        return buttons

    @staticmethod
    def handle_click(buttons):
        """處理滑鼠點擊事件"""
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
                # 添加 ESC 鍵退出功能
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "Exit"
        return None

    @staticmethod
    def show_team(team):
        DisplaySystem.clear_screen(team_bg)
        font = pygame.font.Font(None, 40)
        y_offset = 150  # 原本是50，往下移100像素

        # 計算面板高度：每個成員需要100像素高度(50像素間距)，加上上下邊距
        panel_width = 1145
        panel_height = len(team.members) * 100 + 100  # 100是上下邊距
        panel_x, panel_y = 30, 130  
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((255, 255, 255, 180))  # 180為透明度(0~255)
        screen.blit(panel_surface, (panel_x, panel_y))
        
        for member in team.members:
            job_name = getattr(member, "job", None)
            job_name = job_name.job_name if job_name and hasattr(job_name, "job_name") else "No Job "
            info = (
                f"{member.name} | {job_name} | Lv{member.level}\n"
                f"ATK:{member.attack_power} | HP:{member.hp}/{member.max_hp} | MP:{member.mp}/{member.max_mp} | Armor:{member.armor}/{member.max_armor} | Elem:{member.element or 'None'} | Pos:{member.position}"
            )
            # 多行顯示
            for line in info.split('\n'):
                text_surface = font.render(line, True, BLUE)
                screen.blit(text_surface, (50, y_offset))
                y_offset += 50

        # 新增退出按鈕
        exit_button = pygame.Rect(50, y_offset + 50, 270, 50)
        text_surface = font.render("Exit", True, RED)
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
        # Import required classes at the beginning
        from rpg_game.src.character import Character
        from rpg_game.src.equipment import Equipment
        
        screen = pygame.display.set_mode((1200, 700))
        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 48)
        
        while True:
            screen.blit(backpack_bg, (0, 0))
            
            # Panel parameters
            panel_width = 500
            options = [
                "1. View Items",
                "2. Use Item",
                "3. Return"
            ]
            button_height = 50
            button_spacing = 20
            panel_height = 80 + len(options) * (button_height + button_spacing) + 40
            panel_x = 20
            panel_y = 20
            
            # Create semi-transparent panel
            panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            panel.fill((255, 255, 255, 200))
            
            # Display title
            title = title_font.render("Backpack", True, BLACK)
            title_rect = title.get_rect(left=20, top=20)
            panel.blit(title, title_rect)
            
            # Calculate button positions
            button_width = 460
            start_y = 80
            
            buttons = []
            for i, option in enumerate(options):
                button_rect = pygame.Rect(20, start_y + i * (button_height + button_spacing), button_width, button_height)
                pygame.draw.rect(panel, (200, 200, 200, 150), button_rect, border_radius=10)
                
                text_surface = font.render(option, True, BLACK)
                text_rect = text_surface.get_rect(center=button_rect.center)
                panel.blit(text_surface, text_rect)
                
                buttons.append((button_rect, option))
            
            screen.blit(panel, (panel_x, panel_y))
            pygame.display.flip()
            
            action = DisplaySystem.handle_click(buttons)
            if action == "3. Return":
                break
            elif action == "1. View Items":
                DisplaySystem.clear_screen(backpack_bg)
                if not backpack.items:
                    DisplaySystem.show_message("Backpack is Empty", color=RED, background=backpack_bg)
                    pygame.time.wait(2000)
                    continue
                
                # Create items panel
                items_panel = pygame.Surface((500, 400), pygame.SRCALPHA)
                items_panel.fill((255, 255, 255, 200))
                
                y_offset = 20
                for item_name, data in backpack.items.items():
                    item = data['item']
                    quantity = data['quantity']
                    item_type = "Character" if isinstance(item, Character) else "Equipment" if isinstance(item, Equipment) else "Other"
                    info = f"{item_name} ({item_type}) - Qty: {quantity}"
                    text_surface = font.render(info, True, BLACK)
                    items_panel.blit(text_surface, (20, y_offset))
                    y_offset += 40
                
                screen.blit(items_panel, (20, 20))
                pygame.display.flip()
                pygame.time.wait(2000)
                
            elif action == "2. Use Item":
                if not backpack.items:
                    DisplaySystem.show_message("Backpack is Empty", color=RED, background=backpack_bg)
                    pygame.time.wait(2000)
                    continue
                
                # Create use item panel
                DisplaySystem.clear_screen(backpack_bg)
                use_panel = pygame.Surface((500, 400), pygame.SRCALPHA)
                use_panel.fill((255, 255, 255, 200))
                
                title = font.render("Select Item to Use", True, BLACK)
                use_panel.blit(title, (20, 20))
                
                buttons = []
                y_offset = 70
                for idx, (item_name, data) in enumerate(backpack.items.items()):
                    button_rect = pygame.Rect(20, y_offset, 460, 40)
                    pygame.draw.rect(use_panel, (200, 200, 200, 150), button_rect, border_radius=5)
                    text_surface = font.render(f"{idx + 1}. {item_name} - Qty: {data['quantity']}", True, BLACK)
                    use_panel.blit(text_surface, (30, y_offset + 10))
                    buttons.append((button_rect, item_name))
                    y_offset += 50
                
                exit_rect = pygame.Rect(20, y_offset, 460, 40)
                pygame.draw.rect(use_panel, (255, 200, 200, 150), exit_rect, border_radius=5)
                exit_text = font.render("Exit", True, RED)
                use_panel.blit(exit_text, (30, y_offset + 10))
                buttons.append((exit_rect, "Exit"))
                
                screen.blit(use_panel, (20, 20))
                pygame.display.flip()
                
                selected_item = DisplaySystem.handle_click(buttons)
                if selected_item == "Exit":
                    continue
                if selected_item:
                    item_data = backpack.items[selected_item]
                    item = item_data['item']
                    if isinstance(item, (Character, Equipment)):
                        DisplaySystem.show_message(f"Entering upgrade for {selected_item}", background=backpack_bg)
                        pygame.time.wait(1000)
                        DisplaySystem.upgrade_menu(backpack.team)
                    else:
                        DisplaySystem.show_message(f"Using {selected_item}", background=backpack_bg)
                        backpack.remove_item(selected_item, 1)

    @staticmethod
    def show_battle_status(team, monster, background_override=None, extra_draw=None):
        DisplaySystem.clear_screen(background_override, extra_draw)
        font = pygame.font.Font(None, 24)

        # --- 隊伍狀態白底 ---
        team_panel_width = 900
        team_panel_height = 40 + len(team.members) * 27 + 30  # 上邊距+每人一行+下邊距
        team_panel_x, team_panel_y = 30, 30
        team_panel_surface = pygame.Surface((team_panel_width, team_panel_height), pygame.SRCALPHA)
        team_panel_surface.fill((255, 255, 255, 180))  # 白底，透明度180
        screen.blit(team_panel_surface, (team_panel_x, team_panel_y))

        y_offset = team_panel_y + 15
        text_surface = font.render("=== Team Status ===", True, BLACK)
        screen.blit(text_surface, (team_panel_x + 20, y_offset))
        y_offset += 30
        for member in team.members:
            job_name = getattr(member, "job", None)
            job_name = job_name.job_name if job_name and hasattr(job_name, "job_name") else "No Job"
            eqs = [f"{eq.name} (Lv.{eq.level})" for eq in member.equipment.values() if eq]
            info = f"{member.name} | {job_name} | Lv{member.level} | ATK:{member.attack_power} | HP:{member.hp}/{member.max_hp} | MP:{member.mp}/{member.max_mp} | Armor:{member.armor}/{member.max_armor} | Elem:{member.element or 'None'} | Pos:{member.position} | Eq:{', '.join(eqs) if eqs else 'None'}"
            text_surface = font.render(info, True, BLACK)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 30

        # 顯示怪物狀態
        monster_panel_width = 400
        monster_panel_height = 40 + 30   # 上邊距+標題+資訊+下邊距
        monster_panel_x, monster_panel_y = 40, y_offset + 50  # 在隊伍狀態下方
        monster_panel_surface = pygame.Surface((monster_panel_width, monster_panel_height), pygame.SRCALPHA)
        monster_panel_surface.fill((255, 192, 203, 180))  # 粉紅色底，透明度180
        screen.blit(monster_panel_surface, (monster_panel_x, monster_panel_y))

        # 怪物標題
        monster_title_y = monster_panel_y + 10
        text_surface = font.render("=== Monster Status ===", True, RED)
        screen.blit(text_surface, (monster_panel_x + 20, monster_title_y))

        # 怪物資訊
        monster_info_y = monster_title_y + 30
        monster_info = f"{monster.name} | ATK:{monster.attack} | HP:{monster.hp} | Elem:{monster.element or 'None'}"
        text_surface = font.render(monster_info, True, RED)
        screen.blit(text_surface, (monster_panel_x + 10, monster_info_y))

        pygame.display.flip()
    

    @staticmethod
    def show_team_menu(team):
        """顯示隊伍選單"""
        screen = pygame.display.set_mode((1200, 700))
        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 48)
        
        while True:  # 主循環
            # 保持背景顯示
            screen.blit(team_bg, (0, 0))
            
            # 計算面板大小和位置 (移到左上角)
            panel_width = 400
            # 動態計算面板高度：標題(80) + 選項數量 * (按鈕高度 + 間距) + 底部間距(40)
            button_height = 50
            button_spacing = 20
            options = [
                "1. View Team",
                "2. View Positions",
                "3. Change Position",
                "4. Fire Member",
                "5. Add Member",
                "6. Return to Main Menu"
            ]
            panel_height = 80 + len(options) * (button_height + button_spacing) + 40
            panel_x = 20  # 左邊距
            panel_y = 20  # 上邊距
            
            # 創建半透明背景面板
            panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            panel.fill((255, 255, 255, 200))
            
            # 顯示標題
            title = title_font.render("Team Management", True, BLACK)
            title_rect = title.get_rect(left=20, top=20)
            panel.blit(title, title_rect)
            
            # 計算選項按鈕大小和位置
            button_width = 360
            start_y = 80  # 標題下方開始
            
            buttons = []
            for i, option in enumerate(options):
                # 創建按鈕背景
                button_rect = pygame.Rect(20, start_y + i * (button_height + button_spacing), button_width, button_height)
                pygame.draw.rect(panel, (200, 200, 200, 150), button_rect, border_radius=10)
                
                # 添加按鈕文字
                text_surface = font.render(option, True, BLACK)
                text_rect = text_surface.get_rect(center=button_rect.center)
                panel.blit(text_surface, text_rect)
                
                buttons.append((button_rect, option))
            
            # 顯示面板
            screen.blit(panel, (panel_x, panel_y))
            pygame.display.flip()
            
            # 處理主選單選擇
            action = DisplaySystem.handle_click(buttons)
            
            if action == "1. View Team":
                DisplaySystem.show_team(team)
            elif action == "2. View Positions":
                # 動態計算訊息面板大小
                DisplaySystem.clear_screen(team_bg)
                positions = [f"{member.name}: {member.position}" for member in team.members]
                msg_height = len(positions) * 30 + 60  # 每行30像素，加上上下邊距
                msg_panel = pygame.Surface((400, msg_height), pygame.SRCALPHA)
                msg_panel.fill((255, 255, 255, 200))
                
                # 顯示位置資訊
                y_offset = 20
                for pos in positions:
                    text = font.render(pos, True, BLACK)
                    msg_panel.blit(text, (20, y_offset))
                    y_offset += 30
                
                screen.blit(msg_panel, (20, 20))
                pygame.display.flip()
                pygame.time.wait(2000)
                
            elif action == "3. Change Position":
                # 動態計算選擇面板大小
                DisplaySystem.clear_screen(team_bg)
                select_height = 70 + len(team.members) * 50 + 50  # 標題(70) + 成員列表 + 退出按鈕(50)
                select_panel = pygame.Surface((400, select_height), pygame.SRCALPHA)
                select_panel.fill((255, 255, 255, 200))
                
                # 顯示標題
                title = font.render("Select Member to Change Position", True, BLACK)
                select_panel.blit(title, (20, 20))
                
                # 顯示成員列表
                buttons2 = []
                for idx, member in enumerate(team.members):
                    button_rect = pygame.Rect(20, 70 + idx * 50, 360, 40)
                    pygame.draw.rect(select_panel, (200, 200, 200, 150), button_rect, border_radius=5)
                    text_surface = font.render(f"{idx + 1}. {member.name}", True, BLACK)
                    select_panel.blit(text_surface, (30, 80 + idx * 50))
                    buttons2.append((button_rect, member))
                
                # 添加退出按鈕
                exit_rect = pygame.Rect(20, 70 + len(team.members) * 50, 360, 40)
                pygame.draw.rect(select_panel, (255, 200, 200, 150), exit_rect, border_radius=5)
                exit_text = font.render("Exit", True, RED)
                select_panel.blit(exit_text, (30, 80 + len(team.members) * 50))
                buttons2.append((exit_rect, "Exit"))
                
                # 顯示面板
                screen.blit(select_panel, (20, 20))
                pygame.display.flip()
                
                selected_member = DisplaySystem.handle_click(buttons2)
                if selected_member == "Exit":
                    continue
                if selected_member:
                    # 創建位置選擇面板
                    pos_panel = pygame.Surface((300, 250), pygame.SRCALPHA)
                    pos_panel.fill((255, 255, 255, 200))
                    
                    # 顯示標題
                    title = font.render("Choose Position", True, BLACK)
                    pos_panel.blit(title, (20, 20))
                    
                    # 顯示位置選項
                    pos_buttons = []
                    positions = ["front", "mid", "back"]
                    for idx, pos in enumerate(positions):
                        button_rect = pygame.Rect(20, 70 + idx * 50, 260, 40)
                        pygame.draw.rect(pos_panel, (200, 200, 200, 150), button_rect, border_radius=5)
                        text_surface = font.render(pos, True, BLACK)
                        pos_panel.blit(text_surface, (30, 80 + idx * 50))
                        pos_buttons.append((button_rect, pos))
                    
                    # 添加退出按鈕
                    exit_rect = pygame.Rect(20, 220, 260, 40)
                    pygame.draw.rect(pos_panel, (255, 200, 200, 150), exit_rect, border_radius=5)
                    exit_text = font.render("Exit", True, RED)
                    pos_panel.blit(exit_text, (30, 230))
                    pos_buttons.append((exit_rect, "Exit"))
                    
                    # 顯示面板
                    screen.blit(pos_panel, (20, 20))
                    pygame.display.flip()
                    
                    new_position = DisplaySystem.handle_click(pos_buttons)
                    if new_position == "Exit":
                        continue
                    if new_position:
                        team.change_position(selected_member.name, new_position)
            elif action == "4. Fire Member":
                # 動態計算選擇面板大小
                DisplaySystem.clear_screen(team_bg)
                select_height = 70 + len(team.members) * 50 + 50
                select_panel = pygame.Surface((400, select_height), pygame.SRCALPHA)
                select_panel.fill((255, 255, 255, 200))
                
                # 顯示標題
                title = font.render("Select Member to Fire", True, BLACK)
                select_panel.blit(title, (20, 20))
                
                # 顯示成員列表
                buttons2 = []
                for idx, member in enumerate(team.members):
                    button_rect = pygame.Rect(20, 70 + idx * 50, 360, 40)
                    pygame.draw.rect(select_panel, (200, 200, 200, 150), button_rect, border_radius=5)
                    text_surface = font.render(f"{idx + 1}. {member.name}", True, BLACK)
                    select_panel.blit(text_surface, (30, 80 + idx * 50))
                    buttons2.append((button_rect, member))
                
                # 添加退出按鈕
                exit_rect = pygame.Rect(20, 70 + len(team.members) * 50, 360, 40)
                pygame.draw.rect(select_panel, (255, 200, 200, 150), exit_rect, border_radius=5)
                exit_text = font.render("Exit", True, RED)
                select_panel.blit(exit_text, (30, 80 + len(team.members) * 50))
                buttons2.append((exit_rect, "Exit"))
                
                # 顯示面板
                screen.blit(select_panel, (20, 20))
                pygame.display.flip()
                
                selected_member = DisplaySystem.handle_click(buttons2)
                if selected_member == "Exit":
                    continue
                if selected_member:
                    team.fire(selected_member.name)
            
            elif action == "5. Add Member":
                # 動態計算選擇面板大小
                from rpg_game.src.character import Character  # 添加這行導入
                DisplaySystem.clear_screen(team_bg)
                if not team.backpack.items:
                    select_height = 120  # 標題 + 空背包訊息 + 間距
                else:
                    character_count = sum(1 for item in team.backpack.items.values() if isinstance(item['item'], Character))
                    select_height = 70 + character_count * 50 + 50  # 標題 + 角色列表 + 退出按鈕
                
                select_panel = pygame.Surface((400, select_height), pygame.SRCALPHA)
                select_panel.fill((255, 255, 255, 200))
                
                # 顯示標題
                title = font.render("Select Character to Add", True, BLACK)
                select_panel.blit(title, (20, 20))
                
                if not team.backpack.items:
                    # 顯示空背包訊息
                    msg = font.render("Backpack is empty", True, RED)
                    select_panel.blit(msg, (20, 70))
                    screen.blit(select_panel, (20, 20))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    continue
                
                # 顯示可選角色列表
                buttons2 = []
                y_offset = 70
                for idx, (item_name, data) in enumerate(team.backpack.items.items()):
                    if isinstance(data['item'], Character):
                        button_rect = pygame.Rect(20, y_offset, 360, 40)
                        pygame.draw.rect(select_panel, (200, 200, 200, 150), button_rect, border_radius=5)
                        text_surface = font.render(f"{idx + 1}. {item_name}", True, BLACK)
                        select_panel.blit(text_surface, (30, y_offset + 10))
                        buttons2.append((button_rect, data['item']))
                        y_offset += 50
                
                # 添加退出按鈕
                exit_rect = pygame.Rect(20, y_offset, 360, 40)
                pygame.draw.rect(select_panel, (255, 200, 200, 150), exit_rect, border_radius=5)
                exit_text = font.render("Exit", True, RED)
                select_panel.blit(exit_text, (30, y_offset + 10))
                buttons2.append((exit_rect, "Exit"))
                
                # 顯示面板
                screen.blit(select_panel, (20, 20))
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

        screen = pygame.display.set_mode((1200, 700))
        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 48)
        
        while True:
            screen.blit(store, (0, 0))
            
            # Panel parameters
            panel_width = 400
            options = [
                "1. STR +1 (50 coins)",
                "2. VIT +1 (50 coins)",
                "3. AGL +1 (50 coins)",
                "4. DEX +1 (50 coins)",
                "5. INT +1 (50 coins)",
                "6. Gacha (200 coins)",
                "7. Exit"
            ]
            button_height = 50
            button_spacing = 20
            panel_height = 80 + len(options) * (button_height + button_spacing) + 40
            panel_x = 20
            panel_y = 20
            
            # Create semi-transparent panel
            panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            panel.fill((255, 255, 255, 200))
            
            # Display title and coins
            title = title_font.render("Store", True, BLACK)
            title_rect = title.get_rect(left=20, top=20)
            panel.blit(title, title_rect)
            
            coins = font.render(f"Coins: {team.coin}", True, BLUE)
            panel.blit(coins, (20, 60))
            
            # Calculate button positions
            button_width = 360
            start_y = 100
            
            buttons = []
            for i, option in enumerate(options):
                button_rect = pygame.Rect(20, start_y + i * (button_height + button_spacing), button_width, button_height)
                pygame.draw.rect(panel, (200, 200, 200, 165), button_rect, border_radius=10)
                
                text_surface = font.render(option, True, BLACK)
                text_rect = text_surface.get_rect(center=button_rect.center)
                panel.blit(text_surface, text_rect)
                
                buttons.append((button_rect, option))
            
            screen.blit(panel, (panel_x, panel_y))
            pygame.display.flip()
            
            action = DisplaySystem.handle_click(buttons)
            if action == "7. Exit":
                break
            elif action in ["1. STR +1 (50 coins)", "2. VIT +1 (50 coins)", "3. AGL +1 (50 coins)", "4. DEX +1 (50 coins)", "5. INT +1 (50 coins)"]:
                DisplaySystem.clear_screen(store)
                attribute_map = {
                    "1. STR +1 (50 coins)": "str",
                    "2. VIT +1 (50 coins)": "vit",
                    "3. AGL +1 (50 coins)": "agl",
                    "4. DEX +1 (50 coins)": "dex",
                    "5. INT +1 (50 coins)": "intel"
                }
                attribute = attribute_map[action]
                if team.coin < 50:
                    DisplaySystem.show_message("Not enough coins", color=RED)
                    pygame.time.wait(1200)
                    continue
                
                # Create character selection panel
                char_panel = pygame.Surface((400, 230), pygame.SRCALPHA)
                char_panel.fill((255, 255, 255, 200))
                
                title = font.render("Select Character", True, BLACK)
                char_panel.blit(title, (20, 20))
                
                buttons2 = []
                y_offset = 70
                for idx, member in enumerate(team.members):
                    button_rect = pygame.Rect(20, y_offset, 360, 40)
                    pygame.draw.rect(char_panel, (200, 200, 200, 150), button_rect, border_radius=5)
                    text_surface = font.render(f"{idx + 1}. {member.name} (Lv.{member.level})", True, BLACK)
                    char_panel.blit(text_surface, (30, y_offset + 10))
                    buttons2.append((button_rect, member))
                    y_offset += 50
                
                exit_rect = pygame.Rect(20, y_offset, 360, 40)
                pygame.draw.rect(char_panel, (255, 200, 200, 150), exit_rect, border_radius=5)
                exit_text = font.render("Exit", True, RED)
                char_panel.blit(exit_text, (30, y_offset + 10))
                buttons2.append((exit_rect, "Exit"))
                
                screen.blit(char_panel, (20, 20))
                pygame.display.flip()
                
                selected_member = DisplaySystem.handle_click(buttons2)
                if selected_member == "Exit":
                    continue
                if selected_member:
                    team.spend_coin(50)
                    setattr(selected_member, attribute, getattr(selected_member, attribute) + 1)
                    DisplaySystem.show_message(f"{selected_member.name} {attribute.upper()} +1", color=GREEN, background=store)
                    pygame.time.wait(1200)
            
            elif action == "6. Gacha (200 coins)":
                if team.coin < 200:
                    DisplaySystem.clear_screen(store)
                    DisplaySystem.show_message("Not enough coins", color=RED)
                    pygame.time.wait(1200)
                    continue

                DisplaySystem.clear_screen(store)
                # Create gacha panel
                gacha_panel = pygame.Surface((400, 230), pygame.SRCALPHA)
                gacha_panel.fill((255, 255, 255, 200))
                
                title = font.render("Choose Pool", True, BLACK)
                gacha_panel.blit(title, (20, 20))
                
                buttons2 = [
                    (pygame.Rect(20, 70, 360, 40), "Character"),
                    (pygame.Rect(20, 120, 360, 40), "Equipment"),
                    (pygame.Rect(20, 170, 360, 40), "Exit")
                ]
                
                for rect, label in buttons2:
                    pygame.draw.rect(gacha_panel, (200, 200, 200, 150), rect, border_radius=5)
                    text_surface = font.render(label, True, RED if label == "Exit" else BLACK)
                    gacha_panel.blit(text_surface, (30, rect.y + 10))
                
                screen.blit(gacha_panel, (20, 20))
                pygame.display.flip()
                
                pool_choice = DisplaySystem.handle_click(buttons2)
                if pool_choice == "Exit":
                    continue
                
                if pool_choice == "Character":
                    gacha_character = gacha_draw_character()
                    team.backpack.add_item(gacha_character, 1)
                    DisplaySystem.show_message(f"Got {gacha_character.name}!", color=GREEN, background=store)
                    pygame.time.wait(1200)
                elif pool_choice == "Equipment":
                    gacha_equipment = gacha_draw_equipment()
                    team.backpack.add_item(gacha_equipment, 1)
                    DisplaySystem.show_message(f"Got {gacha_equipment.name}!", color=GREEN, background=store)
                    pygame.time.wait(1200)
                
                team.spend_coin(200)
                pygame.time.wait(1200)

    @staticmethod
    def upgrade_menu(team):
        from rpg_game.src.equipment import Equipment
        from rpg_game.src.character import Character
        from rpg_game.src.UpgradeSystem import UpgradeSystem
        screen = pygame.display.set_mode((1200, 700))
        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 48)
        
        while True:
            screen.fill(WHITE)
            screen.blit(upgrade_bg, (390, 90))  # 保持原來的背景位置
            
            # Panel parameters
            panel_width = 400  # 縮短面板寬度
            options = [
                "1. Level Up Character",
                "2. Upgrade Attributes",
                "3. Upgrade Equipment",
                "4. Return"
            ]
            button_height = 50
            button_spacing = 20
            panel_height = 80 + len(options) * (button_height + button_spacing) + 40
            panel_x = 20
            panel_y = 20
            
            # Create semi-transparent panel
            panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            panel.fill((255, 255, 255, 200))
            
            # Display title
            title = title_font.render("Upgrade System", True, BLACK)
            title_rect = title.get_rect(left=20, top=20)
            panel.blit(title, title_rect)
            
            # Calculate button positions
            button_width = 360  # 縮短按鈕寬度
            start_y = 80
            
            buttons = []
            for i, option in enumerate(options):
                button_rect = pygame.Rect(20, start_y + i * (button_height + button_spacing), button_width, button_height)
                pygame.draw.rect(panel, (200, 200, 200, 150), button_rect, border_radius=10)
                
                text_surface = font.render(option, True, BLACK)
                text_rect = text_surface.get_rect(center=button_rect.center)
                panel.blit(text_surface, text_rect)
                
                buttons.append((button_rect, option))
            
            screen.blit(panel, (panel_x, panel_y))
            pygame.display.flip()
            
            action = DisplaySystem.handle_click(buttons)
            if action == "4. Return":
                break
            elif action == "1. Level Up Character":
                pygame.display.flip()
                screen.fill(WHITE)
                screen.blit(upgrade_bg, (390, 90))
                if not team.members:
                    DisplaySystem.show_message("No characters in team", color=RED)
                    pygame.time.wait(2000)
                    continue
                
                # Create character selection panel
                char_panel = pygame.Surface((400, 300), pygame.SRCALPHA)
                char_panel.fill((255, 255, 255, 200))
                
                title = font.render("Select Character to Level Up", True, BLACK)
                char_panel.blit(title, (20, 20))
                
                buttons2 = []
                y_offset = 70
                for idx, member in enumerate(team.members):
                    button_rect = pygame.Rect(20, y_offset, 360, 40)
                    pygame.draw.rect(char_panel, (200, 200, 200, 150), button_rect, border_radius=5)
                    text_surface = font.render(f"{idx + 1}. {member.name} (Lv.{member.level}) - EXP: {member.exp}/{member.exp_to_next_level}", True, BLACK)
                    char_panel.blit(text_surface, (30, y_offset + 10))
                    buttons2.append((button_rect, member))
                    y_offset += 50
                
                exit_rect = pygame.Rect(20, y_offset, 360, 40)
                pygame.draw.rect(char_panel, (255, 200, 200, 150), exit_rect, border_radius=5)
                exit_text = font.render("Exit", True, RED)
                char_panel.blit(exit_text, (30, y_offset + 10))
                buttons2.append((exit_rect, "Exit"))
                
                screen.blit(char_panel, (20, 20))
                pygame.display.flip()
                
                selected_member = DisplaySystem.handle_click(buttons2)
                if selected_member == "Exit":
                    continue
                if selected_member:
                    UpgradeSystem.level_up(team, selected_member)
            
            elif action == "2. Upgrade Attributes":
                pygame.display.flip()
                screen.fill(WHITE)
                screen.blit(upgrade_bg, (390, 90))
                if not team.members:
                    DisplaySystem.show_message("No characters in team", color=RED)
                    pygame.time.wait(2000)
                    continue
                
                # Create character selection panel
                char_panel = pygame.Surface((400, 300), pygame.SRCALPHA)
                char_panel.fill((255, 255, 255, 200))
                
                title = font.render("Select Character to Upgrade", True, BLACK)
                char_panel.blit(title, (20, 20))
                
                buttons2 = []
                y_offset = 70
                for idx, member in enumerate(team.members):
                    button_rect = pygame.Rect(20, y_offset, 360, 40)
                    pygame.draw.rect(char_panel, (200, 200, 200, 150), button_rect, border_radius=5)
                    text_surface = font.render(f"{idx + 1}. {member.name} (Lv.{member.level})", True, BLACK)
                    char_panel.blit(text_surface, (30, y_offset + 10))
                    buttons2.append((button_rect, member))
                    y_offset += 50
                
                exit_rect = pygame.Rect(20, y_offset, 360, 40)
                pygame.draw.rect(char_panel, (255, 200, 200, 150), exit_rect, border_radius=5)
                exit_text = font.render("Exit", True, RED)
                char_panel.blit(exit_text, (30, y_offset + 10))
                buttons2.append((exit_rect, "Exit"))
                
                screen.blit(char_panel, (20, 20))
                pygame.display.flip()
                
                selected_member = DisplaySystem.handle_click(buttons2)
                if selected_member == "Exit":
                    continue
                if selected_member:
                    pygame.display.flip()
                    screen.fill(WHITE)
                    screen.blit(upgrade_bg, (390, 90))
                    attr_panel = pygame.Surface((400, 370), pygame.SRCALPHA)
                    attr_panel.fill((255, 255, 255, 200))
                    
                    title = font.render(f"Select Attribute to Upgrade", True, BLACK)
                    attr_panel.blit(title, (20, 20))
                    
                    attributes = ["STR", "VIT", "AGL", "DEX", "INT"]
                    buttons3 = []
                    y_offset = 70
                    for attr in attributes:
                        button_rect = pygame.Rect(20, y_offset, 360, 40)
                        pygame.draw.rect(attr_panel, (200, 200, 200, 150), button_rect, border_radius=5)
                        attr_lower = "intel" if attr == "INT" else attr.lower()
                        current_value = getattr(selected_member, attr_lower)
                        text_surface = font.render(f"{attr}: {current_value}", True, BLACK)
                        attr_panel.blit(text_surface, (30, y_offset + 10))
                        buttons3.append((button_rect, attr))
                        y_offset += 50
                    
                    exit_rect = pygame.Rect(20, y_offset, 360, 40)
                    pygame.draw.rect(attr_panel, (255, 200, 200, 150), exit_rect, border_radius=5)
                    exit_text = font.render("Exit", True, RED)
                    attr_panel.blit(exit_text, (30, y_offset + 10))
                    buttons3.append((exit_rect, "Exit"))
                    
                    screen.blit(attr_panel, (20, 20))
                    pygame.display.flip()
                    
                    selected_attr = DisplaySystem.handle_click(buttons3)
                    if selected_attr == "Exit":
                        continue
                    if selected_attr:
                        attr_lower = "intel" if selected_attr == "INT" else selected_attr.lower()
                        UpgradeSystem.upgrade_attribute(team, selected_member, attr_lower)
            
            elif action == "3. Upgrade Equipment":
                pygame.display.flip()
                screen.fill(WHITE)
                screen.blit(upgrade_bg, (390, 90))
                
                # 檢查背包是否為空
                if not team.backpack.items:
                    DisplaySystem.show_message("Backpack is empty", color=RED)
                    pygame.time.wait(2000)
                    continue
                
                # 創建裝備選擇面板
                eq_panel = pygame.Surface((400, 300), pygame.SRCALPHA)
                eq_panel.fill((255, 255, 255, 200))
                
                title = font.render("Select Equipment to Upgrade", True, BLACK)
                eq_panel.blit(title, (20, 20))
                
                # 從背包中篩選出裝備類物品
                equipment_items = [(name, data) for name, data in team.backpack.items.items() 
                                 if isinstance(data['item'], Equipment)]
                
                if not equipment_items:
                    DisplaySystem.show_message("No equipment in backpack", color=RED)
                    pygame.time.wait(2000)
                    continue
                
                buttons2 = []
                y_offset = 70
                for idx, (item_name, data) in enumerate(equipment_items):
                    eq = data['item']
                    button_rect = pygame.Rect(20, y_offset, 360, 40)
                    pygame.draw.rect(eq_panel, (200, 200, 200, 150), button_rect, border_radius=5)
                    text_surface = font.render(f"{idx + 1}. {item_name} (Lv.{eq.level})", True, BLACK)
                    eq_panel.blit(text_surface, (30, y_offset + 10))
                    buttons2.append((button_rect, item_name))
                    y_offset += 50
                
                exit_rect = pygame.Rect(20, y_offset, 360, 40)
                pygame.draw.rect(eq_panel, (255, 200, 200, 150), exit_rect, border_radius=5)
                exit_text = font.render("Exit", True, RED)
                eq_panel.blit(exit_text, (30, y_offset + 10))
                buttons2.append((exit_rect, "Exit"))
                
                screen.blit(eq_panel, (20, 20))
                pygame.display.flip()
                
                selected_item = DisplaySystem.handle_click(buttons2)
                if selected_item == "Exit":
                    continue
                if selected_item:
                    eq = team.backpack.items[selected_item]['item']
                    UpgradeSystem.upgrade_equipment(team, eq)