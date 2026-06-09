import pygame
import random


class Items:
    def __init__(self, x, y, image, amount=1, type="", width=30, height=30):
        self.x = x
        self.y = y
        self.speed = 0.5
        self.vertical = 0
        self.width = width
        self.height = height
        self.amount = amount
        self.type = type
        self.up = True
        self.is_taked = False
        self.ID = ""
        self.name = ""
        self.image = image
        self.rect = pygame.Rect(x - 10, y - 10 , image.get_width() + 40, image.get_height() + 40)

    def update_rect(self):
        """
        📐 HITBOX FOOT COMPENSATOR
        Instead of placing the box at the top-left (0,0) of the image, 
        we shift it down towards the feet and center it horizontally.
        """
        # Adjust these numbers if you want the box tighter or looser!
        self.rect.x = self.x + self.width
        self.rect.y = self.y + (self.height * 2)
        
    def set_name_id(self, name, count):
        self.name = f"{name}"
        self.ID = f"{name}_{count}"
        
class DropedItem(Items):
    def __init__(self, x, y, image, amount, type):
        super().__init__(x, y, image, amount, type)
        self.amount = amount
        
    def up_down(self):
        self.up = False if self.vertical == 20.0 else True if self.vertical < 0.0 else self.up
        self.vertical += self.speed if self.up else -self.speed
        self.update_rect()
        
class Ammo(DropedItem):
    def __init__(self, x, y, image, amount, type):
        super().__init__(x, y, image, amount, type)
        
class Health(DropedItem):
    def __init__(self, x, y, image, type, amount=None):
        super().__init__(x, y, image, amount, type)
        self.amount = random.choice([10, 25, 50, 5, 45, 30])
        
class Chest(Items):
    def __init__(self, x, y):
        super().__init__(x, y)
        