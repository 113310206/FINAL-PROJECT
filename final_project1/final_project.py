from rpg_game.src.character import Character
from rpg_game.src.job import Warrior, Mage, Archer, Healer, Tank, KingKnight, Shooter
from rpg_game.src.equipment import Equipment
from rpg_game.src.skill import Skill, ElementalSkill, SupportElementalSkill
from rpg_game.src.team import Team  # 移除 team_menu 依賴
from rpg_game.src.display import DisplaySystem
from rpg_game.src.backpack import Backpack
from rpg_game.src.UpgradeSystem import UpgradeSystem
import random
import math
import time
import pygame  # 新增 pygame 匯入

# 定義顏色
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((1200, 700))
image_v = pygame.image.load("vectory.jpg")
imafe_b = pygame.image.load("battle.jpg")
image_cop = pygame.image.load("cat-open.jpg")
image_c1 = pygame.image.load("cat1.jpg")
image_b1 = pygame.image.load("boss1.jpg")
image_boss = pygame.image.load("boss.jpg")
vectory = pygame.transform.scale(image_v, (1200, 700))
battle = pygame.transform.scale(imafe_b, (1200, 700))
cat1 = pygame.transform.scale(image_c1, (200, 200))  # 縮小貓咪圖片
boss = pygame.transform.scale(image_boss, (200, 200))  # 縮小boss圖片
cat_open = pygame.transform.scale(image_cop, (200, 200))  # 縮小貓咪開啟圖片
boss1 = pygame.transform.scale(image_b1, (200, 200))  # 縮小boss1圖片


class Monster:
    def __init__(self, hp, attack, element=None, skills=None, behavior=None, round_number=1):
        self.hp = hp + pow(round_number,2) *50  # 每輪增加生命值
        self.attack = attack + pow(round_number, 2)*5  # 每輪增加攻擊力
        self.element = element
        self.skills = skills or []
        self.behavior = behavior or "normal"
        self.name = f"Monster (Round {round_number})"
        self.job = type("Job", (), {"job_name": "Monster"})()  # 讓 monster 有 job 屬性且 job_name 為"怪物"

    def print(self):
        DisplaySystem.show_monster(self)

    def try_crit(self):
        return random.random() < 0.25

    def act(self, team):
        # 怪物行為模式
        if self.behavior == "berserk" and self.hp < 100:
            print("怪物進入狂暴狀態，攻擊力提升！")
            self.attack *= 2
            self.behavior = "normal"
        elif self.behavior == "heal" and self.hp < 100:
            print("怪物自我治療！")
            self.hp += 50
        else:
            # 怪物攻撃（技能或普通攻擊，只執行一次）
            if self.skills and random.random() < 0.5:
                skill = random.choice(self.skills)
                print(f"怪物使用技能：{skill.name}！")
                for m in team.members:
                    if m.is_alive():
                        # 新增閃避判斷
                        if hasattr(m, "take_damage"):
                            if not m.take_damage(skill.damage):
                                continue  # 閃避成功
                        else:
                            m.hp -= skill.damage
                DisplaySystem.show_monster_attack_message(self, None, skill.damage)
            else:
                crit = self.try_crit()
                element_boost = any(m.element == self.element for m in team.members if m.is_alive())
                if random.random() < 0.5:  # 隨機選擇單一目標攻擊或全體攻擊
                    target = random.choice([m for m in team.members if m.is_alive()])
                    total_damage = self.attack * (2 if crit else 1) * (1.5 if element_boost else 1)
                    # 新增閃避判斷
                    if hasattr(target, "take_damage"):
                        if not target.take_damage(total_damage):
                            DisplaySystem.show_monster_attack_message(self, target, 0, crit=crit, element_boost=element_boost)
                            return
                    else:
                        target.hp -= total_damage
                    DisplaySystem.show_monster_attack_message(self, target, total_damage, crit=crit, element_boost=element_boost)
                else:
                    print("怪物進行全體攻擊！")
                    total_damage = (self.attack // 2) * (2 if crit else 1) * (1.5 if element_boost else 1)
                    for m in team.members:
                        if m.is_alive():
                            # 新增閃避判斷
                            if hasattr(m, "take_damage"):
                                if not m.take_damage(total_damage):
                                    continue
                            else:
                                m.hp -= total_damage
                    DisplaySystem.show_monster_attack_message(self, None, total_damage, crit=crit, element_boost=element_boost)

class BonusSystem:
    @staticmethod
    def apply_equipment_bonus(character, equipment, reverse=False):
        factor = -1 if reverse else 1
        for k, v in equipment.stat_bonus.items():
            if hasattr(character, k):
                setattr(character, k, getattr(character, k) + factor * v * equipment.level)
        # 添加武器攻擊加成
        if equipment.eq_type == "weapon":
            character.attack_power += factor * equipment.stat_bonus.get("atk", 0) * equipment.level

    @staticmethod
    def apply_weapon_bonus(character, weapon):
        if weapon.eq_type == "weapon":
            character.attack_power += weapon.stat_bonus.get("str", 0) * weapon.level

    @staticmethod
    def apply_job_bonus(character, job):
        for k, v in job.stat_bonus.items():
            if hasattr(character, k):
                setattr(character, k, getattr(character, k) + v)

    @staticmethod
    def reset_equipment_bonus(character):
        for eq in character.equipment.values():
            if eq:
                BonusSystem.apply_equipment_bonus(character, eq, reverse=True)

    @staticmethod
    def apply_position_bonus(character):
        # 定義站位加成
        position_bonus = {
            "front": {"str": 2, "vit": 2},
            "mid": {"dex": 2, "agl": 2},
            "back": {"intel": 3, "mp": 5}
        }
        if character.position in position_bonus:
            for k, v in position_bonus[character.position].items():
                if hasattr(character, k):
                    setattr(character, k, getattr(character, k) + v)
            print(f"{character.name} 在 {character.position} 位置獲得加成：{position_bonus[character.position]}")

    @staticmethod
    def reset_position_bonus(character):
        # 定義站位加成（重置時使用）
        position_bonus = {
            "front": {"str": 2, "vit": 2},
            "mid": {"dex": 2, "agl": 2},
            "back": {"intel": 3, "mp": 5}
        }
        if character.position in position_bonus:
            for k, v in position_bonus[character.position].items():
                if hasattr(character, k):
                    setattr(character, k, getattr(character, k) - v)
            print(f"{character.name} 在 {character.position} 位置的加成已重置。")

def random_character(team):
    role = random.randint(1, 7)
    print("Enter character details (name, str, vit, agl, dex, intel): ")
    print("The total attribute points cannot exceed 15.")
    print("And the maximum value for each attribute is 10.")
    while True:
        name = input("Name: ").strip()
        try:
            s, v, ag, d, i = map(int, input("Attributes (str vit agl dex intel): ").split())
        except:
            print("Invalid input. Please try again.")
            continue
        if not name:
            print("Name cannot be empty. Please try again.")
        elif s + v + ag + d + i > 15:
            print("Total attribute points exceed 15. Please try again.")
        elif any(x > 10 or x < 0 for x in [s, v, ag, d, i]):
            print("Each attribute must be 0~10. Please try again.")
        else:
            break
    level = 3
    if role == 1:
        job_obj = Warrior(name, level, s, v, ag, d, i)
    elif role == 2:
        job_obj = Mage(name, level, s, v, ag, d, i)
    elif role == 3:
        job_obj = Archer(name, level, s, v, ag, d, i)
    elif role == 4:
        job_obj = Healer(name, level, s, v, ag, d, i)
    elif role == 5:
        job_obj = Tank(name, level, s, v, ag, d, i)
    elif role == 6:
        job_obj = KingKnight(name, level, s, v, ag, d, i)
    else:
        job_obj = Shooter(name, level, s, v, ag, d, i)
    new_character = job_obj.create_character()
    team.backpack.add_item(name)  # 將角色放入背包
    print(f"{name} has been added to the backpack.\n")

def get_valid_choice():
    while True:
        choice = input().strip().upper()
        if choice in ("Y", "N"):
            return choice == "Y"
        print("Invalid input. Please enter 'Y' or 'N'.")

class Battle:
    def __init__(self, team, monster, round_number=1):
        self.team = team
        self.monster = monster
        self.round_number = round_number

    def start(self):
        while True:
            # battle.jpg 背景持續顯示
            screen.blit(battle, (0, 0))
            # 只顯示 battle 背景，不再顯示 cat1, boss
            pygame.display.flip()
            DisplaySystem.show_battle_status(
                self.team,
                self.monster,
                background_override=battle,
                extra_draw=None  # 不再顯示 cat1, boss
            )

            for idx, member in enumerate(self.team.members):
                if not member.is_alive():
                    continue

                while True:
                    # battle 背景持續顯示
                    screen.blit(battle, (0, 0))
                    # 只在選單顯示 cat1, boss
                    screen.blit(cat1, (450, 400))
                    screen.blit(boss, (850, 300))
                    pygame.display.flip()
                    DisplaySystem.show_battle_status(
                        self.team,
                        self.monster,
                        background_override=battle,
                        extra_draw=lambda: (screen.blit(cat1, (450, 400)), screen.blit(boss, (850, 300)))
                    )
                    font = pygame.font.Font(None, 24)
                    options = [
                        "1. Normal Attack",
                        "2. Use Skill",
                        "3. Use Element Skill",
                        "4. Use Element Skill on Teammate",
                        "5. Upgrade System",
                        "6. Equip/Unequip",
                        "7. View Backpack",
                        "8. Skip Turn"
                    ]
                    panel_width = 400
                    option_height = 32
                    panel_height = 30 + 40 + len(options) * option_height + 20  # 上邊距+標題+選項+下邊距
                    panel_x, panel_y = 40, 270

                    # 畫半透明白底
                    panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
                    panel_surface.fill((255, 255, 255, 180))
                    screen.blit(panel_surface, (panel_x, panel_y))

                    # 標題
                    title_text = font.render(f"{member.name}'s Turn (HP: {member.hp}/{member.max_hp}, MP: {member.mp}/{member.max_mp})", True, BLACK)
                    screen.blit(title_text, (panel_x + 20, panel_y + 15))

                    # 選項
                    buttons = []
                    for i, option in enumerate(options):
                        text_surface = font.render(option, True, BLACK)
                        text_rect = text_surface.get_rect(topleft=(panel_x + 20, panel_y + 55 + i * option_height))
                        screen.blit(text_surface, text_rect)
                        buttons.append((text_rect, option))
                    pygame.display.flip()

                    action = DisplaySystem.handle_click(buttons)
                    # 執行選項後，cat open/boss1 顯示於攻擊訊息
                    if action == "1. Normal Attack":
                        crit = member.try_crit(self.monster)
                        total_damage = member.attack_power * (2 if member.element_boost else 1) * (2 if crit else 1)
                        member.element_boost = False
                        DisplaySystem.show_attack_message(
                            member, self.monster, total_damage, crit=crit,
                            background=battle,
                            extra_draw=lambda: (screen.blit(cat_open, (450, 400)), screen.blit(boss1, (850, 300)))
                        )
                        self.monster.hp -= total_damage
                        break
                    elif action == "2. Use Skill":
                        if member.skill:
                            crit = member.try_crit(self.monster)
                            total_damage = member.skill.damage * (2 if crit else 1)
                            DisplaySystem.show_skill_use(
                                member, member.skill, self.monster, total_damage, crit=crit,
                                background=battle,
                                extra_draw=lambda: (screen.blit(cat_open, (450, 400)), screen.blit(boss1, (850, 300)))
                            )
                            self.monster.hp -= total_damage
                        break
                    elif action == "3. Use Element Skill":
                        if member.element_skill:
                            DisplaySystem.show_elementSkill_use(
                                member, member.element_skill, self.monster, member.element_skill.damage,
                                background=battle,
                                extra_draw=lambda: (screen.blit(cat_open, (450, 400)), screen.blit(boss1, (850, 300)))
                            )
                            # 使用元素技能後自動切畫面，不再等待玩家操作
                            self.monster.hp -= member.element_skill.damage
                        break
                    elif action == "4. Use Element Skill on Teammate":
                        DisplaySystem.clear_screen(battle)
                        teammates = [m for m in self.team.members if m.is_alive() and m != member]
                        if not teammates:
                            # 創建錯誤訊息面板
                            error_panel = pygame.Surface((400, 100), pygame.SRCALPHA)
                            error_panel.fill((255, 255, 255, 200))
                            error_text = font.render("No teammates available for support.", True, RED)
                            text_rect = error_text.get_rect(center=(200, 50))
                            error_panel.blit(error_text, text_rect)
                            screen.blit(error_panel, (20, 20))
                            pygame.display.flip()
                            pygame.time.wait(1200)
                            continue

                        # 創建隊友選擇面板
                        panel_width = 400
                        panel_height = 120 + len(teammates) * 60  # 標題 + 隊友列表 + 退出按鈕
                        select_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
                        select_panel.fill((255, 255, 255, 200))

                        # 顯示標題
                        title = font.render("Select a teammate to support:", True, BLACK)
                        select_panel.blit(title, (20, 20))

                        # 顯示隊友列表
                        buttons = []
                        for i, teammate in enumerate(teammates):
                            # 創建隊友信息按鈕
                            button_rect = pygame.Rect(20, 70 + i * 60, 360, 50)
                            pygame.draw.rect(select_panel, (200, 200, 200, 150), button_rect, border_radius=10)
                            
                            # 顯示隊友詳細信息
                            info_text = f"{teammate.name} (HP: {teammate.hp}/{teammate.max_hp}, MP: {teammate.mp}/{teammate.max_mp})"
                            text_surface = font.render(info_text, True, BLACK)
                            text_rect = text_surface.get_rect(center=button_rect.center)
                            select_panel.blit(text_surface, text_rect)
                            
                            buttons.append((button_rect, teammate))

                        # 添加退出按鈕
                        exit_rect = pygame.Rect(20, 70 + len(teammates) * 60, 360, 40)
                        pygame.draw.rect(select_panel, (255, 200, 200, 150), exit_rect, border_radius=10)
                        exit_text = font.render("Exit", True, RED)
                        text_rect = exit_text.get_rect(center=exit_rect.center)
                        select_panel.blit(exit_text, text_rect)
                        buttons.append((exit_rect, "Exit"))

                        # 顯示面板
                        screen.blit(select_panel, (20, 20))
                        pygame.display.flip()

                        selected_teammate = DisplaySystem.handle_click(buttons)
                        if selected_teammate == "Exit":
                            continue
                        if selected_teammate:
                            success = member.element_skill.use(
                                member, selected_teammate,
                                background=battle,
                                extra_draw=lambda: (screen.blit(cat_open, (450, 400)), screen.blit(boss1, (850, 300)))
                            )
                            if success:
                                # 創建成功訊息面板
                                DisplaySystem.clear_screen(battle)
                                success_panel = pygame.Surface((500, 100), pygame.SRCALPHA)
                                success_panel.fill((255, 255, 255, 200))
                                success_text = font.render(
                                    f"{member.name} successfully used {member.element_skill.name} on {selected_teammate.name}!",
                                    True, GREEN
                                )
                                text_rect = success_text.get_rect(center=(250, 50))
                                success_panel.blit(success_text, text_rect)
                                screen.blit(success_panel, (20, 20))
                                pygame.display.flip()
                                pygame.time.wait(1200)
                                break   
                        else:
                            # 創建錯誤訊息面板
                            error_panel = pygame.Surface((400, 100), pygame.SRCALPHA)
                            error_panel.fill((255, 255, 255, 200))
                            error_text = font.render("Invalid teammate selection.", True, RED)
                            text_rect = error_text.get_rect(center=(200, 50))
                            error_panel.blit(error_text, text_rect)
                            screen.blit(error_panel, (20, 20))
                            pygame.display.flip()
                            
                            # 等待玩家操作
                            waiting = True
                            while waiting:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                                        waiting = False
                        break
                    elif action == "5. Upgrade System":
                        DisplaySystem.upgrade_menu(self.team)
                        # 修正：升級系統後回到選單而不是直接 break
                        continue
                    elif action == "6. Equip/Unequip":
                        # 顯示裝備/卸下裝備選單
                        while True:
                            # 保持背景顯示
                            screen.blit(battle, (0, 0))
                            
                            # 計算面板大小
                            font = pygame.font.Font(None, 32)
                            equipment_items = [
                                (item_name, data['item'])
                                for item_name, data in self.team.backpack.items.items()
                                if isinstance(data['item'], Equipment)
                            ]

                            # 計算文字寬度
                            max_width = font.size("Equipment Management")[0]  # 標題寬度
                            for item_name, eq in equipment_items:
                                text = f"{item_name} (Lv.{eq.level})"
                                text_width = font.size(text)[0]
                                max_width = max(max_width, text_width)

                            # 計算面板尺寸
                            panel_width = max_width + 200  # 文字最大寬度 + 左右邊距 + 按鈕空間
                            panel_height = (len(equipment_items) + 2) * 40 + 100  # 裝備數量 * 行高 + 標題和按鈕空間
                            
                            # 創建主面板 (左上角)
                            panel_x = 20
                            panel_y = 20
                            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
                            panel_surface.fill((255, 255, 255, 200))
                            screen.blit(panel_surface, (panel_x, panel_y))

                            # 標題
                            title_text = font.render("Equipment Management", True, BLACK)
                            screen.blit(title_text, (panel_x + 20, panel_y + 20))

                            if not equipment_items:
                                no_items_text = font.render("No equipment in backpack.", True, RED)
                                screen.blit(no_items_text, (panel_x + 20, panel_y + 80))
                                pygame.display.flip()
                                pygame.time.wait(1200)
                                break

                            # 裝備列表
                            buttons_eq = []
                            for idx, (item_name, eq) in enumerate(equipment_items):
                                y = panel_y + 60 + idx * 40
                                
                                # 顯示裝備名稱和等級
                                text = f"{idx + 1}. {item_name} (Lv.{eq.level})"
                                text_surface = font.render(text, True, BLACK)
                                text_rect = text_surface.get_rect(topleft=(panel_x + 20, y))
                                screen.blit(text_surface, text_rect)
                                
                                # 根據裝備狀態顯示不同按鈕
                                if eq.is_equipped:
                                    # 已裝備，顯示卸下按鈕
                                    unequip_rect = pygame.Rect(panel_x + max_width + 40, y, 80, 30)
                                    pygame.draw.rect(screen, RED, unequip_rect, border_radius=5)
                                    unequip_text = font.render("Unequip", True, WHITE)
                                    text_rect = unequip_text.get_rect(center=unequip_rect.center)
                                    screen.blit(unequip_text, text_rect)
                                    buttons_eq.append((unequip_rect, ("unequip", eq)))
                                else:
                                    # 未裝備，顯示裝備按鈕
                                    equip_rect = pygame.Rect(panel_x + max_width + 40, y, 80, 30)
                                    pygame.draw.rect(screen, GREEN, equip_rect, border_radius=5)
                                    equip_text = font.render("Equip", True, WHITE)
                                    text_rect = equip_text.get_rect(center=equip_rect.center)
                                    screen.blit(equip_text, text_rect)
                                    buttons_eq.append((equip_rect, ("equip", eq)))

                            # 退出按鈕
                            exit_rect = pygame.Rect(panel_x + 20, panel_y + 60 + len(equipment_items) * 40 + 20, 150, 40)
                            pygame.draw.rect(screen, RED, exit_rect, border_radius=5)
                            exit_text = font.render("Exit", True, WHITE)
                            text_rect = exit_text.get_rect(center=exit_rect.center)
                            screen.blit(exit_text, text_rect)
                            buttons_eq.append((exit_rect, "Exit"))

                            pygame.display.flip()
                            
                            selected = DisplaySystem.handle_click(buttons_eq)
                            if selected == "Exit":
                                break
                            if selected:
                                action, eq = selected
                                if action == "unequip":
                                    # 直接卸下裝備
                                    for member in self.team.members:
                                        if member.equipment.get(eq.eq_type) == eq:
                                            eq.unequip(member)
                                            member.equipment[eq.eq_type] = None
                                            break
                                else:  # action == "equip"
                                    # 選擇要裝備到哪個角色
                                    DisplaySystem.clear_screen(background=battle)
                                    char_panel_width = max(font.size(m.name)[0] for m in self.team.members) + 100
                                    char_panel_height = len(self.team.members) * 40 + 100
                                    
                                    char_panel = pygame.Surface((char_panel_width, char_panel_height), pygame.SRCALPHA)
                                    char_panel.fill((255, 255, 255, 200))
                                    screen.blit(char_panel, (panel_x, panel_y))

                                    # 顯示角色列表
                                    buttons_char = []
                                    for idx, m in enumerate(self.team.members):
                                        text = f"{idx + 1}. {m.name}"
                                        text_surface = font.render(text, True, BLACK)
                                        text_rect = text_surface.get_rect(topleft=(panel_x + 20, panel_y + 20 + idx * 40))
                                        screen.blit(text_surface, text_rect)
                                        buttons_char.append((text_rect, m))

                                    # 返回按鈕
                                    back_rect = pygame.Rect(panel_x + 20, panel_y + 20 + len(self.team.members) * 40 + 20, 150, 40)
                                    pygame.draw.rect(screen, RED, back_rect, border_radius=5)
                                    back_text = font.render("Back", True, WHITE)
                                    text_rect = back_text.get_rect(center=back_rect.center)
                                    screen.blit(back_text, text_rect)
                                    buttons_char.append((back_rect, "Back"))

                                    pygame.display.flip()

                                    selected_char = DisplaySystem.handle_click(buttons_char)
                                    if selected_char == "Back":
                                        continue
                                    if selected_char:
                                        # 若該角色該部位已有裝備，先卸下
                                        old_eq = selected_char.equipment.get(eq.eq_type)
                                        if old_eq:
                                            old_eq.unequip(selected_char)
                                            selected_char.equipment[eq.eq_type] = None
                                        eq.equip(selected_char)
                                continue
                    elif action == "7. View Backpack":
                        DisplaySystem.show_backpack(self.team.backpack)
                        # 修正：背包後回到選單而不是直接 break
                        continue
                    elif action == "8. Skip Turn":
                        DisplaySystem.show_message(
                            f"{member.name} skipped their turn.",
                            background=battle,
                            extra_draw=None
                        )
                        pygame.time.wait(1200)  # 等待1.2秒以顯示訊息
                        break
                    else:
                        DisplaySystem.show_message(
                            "Invalid choice. Please select a valid option.",
                            background=battle,
                            extra_draw=None
                        )
                        pygame.time.wait(1200)  # 等待1.2秒以顯示訊息
                        # 修正：錯誤選項後回到選單
                        continue
                if self.monster.hp <= 0:
                    # 先清除畫面
                    DisplaySystem.clear_screen()
                    waiting = True
                    while waiting:
                        screen.blit(battle, (0, 0))
                        screen.blit(vectory, (0, 0))
                        # 計算白板尺寸
                        panel_width = 700
                        panel_height = 160
                        panel_x = 100
                        panel_y = 220

                        # 創建半透明白底
                        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
                        panel_surface.fill((255, 255, 255, 200))  # 200為透明度

                        # 畫白板
                        screen.blit(panel_surface, (panel_x, panel_y))

                        # 再畫文字
                        font = pygame.font.Font(None, 48)
                        text_surface = font.render("Victory! The monster has been defeated.", True, GREEN)
                        reward_surface = font.render("Rewards: 1000 EXP, 100 Coins", True, BLUE)
                        screen.blit(text_surface, (panel_x + 30, panel_y + 30))
                        screen.blit(reward_surface, (panel_x + 30, panel_y + 90))
                        pygame.display.flip()
                        pygame.time.wait(1200)
                        waiting = False
                        
                    exp_reward = 1000
                    coin_reward = 100
                    self.team.add_exp(exp_reward)
                    self.team.add_coin(coin_reward)
                    return

            # 怪物回合
            DisplaySystem.show_message(
                "Monster's turn!",
                background=battle,
                extra_draw=None
            )
            pygame.time.wait(1200)  # 等待1.2秒以顯示訊息
            # 修正：呼叫 show_attack_message 取代不存在的 show_monster_attack_message
            def show_monster_attack_message_with_bg(monster, target, damage, crit=False, element_boost=False, background_override=None, extra_draw_override=None):
                DisplaySystem.show_attack_message(
                    monster, target, damage, crit=crit, element_boost=element_boost,
                    background=battle,
                    extra_draw=None
                )
            # 將 act 內部的 show_monster_attack_message 替換為 show_monster_attack_message_with_bg
            original_show_attack_message = DisplaySystem.show_attack_message
            DisplaySystem.show_attack_message = show_monster_attack_message_with_bg
            self.monster.act(self.team)
            DisplaySystem.show_attack_message = original_show_attack_message

            if all(not m.is_alive() for m in self.team.members):
                waiting = True
                while waiting:
                    screen.blit(battle, (0, 0))
                    font = pygame.font.Font(None, 48)
                    text_surface = font.render("Game Over! The team has been defeated.", True, RED)
                    screen.blit(text_surface, (200, 100))
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                            waiting = False
                return