# inventory.py
from src.settings import PIXEL_FONT, GLOBAL_NOTIFICATIONS
from src.ui import notification
import pygame


class Inventory:
    def __init__(self, x, y, width, height, image, screen, items=None):
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height
        
        self.slot_size = 64

        self.padding_x = 20
        self.padding_y = 20
        
        self.screen = screen
        
        self.active_list = False
        
        self.list_x = 0
        self.list_y = 0
        
        self.count_x = 0
        self.count_y = 0
        
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.items = [] if items is None else items
        
        self.selected_item = None
        
        self.taps = [
            pygame.Rect(x, y + 110, 150, 50),
            pygame.Rect(x, y + 190, 150, 50),
            pygame.Rect(x, y + 270, 150, 50),
        ]

        
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

        for item in self.items:
            item_x = item.x + (self.count_x * (self.padding_x + item.rect.width))
            item_y = item.y + (self.count_y * (self.padding_y + item.rect.height))
            
            self.screen.blit(item.image, (item_x, item_y))
            
            item.update_rect(item_x, item_y)
            
            if self.count_x < 5:
                self.count_x += 1
            else:
                self.count_x = 0
                self.count_y += 1
            # pygame.draw.rect(self.screen, (255,255,255), (item_x, item_y, item.rect.width, item.rect.height), 2)
        self.count_x, self.count_y = 0, 0
        
    def drop_down_list(self, event, hover_list):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # Right Click
            for item in self.items:
                if item.rect.collidepoint(event.pos):
                    self.list_x = item.rect.x
                    self.list_y = item.rect.y + item.rect.height
                    self.active_list = True
                    self.selected_item = item
                    

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if 1 in hover_list:
                index = hover_list.index(1)
                
                # Map indices to methods directly
                if self.selected_item:
                    actions = {
                        1: self.selected_item.use,
                        2: lambda: self.selected_item.use(self.selected_item.quantity),
                        3: self.selected_item.fix_position,
                        4: self.selected_item.drop
                    }
                    
                    # Execute the chosen action
                    if index in actions:
                        actions[index]()
                        if self.selected_item.quantity <= 0:
                            self.selected_item = None
                            self.active_list = False
                    
            else:
                self.active_list = False
                self.selected_item = None

class ListComponent:
    def __init__(self, image):
        self.x = 0
        self.y = 0
        self.clean_image = image.copy()
        self.image = image.copy()
        self.rect = self.image.get_rect(topleft=(0, 0))
        
    def reset(self):
        self.image = self.clean_image.copy()
                
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, details=None, category="", player=None, *groups):
        super().__init__(*groups)
        
        self.x = x
        self.y = y
        
        self.width = 64
        self.height = 64
        
        self.name = details["name"]
        self.category = category
        
        self.quantity = 1
        self.amount = details["amount"]
        
        self.player = player
        
        self.font = pygame.font.Font(PIXEL_FONT, 25)
        self.shadow_font = pygame.font.Font(PIXEL_FONT, 26)
        
        self.quantity_font = pygame.font.Font(PIXEL_FONT, 20)
        self.quantity_shadow_font = pygame.font.Font(PIXEL_FONT, 21)
        
        self.text_surface = self.font.render(self.name, False, "#604e00")
        self.shadow_surface = self.shadow_font.render(self.name, True, (0, 0, 0))
        
        self.quantity_surface = None
        self.quantity_shadow_surface = None
        
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
    
    def use(self, quantity=1):
        if quantity == 1:
            if self.category == "Health":
                if self.player.health == self.player.health_limit:
                    GLOBAL_NOTIFICATIONS.append(
                        notification.Notification(text="Your Health is Full, no Need to Use Health.", color="#a2af28",
                                                x=self.x, y=self.y)
                    )
                    # self.inc()
                else:
                    self.player.health_system(health=self.amount)
                    GLOBAL_NOTIFICATIONS.append(
                        notification.Notification(text=f"+{self.amount} {self.category}", color="#006e00",
                                                x=self.x, y=self.y)
                    )
                    self.dic()
            elif self.category == "Ammo":
                self.player.weapon_ammo_count += self.amount
                GLOBAL_NOTIFICATIONS.append(
                    notification.Notification(text=f"+{self.amount} {self.category}", color="#6b7407",
                                            x=self.x, y=self.y)
                )
                self.dic()
        else:
            steps = 0
            if self.category == "Health":
                amount = 0
                for _ in range(quantity):
                    if self.player.health == self.player.health_limit:
                        if steps == 0:
                            GLOBAL_NOTIFICATIONS.append(
                                notification.Notification(text="Your Health is Full, no Need to Use Health.", color="#a2af28",
                                                        x=self.x, y=self.y)
                            )
                        else:
                            GLOBAL_NOTIFICATIONS.append(
                                notification.Notification(text=f"+{amount} {self.category}", color="#006e00",
                                                        x=self.x, y=self.y)
                            )
                        break
                    else:
                        self.player.health_system(health=self.amount) 
                        amount += self.amount
                        self.dic()
                        steps += 1
                if steps == quantity:
                    GLOBAL_NOTIFICATIONS.append(
                        notification.Notification(text=f"+{amount} {self.category}", color="#006e00",
                                                x=self.x, y=self.y)
                    )
                    
            elif self.category == "Ammo":
                amount = 0
                for _ in range(quantity):
                    self.player.weapon_ammo_count += self.amount
                    amount += self.amount
                    self.dic()
                    
                GLOBAL_NOTIFICATIONS.append(
                    notification.Notification(text=f"+{amount} {self.category}", color="#6b7407",
                                            x=self.x, y=self.y)
                )
        if self.quantity == 0:
            self.kill()
    
    def fix_position(self):
        pass
    
    def drop(self):
        self.kill()
