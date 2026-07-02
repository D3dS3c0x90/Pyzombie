# inventory.py
from src.settings import PIXEL_FONT
import pygame


class Inventory:
    def __init__(self, x, y, width, height, image, items=None):
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height
        
        self.slot_size = 64

        self.padding_x = 20
        self.padding_y = 20
        
        self.count_x = 0
        self.count_y = 0
        
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.items = [] if items is None else items
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        for item in self.items:
            item_x = item.x + (self.count_x * (self.padding_x + item.rect.width))
            item_y = item.y + (self.count_y * (self.padding_y + item.rect.height))
            screen.blit(item.image, (item_x, item_y))
            item.update_rect(item_x, item_y)
            
            if self.count_x < 5:
                self.count_x += 1
            else:
                self.count_x = 0
                self.count_y += 1
            # pygame.draw.rect(screen, (255,255,255), (item_x, item_y, item.rect.width, item.rect.height), 2)
        self.count_x, self.count_y = 0, 0
        
    def drop_down_list(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # Right Click
            for item in self.items:
                if item.rect.collidepoint(event.pos):
                    print(item.name)
                    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left Click
            pass
            # if self.context_menu:
            #     # Check if user clicked "Use" or "Drop" inside the context menu rect
            #     # ... logic to trigger item.use() or item.kill() ...
            #     self.context_menu = None # Close menu after action

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, details=None, catigory="", *groups):
        super().__init__(*groups)
        
        self.x = x
        self.y = y
        
        self.width = 64
        self.height = 64
        
        self.name = details["name"]
        self.catigory = catigory
        
        self.quantity = 1
        self.amount = details["amount"]
        
        self.font = pygame.font.Font(PIXEL_FONT, 24)
        
        self.image = pygame.transform.scale(details["image"], (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
    def update_rect(self, x, y):
        self.rect.x = x
        self.rect.y = y
                
    def inc(self, amount=1):
        self.quantity += amount
        
    def dic(self, amount=1):
        if self.quantity >= 1:
            self.quantity -= amount
        else:
            self.kill()
        
    def write_details(self):
        return f"{self.name} ({self.quantity})"
    
# class Health(Item):
#     def __init__(self, x, y, width=64, height=64):
#         super().__init__(x, y, width, height)
        
# class Ammo(Item):
#     def __init__(self, x, y, width=64, height=64):
#         super().__init__(x, y, width, height)
        
# class RifleAmmo(Ammo):
#     def __init__(self, x, y, width=64, height=64):
#         super().__init__(x, y, width, height)
        
# class SemiAmmo(Ammo):
#     def __init__(self, x, y, width=64, height=64):
#         super().__init__(x, y, width, height)