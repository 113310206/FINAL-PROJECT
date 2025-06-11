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
image_v = pygame.image.load("C:/CODing/PYTHON/final_project1/vectory.jpg")
imafe_b = pygame.image.load("C:/CODing/PYTHON/final_project1/battle.jpg")
image_c1 = pygame.image.load("C:/CODing/PYTHON/final_project1/cat1.jpg")
image_boss = pygame.image.load("C:/CODing/PYTHON/final_project1/boss.jpg")
vectory = pygame.transform.scale(image_v, (1200, 700))
battle = pygame.transform.scale(imafe_b, (1200, 700))
cat1 = pygame.transform.scale(image_c1, (200, 200))  # 縮小貓咪圖片
boss = pygame.transform.scale(image_boss, (200, 200))  # 縮小boss圖片


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
            # 貓咪與boss往左上移一點
            cat_x, cat_y = 450, 400
            boss_x, boss_y = cat_x + 400, cat_y - 100
            screen.blit(cat1, (cat_x, cat_y))
            screen.blit(boss, (boss_x, boss_y))
            pygame.display.flip()
            DisplaySystem.show_battle_status(
                self.team,
                self.monster,
                background_override=battle,
                extra_draw=lambda: (screen.blit(cat1, (cat_x, cat_y)), screen.blit(boss, (boss_x, boss_y)))
            )

            for idx, member in enumerate(self.team.members):
                if not member.is_alive():
                    continue

                while True:
                    screen.blit(battle, (0, 0))
                    screen.blit(cat1, (cat_x, cat_y))
                    screen.blit(boss, (boss_x, boss_y))
                    pygame.display.flip()
                    DisplaySystem.show_battle_status(
                        self.team,
                        self.monster,
                        background_override=battle,
                        extra_draw=lambda: (screen.blit(cat1, (cat_x, cat_y)), screen.blit(boss, (boss_x, boss_y)))
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
                        text_rect = text_surface.get_rect(topleft=(50, 300 + i * 30))  # 從上到下排列，間距 30
                        screen.blit(text_surface, text_rect)
                        buttons.append((text_rect, option))
                    pygame.display.flip()

                    action = DisplaySystem.handle_click(buttons)
                    if action == "1. Normal Attack":
                        crit = member.try_crit(self.monster)
                        total_damage = member.attack_power * (2 if member.element_boost else 1) * (2 if crit else 1)
                        member.element_boost = False  # 攻击后重置加成
                        DisplaySystem.show_attack_message(member, self.monster, total_damage, crit=crit)
                        self.monster.hp -= total_damage
                        break
                    elif action == "2. Use Skill":
                        if member.skill:
                            crit = member.try_crit(self.monster)
                            total_damage = member.skill.damage * (2 if crit else 1)
                            DisplaySystem.show_skill_use(member, member.skill, self.monster, total_damage, crit=crit)
                            self.monster.hp -= total_damage
                        break
                    elif action == "3. Use Element Skill":
                        if member.element_skill:
                            success = member.element_skill.use(member, self.monster)
                            if success:
                                # 不需再手動覆蓋元素，已由技能內部處理
                                DisplaySystem.show_message(f"{member.name} successfully used {member.element_skill.name}!")
                        break
                    elif action == "4. Use Element Skill on Teammate":
                        teammates = [m for m in self.team.members if m.is_alive() and m != member]
                        if not teammates:
                            DisplaySystem.show_message("No teammates available for support.", color=RED)
                            continue

                        DisplaySystem.show_message("Select a teammate to use the skill on.")
                        buttons = []
                        for i, teammate in enumerate(teammates):
                            text_surface = font.render(f"{i + 1}. {teammate.name}", True, BLACK)
                            text_rect = text_surface.get_rect(topleft=(50, 50 + i * 50))
                            screen.blit(text_surface, text_rect)
                            buttons.append((text_rect, teammate))
                        pygame.display.flip()

                        selected_teammate = DisplaySystem.handle_click(buttons)
                        if selected_teammate:
                            success = member.element_skill.use(member, selected_teammate)
                            if success:
                                # 不需再手動覆蓋元素，已由技能內部處理
                                DisplaySystem.show_message(f"{member.name} successfully used {member.element_skill.name} on {selected_teammate.name}!")
                        else:
                            DisplaySystem.show_message("Invalid teammate selection.", color=RED)
                        break
                    elif action == "5. Upgrade System":
                        DisplaySystem.upgrade_menu(self.team)
                        continue
                    elif action == "6. Equip/Unequip":
                        font = pygame.font.Font(None, 36)
                        options = [
                            "1. Equip",
                            "2. Unequip"
                        ]
                        DisplaySystem.clear_screen()
                        buttons = []
                        for i, option in enumerate(options):
                            text_surface = font.render(option, True, BLACK)
                            text_rect = text_surface.get_rect(topleft=(50, 50 + i * 50))
                            screen.blit(text_surface, text_rect)
                            buttons.append((text_rect, option))
                        pygame.display.flip()

                        sub_action = DisplaySystem.handle_click(buttons)
                        if sub_action == "1. Equip":
                            DisplaySystem.clear_screen()
                            if not self.team.backpack.items:
                                DisplaySystem.show_message("Your backpack is empty. Please add items to equip.", color=RED)
                                # 只要點擊任意地方就退出
                                waiting = True
                                while waiting:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()
                                        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                                            waiting = False
                                break  # 直接退出 equip 流程
                            DisplaySystem.show_backpack(self.team.backpack, pause=False)
                            buttons = []
                            for idx, (item_name, data) in enumerate(self.team.backpack.items.items()):
                                item = data['item']
                                text_surface = font.render(f"{idx + 1}. {item_name} (Lv.{item.level})", True, BLACK)
                                text_rect = text_surface.get_rect(topleft=(50, 50 + idx * 50))
                                screen.blit(text_surface, text_rect)
                                buttons.append((text_rect, item))
                            pygame.display.flip()

                            selected_item = DisplaySystem.handle_click(buttons)
                            if selected_item and isinstance(selected_item, Equipment):
                                member.equip(selected_item, self.team.backpack)  # 傳入 team.backpack
                            else:
                                DisplaySystem.show_message("Invalid selection. Please choose a valid equipment.", color=RED)

                        elif sub_action == "2. Unequip":
                            DisplaySystem.clear_screen()
                            # 修正：如果沒有任何裝備，直接顯示訊息並等待點擊退出
                            if all(eq is None for eq in member.equipment.values()):
                                DisplaySystem.show_message("No equipment to unequip.", color=RED)
                                waiting = True
                                while waiting:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()
                                        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                                            waiting = False
                                break  # 直接退出 unequip 流程
                            buttons = []
                            for eq_type, eq in member.equipment.items():
                                if eq:
                                    text_surface = font.render(f"{eq_type.capitalize()}: {eq.name} (Lv.{eq.level})", True, BLACK)
                                    text_rect = text_surface.get_rect(topleft=(50, 50 + len(buttons) * 50))
                                    screen.blit(text_surface, text_rect)
                                    buttons.append((text_rect, eq_type))
                            pygame.display.flip()

                            selected_eq_type = DisplaySystem.handle_click(buttons)
                            if selected_eq_type and member.equipment.get(selected_eq_type):
                                member.unequip(selected_eq_type, self.team.backpack)  # 傳入 team.backpack
                                DisplaySystem.show_message(f"{member.name} unequipped {selected_eq_type.capitalize()}!", color=GREEN)
                            else:
                                DisplaySystem.show_message("Invalid selection. No equipment to unequip.", color=RED)

                        else:
                            DisplaySystem.show_message("Invalid choice. Please select 1 or 2.", color=RED)
                        continue  # 不消耗回合，保持角色動作
                    elif action == "7. View Backpack":
                        DisplaySystem.backpack_menu(self.team.backpack)  # 傳入 team.backpack 而非 team
                        continue
                    elif action == "8. Skip Turn":
                        DisplaySystem.show_message(f"{member.name} skipped their turn.")
                        break
                    else:
                        DisplaySystem.show_message("Invalid choice. Please select a valid option.")

                if self.monster.hp <= 0:
                    # 先清除畫面
                    DisplaySystem.clear_screen()
                    # 持續顯示勝利畫面直到玩家操作
                    waiting = True
                    while waiting:
                        screen.blit(vectory, (0, 0))
                        pygame.display.flip()
                        # 可選：顯示獎勵訊息
                        font = pygame.font.Font(None, 48)

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                                waiting = False
                    exp_reward = 1000
                    coin_reward = 100
                    text_surface = font.render("Victory! The monster has been defeated.", True, GREEN)
                    screen.blit(text_surface, (100, 100))
                    reward_surface = font.render("Rewards: 1000 EXP, 100 Coins", True, BLUE)
                    screen.blit(reward_surface, (100, 180))
                    pygame.display.flip()
                    self.team.add_exp(exp_reward)
                    self.team.add_coin(coin_reward)
                    return

            # 怪物回合
            DisplaySystem.show_message("Monster's turn!")
            self.monster.act(self.team)

            if all(not m.is_alive() for m in self.team.members):
                DisplaySystem.show_message("Game Over! The team has been defeated.")
                return

