import pygame
from rpg_game.src.team import Team
from rpg_game.src.backpack import Backpack
from rpg_game.src.display import DisplaySystem, BLUE, RED, WHITE
from rpg_game.src.job import Archer, Warrior, Mage, Healer, Tank, KingKnight, Shooter
from rpg_game.src.monster import Monster
from rpg_game.src.skill import Skill
from final_project import Battle

pygame.font.init()
screen =pygame.display.set_mode((1200, 700))
image = pygame.image.load("C:/CODing/PYTHON/final_project1/background.jpg")
image_s = pygame.image.load("C:/CODing/PYTHON/final_project1/store.jpg")
image_b = pygame.image.load("C:/CODing/PYTHON/final_project1/battle.jpg")
background = pygame.transform.scale(image, (1200, 700))
store = pygame.transform.scale(image_s, (1200, 700))
battle = pygame.transform.scale(image_b, (1200, 700))

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    screen.fill((0, 0, 0))  # 清空螢幕
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # 進入遊戲顯示開始畫面
    font = pygame.font.Font(None, 72)
    start_text = font.render("RPG Game Start", True, BLUE)
    exit_text = font.render("Exit", True, RED)
    start_rect = start_text.get_rect(center=(600, 250))
    exit_rect = exit_text.get_rect(center=(600, 400))
    screen.blit(start_text, start_rect)
    screen.blit(exit_text, exit_rect)
    pygame.display.flip()

    # 等待玩家選擇開始或退出
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_rect.collidepoint(mouse_pos):
                    waiting = False
                elif exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

    team = Team()
    team.backpack = Backpack(team)  # 傳入 team 作為參數
    
    # 創建初始角色（不顯示訊息）
    archer1 = Archer("Archer1", 1, 5, 5, 5, 5, 5)
    team.members.append(archer1.create_character())
    team.members[-1].team = team
    warrior = Warrior("Warrior1", 1, 5, 5, 5, 5, 5)
    team.members.append(warrior.create_character())
    team.members[-1].team = team
    
    round_number = 1  # 初始化輪次
    while True:
        screen
        pygame.display.flip()

        buttons = DisplaySystem.show_main_menu()  # 顯示主選單並返回按鈕

        action = DisplaySystem.handle_click(buttons)  # 等待玩家點擊選項
        if action == "1. Show Team":
            DisplaySystem.show_team(team)
        elif action == "2. Battle":
            monster = Monster(15, 500, "WATER", [Skill("Fireball", 1, 1)], "berserk", round_number)
            battle = Battle(team, monster, round_number)
            battle.start()
            round_number += 1  # 每次戰鬥結束後增加輪次
        elif action == "3. Store":
            DisplaySystem.store(team)
        elif action == "4. Team Management":
            DisplaySystem.show_team_menu(team)
        elif action == "5. Backpack":
            DisplaySystem.backpack_menu(team.backpack)  # 傳入 team.backpack 而非 team
        elif action == "6. Upgrade Character/Equipment":
            DisplaySystem.upgrade_menu(team)
        elif action == "7. Exit Game":
            DisplaySystem.show_message("Exiting game. Goodbye!", color=RED)
            pygame.quit()
            break
        else:
            DisplaySystem.show_message("Invalid choice. Please select a valid option.", color=RED)