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
        self.name = f"怪物 (Round {round_number})"
        self.job = type("Job", (), {"job_name": "怪物"})()  # 讓 monster 有 job 屬性且 job_name 為"怪物"

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
                    text_surface = font.render(f"{member.name}'s Turn (HP: {member.hp}/{member.max_hp}, MP: {member.mp}/{member.max_mp})", True, BLACK)
                    text_rect = text_surface.get_rect(topleft=(50, 270))
                    screen.blit(text_surface, text_rect)
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
                    buttons = []
                    for i, option in enumerate(options):
                        text_surface = font.render(option, True, BLACK)
                        text_rect = text_surface.get_rect(topleft=(50, 300 + i * 30))
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
                            success = member.element_skill.use(
                                member, self.monster,
                                background=battle,
                                extra_draw=lambda: (screen.blit(cat_open, (450, 400)), screen.blit(boss1, (850, 300)))
                            )
                            pygame.time.wait(1200)  # 等待技能動畫結束
                            # 使用元素技能後自動切畫面，不再等待玩家操作
                        break
                    elif action == "4. Use Element Skill on Teammate":
                        teammates = [m for m in self.team.members if m.is_alive() and m != member]
                        if not teammates:
                            DisplaySystem.show_message(
                                "No teammates available for support.", color=RED,
                                background=battle,
                                extra_draw=lambda: (screen.blit(cat_open, (450, 400)), screen.blit(boss1, (850, 300)))
                            )
                            pygame.time.wait(1200)  # 等待1.2秒以顯示訊息
                            # 等待玩家操作，避免訊息被蓋掉
                            waiting = True
                            while waiting:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                                        waiting = False
                            continue

                        DisplaySystem.show_message(
                            "Select a teammate to use the skill on.",
                            background=battle,
                            extra_draw=lambda: (screen.blit(cat_open, (450, 400)), screen.blit(boss1, (850, 300)))
                        )
                        buttons = []
                        for i, teammate in enumerate(teammates):
                            text_surface = font.render(f"{i + 1}. {teammate.name}", True, BLACK)
                            text_rect = text_surface.get_rect(topleft=(50, 50 + i * 50))
                            screen.blit(text_surface, text_rect)
                            buttons.append((text_rect, teammate))
                        pygame.display.flip()

                        selected_teammate = DisplaySystem.handle_click(buttons)
                        if selected_teammate:
                            success = member.element_skill.use(
                                member, selected_teammate,
                                background=battle,
                                extra_draw=lambda: (screen.blit(cat_open, (450, 400)), screen.blit(boss1, (850, 300)))
                            )
                            if success:
                                DisplaySystem.show_message(
                                    f"{member.name} successfully used {member.element_skill.name} on {selected_teammate.name}!",
                                    background=battle,
                                    extra_draw=lambda: (screen.blit(cat_open, (450, 400)), screen.blit(boss1, (850, 300)))
                                )
                                # 等待玩家操作，避免訊息被蓋掉
                                waiting = True
                                while waiting:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()
                                        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                                            waiting = False
                        else:
                            DisplaySystem.show_message(
                                "Invalid teammate selection.", color=RED,
                                background=battle,
                                extra_draw=lambda: (screen.blit(cat_open, (450, 400)), screen.blit(boss1, (850, 300)))
                            )
                            # 等待玩家操作，避免訊息被蓋掉
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
                            DisplaySystem.show_message("Select equipment to equip/unequip.", background=battle)
                            from rpg_game.src.equipment import Equipment
                            equipment_items = [
                                (item_name, data['item'])
                                for item_name, data in self.team.backpack.items.items()
                                if isinstance(data['item'], Equipment)
                            ]
                            if not equipment_items:
                                DisplaySystem.show_message("No equipment in backpack.", color=RED, background=battle)
                                pygame.time.wait(1200)
                                break
                            font = pygame.font.Font(None, 24)
                            buttons_eq = []
                            for idx, (item_name, eq) in enumerate(equipment_items):
                                eq_status = "Equipped" if eq.is_equipped else "Unequipped"
                                text_surface = font.render(f"{idx + 1}. {item_name} (Lv.{eq.level}) [{eq_status}]", True, BLACK)
                                text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 40))
                                screen.blit(text_surface, text_rect)
                                buttons_eq.append((text_rect, eq))
                            # 新增「全部卸下」按鈕
                            unequip_all_rect = pygame.Rect(50, 60 + len(buttons_eq) * 40, 200, 40)
                            unequip_all_text = font.render("Unequip All", True, BLUE)
                            screen.blit(unequip_all_text, unequip_all_rect.topleft)
                            buttons_eq.append((unequip_all_rect, "Unequip All"))
                            # 退出按鈕
                            exit_rect = pygame.Rect(50, 100 + len(buttons_eq) * 40, 200, 40)
                            exit_text = font.render("Exit", True, RED)
                            screen.blit(exit_text, exit_rect.topleft)
                            buttons_eq.append((exit_rect, "Exit"))
                            pygame.display.flip()
                            selected_eq = DisplaySystem.handle_click(buttons_eq)
                            if selected_eq == "Exit":
                                break
                            if selected_eq == "Unequip All":
                                # 選擇角色後全部卸下
                                DisplaySystem.show_message("Select a character to unequip all.", background=battle)
                                buttons_char = []
                                for idx, m in enumerate(self.team.members):
                                    text_surface = font.render(f"{idx + 1}. {m.name}", True, BLACK)
                                    text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 40))
                                    screen.blit(text_surface, text_rect)
                                    buttons_char.append((text_rect, m))
                                exit_rect2 = pygame.Rect(50, 50 + len(buttons_char) * 40, 200, 40)
                                exit_text2 = font.render("Exit", True, RED)
                                screen.blit(exit_text2, exit_rect2.topleft)
                                buttons_char.append((exit_rect2, "Exit"))
                                pygame.display.flip()
                                selected_char = DisplaySystem.handle_click(buttons_char)
                                if selected_char == "Exit":
                                    continue
                                if selected_char:
                                    for eq_type, eq in selected_char.equipment.items():
                                        if eq:
                                            eq.unequip(selected_char)
                                            selected_char.equipment[eq_type] = None
                                continue
                            if selected_eq:
                                # 選擇要裝備到哪個角色
                                DisplaySystem.show_message("Select a character to equip/unequip.", background=battle)
                                buttons_char = []
                                for idx, m in enumerate(self.team.members):
                                    text_surface = font.render(f"{idx + 1}. {m.name}", True, BLACK)
                                    text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 40))
                                    screen.blit(text_surface, text_rect)
                                    buttons_char.append((text_rect, m))
                                exit_rect2 = pygame.Rect(50, 50 + len(buttons_char) * 40, 200, 40)
                                exit_text2 = font.render("Exit", True, RED)
                                screen.blit(exit_text2, exit_rect2.topleft)
                                buttons_char.append((exit_rect2, "Exit"))
                                pygame.display.flip()
                                selected_char = DisplaySystem.handle_click(buttons_char)
                                if selected_char == "Exit":
                                    continue
                                if selected_char:
                                    # 若已裝備則卸下，否則裝備
                                    if selected_eq.is_equipped and selected_char.equipment.get(selected_eq.eq_type) == selected_eq:
                                        selected_eq.unequip(selected_char)
                                        selected_char.equipment[selected_eq.eq_type] = None
                                    else:
                                        # 若該角色該部位已有裝備，先卸下
                                        old_eq = selected_char.equipment.get(selected_eq.eq_type)
                                        if old_eq:
                                            old_eq.unequip(selected_char)
                                            selected_char.equipment[selected_eq.eq_type] = None
                                        selected_eq.equip(selected_char)
                        continue
                    elif action == "7. View Backpack":
                        DisplaySystem.backpack_menu(self.team.backpack)
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
                        # 不再顯示 cat1, boss
                        font = pygame.font.Font(None, 48)
                        text_surface = font.render("Victory! The monster has been defeated.", True, GREEN)
                        screen.blit(text_surface, (100, 100))
                        reward_surface = font.render("Rewards: 1000 EXP, 100 Coins", True, BLUE)
                        screen.blit(reward_surface, (100, 180))
                        pygame.display.flip()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
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
                    screen.blit(text_surface, (100, 100))
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                            waiting = False
                return

