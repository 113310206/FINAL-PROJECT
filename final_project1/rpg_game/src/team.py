import pygame
image_s = pygame.image.load("store.jpg")
image_v = pygame.image.load("vectory.jpg")
image_team = pygame.image.load("team.jpg")
store = pygame.transform.scale(image_s, (1200, 700))
vectory = pygame.transform.scale(image_v, (1200, 700))
team_bg = pygame.transform.scale(image_team, (1200, 700))
BLUE = (0, 185, 220)

class Team:
    def __init__(self):
        from rpg_game.src.backpack import Backpack  # Dynamic import
        self.members = []
        self.coin = 1000
        self.exp = 0
        self.total_exp = 0
        self.exp_to_next_level = 500
        self.backpack = Backpack(self)  # Pass self as team parameter

    def add_coin(self, amount):
        from rpg_game.src.display import DisplaySystem  # Dynamic import
        self.coin += amount
        DisplaySystem.show_message(f"The team gained {amount} coins! Total coins: {self.coin}", background=vectory)
        pygame.time.wait(1200)  # Wait 1 second
        
    def spend_coin(self, amount):
        from rpg_game.src.display import DisplaySystem  # Dynamic import
        if self.coin >= amount:
            self.coin -= amount
            DisplaySystem.show_message(f"Spent {amount} coins. Remaining coins: {self.coin}",background=store, position=(350, 250), color=BLUE)
            pygame.time.wait(1200)
        else:
            DisplaySystem.show_message("Not enough coins.", background=store, position=(350, 250))
            pygame.time.wait(1200)

    def add_exp(self, amount):
        from rpg_game.src.display import DisplaySystem  # Dynamic import
        self.exp += amount
        self.total_exp += amount
        DisplaySystem.show_message(f"The team gained {amount} EXP! Total EXP: {self.exp}/{self.exp_to_next_level}", background=vectory, position=(350, 250))
        pygame.time.wait(1200)  # Wait 1 second
        if self.exp >= self.exp_to_next_level:
            self.level_up_team()

    def level_up_team(self):
        from rpg_game.src.display import DisplaySystem  # Dynamic import
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        DisplaySystem.show_message("The team has leveled up! Distributing level-ups to all members.",background=vectory, position=(450, 250))
        pygame.time.wait(1200)  # Wait 1 second
        for member in self.members:
            member.level_up()

    def recruit(self, character):
        from rpg_game.src.display import DisplaySystem  # Dynamic import
        if len(self.members) < 4:
            self.members.append(character)
            DisplaySystem.show_message(f"{character.name} joined the team!", background=team_bg)
            pygame.time.wait(1200)  # Wait 1 second
        else:
            DisplaySystem.show_message("Team is full, cannot recruit.", background=team_bg)
            pygame.time.wait(1200)

    def fire(self, name):
        from rpg_game.src.display import DisplaySystem  # Dynamic import
        for m in self.members:
            if m.name == name:
                self.members.remove(m)
                DisplaySystem.show_message(f"{name} has been removed from the team.", background=team_bg)
                pygame.time.wait(1200)
                return
        DisplaySystem.show_message("Character not found.", background=team_bg)

    def change_position(self, name, pos):
        from rpg_game.src.display import DisplaySystem  # Dynamic import
        for m in self.members:
            if m.name == name:
                if pos not in ("front", "mid", "back"):
                    DisplaySystem.show_message("Position must be front/mid/back", background=team_bg)
                    pygame.time.wait(1200)
                    return
                m.position = pos
                DisplaySystem.show_message(f"{name}'s position changed to {pos}.", background=team_bg)
                pygame.time.wait(1200)
                return
        DisplaySystem.show_message("Character not found.", background=team_bg)

    def show_positions(self):
        from rpg_game.src.display import DisplaySystem  # Dynamic import
        positions = "\n".join([f"{member.name}: {member.position}" for member in self.members])
        DisplaySystem.show_message(f"=== Positions ===\n{positions}\n=================", background=team_bg)
        pygame.time.wait(1200)

    def add_member(self, character):
        from rpg_game.src.display import DisplaySystem
        # Check if character is already in team
        if character in self.members:
            DisplaySystem.show_message(f"{character.name} is already in the team.", background=team_bg)
            pygame.time.wait(1200)
            return
        if len(self.members) < 4:
            self.members.append(character)
            DisplaySystem.show_message(f"{character.name} joined the team!", background=team_bg)
            pygame.time.wait(1200)
        else:
            DisplaySystem.show_message("Team is full, cannot add more members.", background=team_bg)
            pygame.time.wait(1200)

    def print_positions(self):
        self.show_positions()

    def add_character(self, character):
        """Add character to team and set team attribute"""
        self.members.append(character)
        character.team = self  # Set character's team attribute
        from rpg_game.src.display import DisplaySystem  # Dynamic import
        DisplaySystem.show_message(f"{character.name} has joined the team!", background=team_bg)
        pygame.time.wait(1200)

