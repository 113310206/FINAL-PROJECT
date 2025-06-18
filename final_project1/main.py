import pygame
from rpg_game.src.team import Team
from rpg_game.src.backpack import Backpack
from rpg_game.src.display import DisplaySystem, BLUE, RED, WHITE
from rpg_game.src.job import Archer, Warrior, Mage, Healer, Tank, KingKnight, Shooter
from rpg_game.src.monster import Monster
from rpg_game.src.skill import Skill
from final_project import Battle

pygame.font.init()
screen = pygame.display.set_mode((1200, 700))
image_link = pygame.image.load("link.jpg")  # 進入畫面
image = pygame.image.load("background1.jpg")     # 主畫面
image_s = pygame.image.load("store.jpg")
image_b = pygame.image.load("battle.jpg")
background = pygame.transform.scale(image, (1200, 700))
link_bg = pygame.transform.scale(image_link, (1200, 700))
store = pygame.transform.scale(image_s, (1200, 700))
battle = pygame.transform.scale(image_b, (1200, 700))

game_running = True
# 只顯示進入畫面一次
screen.blit(link_bg, (0, 0))
pygame.display.flip()
font = pygame.font.Font(None, 72)
start_text = font.render("RPG Game Start", True, BLUE)
exit_text = font.render("Exit", True, RED)
start_rect = start_text.get_rect(topright=(1150, 30))   # 右上角
exit_rect = exit_text.get_rect(bottomleft=(50, 670))    # 左下角
screen.blit(start_text, start_rect)
screen.blit(exit_text, exit_rect)
pygame.display.flip()
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

def choose_job_and_create_character(team):
    from rpg_game.src.job import Archer, Warrior, Mage, Healer, Tank, KingKnight, Shooter
    from rpg_game.src.display import DisplaySystem
    DisplaySystem.clear_screen(background)  
    font = pygame.font.Font(None, 40)
    jobs = [
        ("Archer", Archer),
        ("Warrior", Warrior),
        ("Mage", Mage),
        ("Healer", Healer),
        ("Tank", Tank),
        ("KingKnight", KingKnight),
        ("Shooter", Shooter)
    ]
    panel_width, panel_height = 500, 80 + len(jobs) * 60
    panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel.fill((255, 255, 255, 220))
    title = font.render("Choose Your Character", True, BLUE)
    panel.blit(title, (20, 20))
    buttons = []
    y_offset = 70
    for idx, (job_name, job_cls) in enumerate(jobs):
        button_rect = pygame.Rect(20, y_offset, 460, 40)
        pygame.draw.rect(panel, (200, 200, 200, 180), button_rect, border_radius=8)
        text_surface = font.render(f"{idx+1}. {job_name}", True, (0, 0, 0))
        panel.blit(text_surface, (30, y_offset + 8))
        buttons.append((button_rect, job_cls))
        y_offset += 50
    screen.blit(panel, (650, 150))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, job_cls in buttons:
                    if rect.move(350, 150).collidepoint(mouse_pos):
                        # 這裡可彈出命名視窗，這裡先用預設名
                        char = job_cls(f"YOU is {job_cls.__name__}", 1, 5, 5, 5, 5, 5).create_character()
                        char.team = team
                        return char

team = Team()
team.backpack = Backpack(team)
player_char = choose_job_and_create_character(team)
team.members.append(player_char)
DisplaySystem.show_message(f"{player_char.name} has joined the team!", background=background ,position=(900, 350), color=BLUE)
pygame.time.wait(1200)
team.members[-1].team = team



round_number = 1
while game_running:
    # 主畫面顯示 ground
    screen.blit(background, (0, 0))
    pygame.display.flip()
    buttons = DisplaySystem.show_main_menu()
    action = DisplaySystem.handle_click(buttons)
    if action == "1. Show Team":
        DisplaySystem.show_team(team)
    elif action == "2. Battle":
        monster = Monster(15, 500, "WATER", [Skill("Fireball", 10, 20)], "berserk", round_number)
        battle = Battle(team, monster, round_number)
        battle.start()
        round_number += 1  # 每次戰鬥結束後增加輪次
    elif action == "3. Store":
        DisplaySystem.store(team)
    elif action == "4. Team Management":
        DisplaySystem.show_team_menu(team)
    elif action == "5. Backpack":
        DisplaySystem.show_backpack(team.backpack)  # 傳入 team.backpack 而非 team
    elif action == "6. Upgrade Character/Equipment":
        DisplaySystem.upgrade_menu(team)
    elif action == "7. Exit Game":
        DisplaySystem.show_message("Exiting game. Goodbye!", color=RED)
        pygame.time.wait(1000)
        pygame.quit()
        break
    else:
        DisplaySystem.show_message("Invalid choice. Please select a valid option.", color=RED)