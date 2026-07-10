# src/entities/player.py
import pygame
import src.systems.combat_helpers as combat
from src.entities.base import Entity
from src.settings import WORLD_WIDTH, WORLD_HEIGHT, WALLS
from src.ui import notification
import src.assets_manager as assets


class Player(Entity):
    def __init__(self, x, y, animations, *groups):
        super().__init__(x, y, 60, 90, *groups)

        self.animations = animations
        self.move_direction = "down"

        self.is_dead = False
        self.current_frame = 0.0
        self.moving = False
        self.firing = False
        self.speed = 5

        self.weapon_type = "Rifle"
        self.ammo_type = "5.56×45mm"
        self.weapon_ammo_count = 20
        self.ammo_stack = 20
        self.ammo_count = 20

        self.coins = 13465

        self.step_counter = 0
        self.step_timer = 20

        self.animation_speed = 0.2
        self.fire_animation_speed = 0.6
        
        self.interact_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

        self.update_rect()

    def update_rect(self):
        self.rect.x = self.x + (self.width - 45)
        self.rect.y = self.y + (self.height - 35)
        self.rect.width = 30
        self.rect.height = 30
        
        self.interact_rect.x = self.x - 5
        self.interact_rect.y = self.y + 35
        self.interact_rect.width = (self.image.get_width() // 2) - 10
        self.interact_rect.height = (self.image.get_height() // 2) - 10
        
    def draw_health_bar(self, screen, x, y):
        screen.blit(assets.sprites["player_health_bar"], (x, y))

    def reload(self, keys, mouse):
        if keys[pygame.K_r] or mouse[2]:
            if self.ammo_count == self.ammo_stack or self.weapon_ammo_count <= 0:
                return
            needed = self.ammo_stack - self.ammo_count
            amount_to_load = min(needed, self.weapon_ammo_count)
            self.ammo_count += amount_to_load
            self.weapon_ammo_count -= amount_to_load
            combat.play_sound_randomly("reload")

    def move(self, keys, base=None, trees=()):
        old_x, old_y = self.x, self.y
        dx, dy = 0, 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed

        self.x += dx
        self.update_rect()
        
        for tree in trees:
            if self.rect.colliderect(tree.rect):
                self.x = old_x
                
        for wall in WALLS: 
            if self.rect.colliderect(wall):
                self.x = old_x
                self.update_rect()

        self.y += dy
        self.update_rect()
        
        for tree in trees:
            if self.rect.colliderect(tree.rect):
                self.y = old_y
                
        for wall in WALLS:
            if self.rect.colliderect(wall):
                self.y = old_y
                self.update_rect()

        if (self.rect.colliderect(base.rect) or self.rect.colliderect(base.rect_n)
                or self.rect.colliderect(base.rect_e) or self.rect.colliderect(base.rect_w)):
            self.x = old_x
            self.y = old_y

        self.x = max(0, min(WORLD_WIDTH - self.width, self.x))
        self.y = max(0, min(WORLD_HEIGHT - self.height, self.y))
        self.update_rect()

        self.moving = (dx != 0 or dy != 0)

        if self.moving:
            self.move_direction = combat.get_angle(dx, dy)

    def determine_action_state(self):
        if not self.firing:
            return "Idle" if not self.moving else "Run"
        if not self.moving:
            return "Attack1"
        return "RunAttack"

    def update_animation(self, action_state):
        if "Attack" in action_state or action_state == "Attack1":
            current_speed = self.fire_animation_speed
        else:
            current_speed = self.animation_speed

        self.current_frame += current_speed

        if action_state in ["Run", "RunAttack"]:
            self.step_counter += 1
            if self.step_counter >= self.step_timer:
                combat.play_sound_randomly("move")
                self.step_counter = 0

        animation_pool = self.animations.get(action_state, self.animations["Idle"]).get(self.move_direction, [])
        if len(animation_pool) == 0:
            self.current_frame = 0
            return

        if self.current_frame >= len(animation_pool):
            self.current_frame = 0.0
            if "Attack" in action_state or action_state == "Attack1":
                self.firing = False

    def get_current_image(self, camera_x, camera_y):
        """
        Updates self.image in-place (not just returning a surface).
        This keeps the sprite ready for automatic rendering via
        all_sprites.draw(screen) if we ever switch from manual blitting.
        """
        action = self.determine_action_state()

        if not self.moving:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_mx = mouse_x + camera_x
            world_my = mouse_y + camera_y
            p_cx = self.x + self.width // 2
            p_cy = self.y + self.height // 2
            dx = world_mx - p_cx
            dy = world_my - p_cy
            self.move_direction = combat.get_angle(dx, dy)

        state_pool = self.animations.get(action, self.animations["Idle"])
        frame_list = state_pool.get(self.move_direction, state_pool.get("down", []))

        frame_idx = int(self.current_frame) % max(1, len(frame_list))
        self.image = frame_list[frame_idx]
        return self.image

    def draw_health_bar(self, screen, x, y):
        screen.blit(assets.sprites["player_health_bar"], (x, y))

    def check_in_gate_notification(self, amount):
        return notification.FixedNotification(text=f"Wanna Pay {amount} for Enter?", image=assets.sprites["E"])
        
    def check_out_gate_notification(self):
        return notification.FixedNotification(text="Wanna Exit?", image=assets.sprites["E"])

    def player_alert(self, text, image=None):
        return notification.Notification(text, image)

    def pay(self, amount):
        if self.coins < amount:
            return False
        self.coins -= amount
        return True