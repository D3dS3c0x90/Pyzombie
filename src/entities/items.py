# src/entities/items.py
import random
import pygame
from src.entities.base import Entity


class Item(Entity):
    def __init__(self, x, y, image, *groups, amount=1, type="", width=10, height=10):
        super().__init__(x, y, width, height, *groups)
        self.speed = 0.5
        self.vertical = 0
        self.amount = amount
        self.type = type
        self.up = True
        self.is_taked = False
        self.ID = ""
        self.name = ""
        self.image = image
        self.rect = pygame.Rect(x - 10, y - 10, image.get_width() + 10, image.get_height() + 10)

    def update_rect(self):
        self.rect.x = self.x + self.width
        self.rect.y = self.y + (self.height * 2)

    def set_name_id(self, name, count):
        self.name = f"{name}"
        self.ID = f"{name}_{count}"


class DroppedItem(Item):
    def __init__(self, x, y, image, amount, type, *groups):
        super().__init__(x, y, image, *groups, amount=amount, type=type)

    def up_down(self):
        self.up = False if self.vertical == 20.0 else True if self.vertical < 0.0 else self.up
        self.vertical += self.speed if self.up else -self.speed
        self.update_rect()


class Ammo(DroppedItem):
    pass


class Coins(DroppedItem):
    pass


class Health(DroppedItem):
    def __init__(self, x, y, image, type, *groups, amount=None):
        super().__init__(x, y, image, amount, type, *groups)
        self.amount = random.choice([10, 15, 5, 20, 25])


class Chest(Item):
    def __init__(self, x, y, image, *groups):
        super().__init__(x, y, image, *groups)
