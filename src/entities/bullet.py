# src/entities/bullet.py
import random
import pygame
import src.assets_manager as assets
from src.entities.base import Entity
from src.core.id_generator import id_generator


class Bullet(Entity):
    """💥 BALLISTIC PROJECTILE"""

    def __init__(self, x, y, dir_x, dir_y, *groups, speed=40, max_dist=600):
        super().__init__(x, y, 6, 6, *groups)
        self.dir_x = dir_x
        self.dir_y = dir_y

        self.traveled = 0
        self.speed = speed
        self.max_dist = max_dist
        self.damage = random.randint(40, 80)

        self.ID = id_generator.next_id("bullet")
        self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (3, 3), 3)

    def update(self):
        """Returns True when the bullet's travel distance is exhausted.
        The caller decides whether to kill(), preserving the original
        control flow where the game loop manages removal."""
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        self.update_rect()
        self.traveled += self.speed
        return self.traveled >= self.max_dist


class DeadBullet(Entity):
    """🔸 ظرف الطلقة الفاضي اللي بيقع بعد الإطلاق (تأثير بصري بس)"""

    def __init__(self, x, y, *groups):
        super().__init__(x, y, 10, 10, *groups)

        self.vx = random.uniform(-1, 3)
        self.vy = random.uniform(-3, 2)
        self.gravity = 0.5
        self.lifetime = 15

        self.image = assets.sprites["empty_bullets"][random.randrange(0, len(assets.sprites["empty_bullets"]) - 1)]
        self.rect = pygame.Rect(x, y, 10, 10)

    def update(self):
        if self.lifetime > 0:
            self.vy += self.gravity
            self.x += self.vx
            self.y += self.vy
        self.lifetime -= 1
        self.update_rect()
        return self.lifetime > 0

    def update_rect(self):
        self.rect.x = self.x + 10
        self.rect.y = self.y + 10
