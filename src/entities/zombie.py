# src/entities/zombie.py
import math
import random
import pygame
import src.systems.combat_helpers as combat
from src.entities.base import Entity
from src.core.id_generator import id_generator
from src.settings import WALLS


class Zombie(Entity):
    def __init__(self, x, y, move_animation_dict, die_animation_dict, *groups):
        super().__init__(x, y, 75, 75, *groups)

        self.move_animations = move_animation_dict
        self.die_animations = die_animation_dict

        self.move_direction = "down"
        self.die_direction = "down"

        self.is_dead = False

        self.move_current_frame = 0
        self.die_current_frame = 0

        self.move_animation_speed = 0.2
        self.die_animation_speed = 0.15

        self.speed = 3
        self.delay = 0.05
        self.step_delay = 0.05
        self.damage = random.randrange(10, 20)

        self.damage_rect = pygame.Rect(self.x, self.y, self.width + 20, self.height + 30)

        self.ID = id_generator.next_id("zombie")
        self.image = self.move_animations[self.move_direction][0]

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y + 40

    def update_damage_rect(self):
        self.damage_rect.x = self.x - 10
        self.damage_rect.y = self.y + 20

    def update_ai(self, player, base={}, items=(), trees=()):
        """🎯 ملاحقة 8 اتجاهات بناء على trigonometry."""
        if not self.is_dead:
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy)

            if dist > 0:
                move_x = (dx / dist) * self.speed
                move_y = (dy / dist) * self.speed

                old_x = self.x
                self.x += move_x
                self.update_rect()
                for item in items:
                    if item.ID != self.ID and self.rect.colliderect(item.rect) and not item.is_dead and not self.is_dead:
                        self.x = old_x
                        self.update_rect()
                        break
                    
                for wall in WALLS: 
                    if self.rect.colliderect(wall):
                        self.x = old_x
                        self.update_rect()
                        
                for tree in trees:
                    if self.rect.colliderect(tree.rect):
                        self.x = old_x
                        self.update_rect()
                        break

                old_y = self.y
                self.y += move_y
                self.update_rect()
                for item in items:
                    if item.ID != self.ID and self.rect.colliderect(item.rect) and not item.is_dead and not self.is_dead:
                        self.y = old_y
                        self.update_rect()
                        break
                    
                for wall in WALLS: 
                    if self.rect.colliderect(wall):
                        self.y = old_y
                        self.update_rect()
                        
                for tree in trees:
                    if self.rect.colliderect(tree.rect):
                        self.y = old_y
                        self.update_rect()
                        break

                if (self.rect.colliderect(player.rect) or self.rect.colliderect(base.rect)
                        or self.rect.colliderect(base.rect_n) or self.rect.colliderect(base.rect_e)
                        or self.rect.colliderect(base.rect_w)):
                    self.x = old_x
                    self.y = old_y
                    self.update_rect()

                self.move_direction = combat.get_angle(dx, dy)
                self.die_direction = self.move_direction

            self.move_current_frame += self.move_animation_speed
            if self.move_current_frame >= len(self.move_animations[self.move_direction]):
                self.move_current_frame = 0

            self.image = self.move_animations[self.move_direction][int(self.move_current_frame)]
        else:
            self.die_current_frame += self.die_animation_speed
            if self.die_current_frame >= len(self.die_animations[self.die_direction]):
                self.die_current_frame = len(self.die_animations[self.die_direction]) - 1
                self.die_animation_speed = 0
            self.image = self.die_animations[self.die_direction][int(self.die_current_frame)]

    def get_current_image(self, flag="move"):
        if flag == "move":
            return self.move_animations[self.move_direction][int(self.move_current_frame)]
        elif flag == "die":
            return self.die_animations[self.die_direction][int(self.die_current_frame)]

    def draw_health_bar(self, screen, x, y):
        import src.assets_manager as assets
        screen.blit(assets.sprites["zombie_health_bar"][self.get_health_bar_index(12)], (x, y))
