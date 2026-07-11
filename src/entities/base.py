# src/entities/base.py
import pygame


class Entity(pygame.sprite.Sprite):
    """
    BASE ENTITY (inherits from pygame.sprite.Sprite)

    Key changes from the legacy design:
    - Extends pygame.sprite.Sprite so it can be added to any Group
      (all_sprites, zombies_group, …) and leverage group collision helpers.
    - Every subclass must provide self.image (a Surface) so that
      group.draw(screen) works automatically.
    - self.kill() is available out of the box — no more manual list removal.
    """

    def __init__(self, x, y, width, height, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.health = 100
        self.health_limit = 100

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height

    def health_system(self, entity=None, health=None):
        if entity:
            if self.health > entity.damage:
                self.health -= entity.damage
            else:
                self.health = 0
            self.is_dead = True if self.health == 0 else False
        if health:
            if self.health_limit >= self.health + health:
                self.health += health
            else:
                self.health = self.health_limit

    def get_health_bar_index(self, slices):
        base = self.health_limit / slices
        value = self.health_limit - self.health
        idx = int(value // base)
        return max(0, min(idx, slices - 1))

    def world_draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))
