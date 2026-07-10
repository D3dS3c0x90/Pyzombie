# src/ui/player_state.py
import pygame
import src.assets_manager as assets
from src.settings import PIXEL_FONT, SCREEN_WIDTH, ITEMS_KEYS


class PlayerState:
    def __init__(self, screen, blank_axis, health_axis, player):
        self.blank_x, self.blank_y = blank_axis
        self.health_x, self.health_y = health_axis
        
        self.screen = screen
        self.player = player
        
        self.empty_index = 0
        self.key_release = False
        
        self.font = pygame.font.Font(PIXEL_FONT, 22)
        
        self.collisions = {f"{i + 1}": pygame.Rect(
            0, 0,
            assets.sprites["item_background"].get_width() - 10,
            assets.sprites["item_background"].get_width() - 10,
                           ) for i in range(9)}
        self.collisions["0"] = pygame.Rect(
            0, 0,
            assets.sprites["item_background"].get_width() - 10,
            assets.sprites["item_background"].get_width() - 10)
        
        self.items = {f"{i}": None for i in range(10)}
        
        self.selected_char = None
        self.recent_char = None
        self.hotbar_item_pressed = False
        self.last_dragged_item_key = None
        self.dragged_item = {"char": None, "item": None}
        
        self.chars_x = {
            "1": 0,
            "2": 70,
            "3": 136,
            "4": 204,
            "5": 271,
            "6": 337,
            "7": 405,
            "8": 472,
            "9": 539,
            "0": 606,
        }
        
        self.updare_rect()
        
    def updare_rect(self):
        for key, value in self.chars_x.items():
            self.collisions[key].x = self.blank_x + 460 + value
            self.collisions[key].y = self.blank_y + 46
            
    def add_item(self, char, item):
        self.items[char] = item
        
    def drag_item(self, mouse_pos):
        if not self.hotbar_item_pressed:
            for key, rect in self.collisions.items():
                if rect.collidepoint(mouse_pos):
                    if self.items[key]:
                        self.dragged_item["char"] = key
                        self.dragged_item["item"] = self.items[key]
                        self.hotbar_item_pressed = True
                        self.last_dragged_item_key = key
                        break
        else:
            for key, rect in self.collisions.items():
                if rect.collidepoint(mouse_pos):
                    for item_key, _ in self.items.items():
                        if item_key == key:
                            self.items[item_key] = self.dragged_item["item"]
                            self.items[self.last_dragged_item_key] = None
                            self.last_dragged_item_key = None
                            # self.items[item_key] = self.dragged_item["char"]
                            break
                    self.dragged_item["char"] = None
                    self.dragged_item["item"] = None
                    self.hotbar_item_pressed = False
                    break
                         
    def collision_event_detection(self, event, is_inventory_open):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for key, rect in self.collisions.items():
                if rect.collidepoint(mx, my) and is_inventory_open:
                    self.selected_char = key
            
    def draw_amount(self, amount, f=2):
        if amount > 999:
            return f"{amount / 1000:.{f}f}k"
        elif amount > 999999:
            return f"{amount / 1000000:.{f}f}M"
        return str(amount)
    
    def draw_numbers(self, number, x, y):
        char_surface = assets.sprites[f"char_{str(number)[0]}"]
        self.screen.blit(char_surface, (x , y))
        
    def draw_selected_item(self, char):
        key, value = (char, self.chars_x[str(char)])
        self.screen.blit(assets.sprites[f"char_10"], (self.blank_x + 469 + value, self.blank_y + 15))
        self.screen.blit(assets.sprites[f"char_11"], (self.blank_x + 489 + value, self.blank_y + 15))
        
        self.draw_numbers(key, self.blank_x + 479 + value, self.blank_y + 15)
        self.screen.blit(assets.sprites["item_background"], (self.blank_x + 455 + value, self.blank_y + 40))
        
        self.selected_char = char
        
        if self.dragged_item["char"]:
            self.screen.blit(assets.sprites["pointer_background"], (self.blank_x + 455 + value, self.blank_y + 40))

    def draw(self):
        self.screen.blit(assets.sprites["player_state"], (self.blank_x, self.blank_y + 8))
        
        for index in range(self.player.health_limit + (self.player.health - self.player.health_limit)):
            self.player.draw_health_bar(self.screen, self.health_x + index * 2, self.health_y)
            self.empty_index = index
        for i in range(self.empty_index, self.player.health_limit):
            self.screen.blit(assets.sprites["player_empty_health_banner"], (self.health_x + i * 2, self.health_y))
        self.screen.blit(assets.sprites["player_health_banner"], (self.health_x, self.health_y))

        weapon_ammo, total_ammo = (self.player.ammo_count, self.player.weapon_ammo_count)

        weapon_ammo_surface = self.font.render(str(weapon_ammo), False, "#ffffff")
        total_ammo_surface = self.font.render(str(self.draw_amount(total_ammo, f=1)), False, "#ffffff")
        coins_surface = self.font.render(str(self.draw_amount(self.player.coins)), False, "#86926e")

        ammo_x, ammo_y = self.blank_x + SCREEN_WIDTH - 215, self.blank_y + 165
        total_ammo_x, total_ammo_y = self.blank_x + SCREEN_WIDTH - 170, self.blank_y + 164
        coins_x, coins_y = self.blank_x + SCREEN_WIDTH - 90, self.blank_y + 158

        self.screen.blit(weapon_ammo_surface, (ammo_x, ammo_y))
        self.screen.blit(total_ammo_surface, (total_ammo_x, total_ammo_y))
        self.screen.blit(coins_surface, (coins_x, coins_y))            
   
        for key, value in ITEMS_KEYS.items():
            if value:
                self.selected_char = key
                break
        if self.selected_char:
            if self.recent_char == self.selected_char:
                if self.key_release and self.items[self.selected_char]:
                    self.items[self.selected_char].use()
            else:
                self.recent_char = self.selected_char
            self.key_release = False
            self.draw_selected_item(self.selected_char)
        
        for key, value in self.items.items():
            if value:
                if value.quantity > 0:
                    image = value.image
                    image = pygame.transform.scale(image, (self.collisions[key].width - 5, self.collisions[key].height - 5))
                    if self.dragged_item["char"] != key:
                        self.screen.blit(image, (self.blank_x + 460 + self.chars_x[key], self.blank_y + 50))
                    item_font = pygame.font.Font(PIXEL_FONT, 18)
                    self.screen.blit(item_font.render(str(value.quantity), False, "#ffffff"), (self.collisions[key].x, self.collisions[key].y))
                else:
                    value.kill()
                    self.selected_char = None
        
        # for _, value in self.collisions.items():
        #     pygame.draw.rect(self.screen, (255, 0, 0), value, 1)
            