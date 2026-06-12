import pygame
import src.assets_manager as assets
import src.settings as settings


class PlayerState:
    def __init__(self, screen, blank_axis, health_axis, player):
        self.screen = screen
        
        self.blank_x = blank_axis[0] 
        self.blank_y = blank_axis[1] 
        
        self.health_x = health_axis[0]
        self.health_y = health_axis[1]
        
        self.player = player
        
        self.font = pygame.font.Font(settings.PIXEL_FONT, 24)
        
    def draw(self):
        # 1. Draw the background HUD bar state
        self.screen.blit(assets.sprites["player_state"], (self.blank_x, self.blank_y))
        
        # 2. Draw the player health bar
        self.player.draw_health_bar(self.screen, self.health_x, self.health_y)
        
        # 3. Fetch ammo values
        weapon_ammo, stack_size, total_ammo, coins = self.player.ammo_count, self.player.ammo_stack, self.player.weapon_ammo_count, self.player.coins
        
        # ✅ FIX 2: Set anti-aliasing to False so your Minecraft pixel font stays perfectly sharp and crisp!
        weapon_ammo_surface = self.font.render(str(weapon_ammo), False, "#58534a")
        stack_ammo_surface = self.font.render(str(stack_size), False, "#58534a")
        total_ammo_surface = self.font.render(str(total_ammo), False, "#58534a")
        coins_surface = self.font.render(str(coins), False, "#58534a")
        
        # ✅ FIX 3: Blit the text surface directly onto the main screen.
        # Use relative coordinates based on your HUD position (e.g., self.blank_x + offset)
        # Change (100, 10) to whatever pixel offset fits perfectly over your HUD ammo box slot!
        ammo_x = self.blank_x + settings.SCREEN_WIDTH - 180 
        ammo_y = self.blank_y + 75
        
        stack_x = self.blank_x + settings.SCREEN_WIDTH - 120 
        stack_y = self.blank_y + 75
        
        total_ammo_x = self.blank_x + settings.SCREEN_WIDTH - 60 
        total_ammo_y = self.blank_y + 75
        
        coins_x = self.blank_x + 190
        coins_y = self.blank_y + 63
        
        self.screen.blit(weapon_ammo_surface, (ammo_x, ammo_y))
        self.screen.blit(stack_ammo_surface, (stack_x, stack_y))
        self.screen.blit(total_ammo_surface, (total_ammo_x, total_ammo_y))
        self.screen.blit(coins_surface, (coins_x, coins_y))

        