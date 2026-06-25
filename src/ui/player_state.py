# src/ui/player_state.py
import pygame
import src.assets_manager as assets
import src.settings as settings


class PlayerState:
    def __init__(self, screen, blank_axis, health_axis, player):
        self.screen = screen
        self.blank_x, self.blank_y = blank_axis
        self.health_x, self.health_y = health_axis
        self.player = player
        self.font = pygame.font.Font(settings.PIXEL_FONT, 24)

    def draw(self):
        self.screen.blit(assets.sprites["player_state"], (self.blank_x, self.blank_y))
        self.player.draw_health_bar(self.screen, self.health_x, self.health_y)

        weapon_ammo, stack_size, total_ammo, coins = (
            self.player.ammo_count, self.player.ammo_stack,
            self.player.weapon_ammo_count, self.player.coins
        )

        weapon_ammo_surface = self.font.render(str(weapon_ammo), False, "#58534a")
        stack_ammo_surface = self.font.render(str(stack_size), False, "#58534a")
        total_ammo_surface = self.font.render(str(total_ammo), False, "#58534a")
        coins_surface = self.font.render(str(coins), False, "#58534a")

        ammo_x, ammo_y = self.blank_x + settings.SCREEN_WIDTH - 180, self.blank_y + 75
        stack_x, stack_y = self.blank_x + settings.SCREEN_WIDTH - 120, self.blank_y + 75
        total_ammo_x, total_ammo_y = self.blank_x + settings.SCREEN_WIDTH - 60, self.blank_y + 75
        coins_x, coins_y = self.blank_x + 190, self.blank_y + 63

        self.screen.blit(weapon_ammo_surface, (ammo_x, ammo_y))
        self.screen.blit(stack_ammo_surface, (stack_x, stack_y))
        self.screen.blit(total_ammo_surface, (total_ammo_x, total_ammo_y))
        self.screen.blit(coins_surface, (coins_x, coins_y))
