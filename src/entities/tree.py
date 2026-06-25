# src/entities/tree.py
import pygame
from src.entities.base import Entity


class Tree(Entity):

    def __init__(self, x, y, image, *groups):
        super().__init__(x, y, image.get_width(), image.get_height(), *groups)
        self.image = image
        self.rect = pygame.Rect(x + 35, y + 185, image.get_width() - 80, image.get_height() - 200)
        self.opposite_rect = pygame.Rect(x + 15, y + 200, image.get_width() - 40, image.get_height() - 170)
