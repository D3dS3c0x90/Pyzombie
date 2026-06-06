import pygame
import math
import random
import src.central_managment as manage
import src.assets_manager as assets
from src.settings import *

class Entity:
    """Class to manage base positions, sizes, and physics rect components."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Base rectangle setup fallback
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_rect(self):
        """Standard uniform hitbox mapping adjustment loop."""
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height


# ==============================================================================
# 🧑‍🚀 THE UPDATED SURVIVOR CLASS (Inheriting from Entity)
# ==============================================================================
class Player(Entity):
    def __init__(self, x, y, animations_hub):
        # Pass positioning specifications right up into the Entity base class layout
        super().__init__(x, y, width=60, height=90)
        
        self.anims = animations_hub
        self.move_direction = "down"
        
        self.current_frame = 0.0
        self.moving = False
        self.firing = False
        self.speed = 5
        
        self.weapon_type = "Sniper"
        self.weapon_ammo_count = 360
        self.ammo_type = "7.62"
        self.ammo_stack = 6
        self.ammo_count = 6
        
        self.step_counter = 0
        self.step_timer = 20
        
        # ⚡ ANIMATION CYCLE SPEEDS
        self.animation_speed = 0.2       # Default walk/idle speed
        self.fire_animation_speed = 0.6  # Snappy combat weapon speed
        
        # Override standard rect to give player a tight footprint at their feet
        self.update_rect()

    def update_rect(self):
        """Aligns the processing hitbox to map structural feet placement coordinates."""
        self.rect.x = self.x + (self.width - 70)
        self.rect.y = self.y + (self.height - 80) 
        self.rect.width = 80
        self.rect.height = 80

    def reload(self, keys):
        if keys[pygame.K_r]:
            if self.ammo_count == self.ammo_stack or self.weapon_ammo_count <= 0:
                return 
            needed = self.ammo_stack - self.ammo_count
            amount_to_load = min(needed, self.weapon_ammo_count)
            self.ammo_count += amount_to_load
            self.weapon_ammo_count -= amount_to_load
            manage.get_sound_randomly("reload", assets.sounds).play()

    def move(self, keys, trees):
        old_x, old_y = self.x, self.y
        dx, dy = 0, 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy = self.speed

        # --- STEP 1: Horizontal Checks ---
        self.x += dx
        self.update_rect()
        for tree in trees:
            if self.rect.colliderect(tree.rect):
                self.x = old_x
                self.update_rect()

        # --- STEP 2: Vertical Checks ---
        self.y += dy
        self.update_rect()
        for tree in trees:
            if self.rect.colliderect(tree.rect):
                self.y = old_y
                self.update_rect()

        # --- STEP 3: Boundary Constraints ---
        self.x = max(0, min(WORLD_WIDTH - self.width, self.x))
        self.y = max(0, min(WORLD_HEIGHT - self.height, self.y))
        self.update_rect()
        
        self.moving = (dx != 0 or dy != 0)

        # 🧭 NEW DIRECTION LOGIC: If moving, overwrite direction using input vectors
        if self.moving:
            self.move_direction = manage.get_angle(dx, dy)
        
        # 🛠️ POSITION DEBUGGER ENABLED
        manage.debugger("p_p", self.x, self.y)

    def determine_action_state(self):
        if not self.firing:
            return "Idle" if not self.moving else "Run"
        if not self.moving:
            return "Attack1"
        return "RunAttack"

    def update_animation(self, action_state):
        # 🛠️ MOVEMENT STATE DEBUGGER ENABLED
        manage.debugger("p_m", "Running" if self.moving else "Firing" if self.firing else "IDLE")

        # ⚡ DYNAMIC ANIMATION SPEED SELECTOR
        if "Attack" in action_state or action_state == "Attack1":
            current_speed = self.fire_animation_speed
        else:
            current_speed = self.animation_speed
        
        self.current_frame += current_speed
        
        if action_state in ["Run", "RunAttack"]:
            self.step_counter += 1
            if self.step_counter >= self.step_timer:
                manage.get_sound_randomly("move", assets.sounds).play()
                self.step_counter = 0

        animation_pool = self.anims.get(action_state, self.anims["Idle"]).get(self.move_direction, [])
        if len(animation_pool) == 0:
            self.current_frame = 0
            return

        if self.current_frame >= len(animation_pool):
            self.current_frame = 0.0
            if "Attack" in action_state or action_state == "Attack1":
                self.firing = False

    def get_current_image(self, camera_x, camera_y):
        action = self.determine_action_state()

        # 🧭 NEW DIRECTION LOGIC: Only look at the mouse if we are NOT running
        if not self.moving:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_mx = mouse_x + camera_x
            world_my = mouse_y + camera_y
            
            p_cx = self.x + self.width // 2
            p_cy = self.y + self.height // 2
            dx = world_mx - p_cx
            dy = world_my - p_cy
            
            self.move_direction = manage.get_angle(dx, dy)
        
        state_pool = self.anims.get(action, self.anims["Idle"])
        frame_list = state_pool.get(self.move_direction, state_pool.get("down", []))
        
        frame_idx = int(self.current_frame) % max(1, len(frame_list))
        return frame_list[frame_idx]
      
class Zombie(Entity):
    """🧟 THE HORDE"""
    def __init__(self, x, y, move_animation_dict, die_animation_dict):
        super().__init__(x, y, width=70, height=70)
        self.move_animations = move_animation_dict
        self.die_animations = die_animation_dict
        self.move_direction = "down"
        self.die_direction = "down"
        self.is_dead = False
        self.speed = 2
        self.health = 100
        self.move_current_frame = 0
        self.die_current_frame = 0
        self.move_animation_speed = 0.2
        self.die_animation_speed = 0.15
        self.ID = self.set_id()
        
    def set_id(self):
        global ZOMBIE_ID
        ZOMBIE_ID += 1
        manage.debugger("z_c", f"zombie_{ZOMBIE_ID}")
        return f"zombie_{ZOMBIE_ID}"

    def update_rect(self):
        """
        📐 HITBOX FOOT COMPENSATOR
        Instead of placing the box at the top-left (0,0) of the image, 
        we shift it down towards the feet and center it horizontally.
        """
        # Adjust these numbers if you want the box tighter or looser!
        self.rect.x = self.x + 20
        self.rect.y = self.y + 50

    def update_ai(self, player, items=[], trees=[]):
        """
        🎯 8-DIRECTIONAL VECTOR CHASE CALCULATIONS
        Uses trigonometry to chase the player smoothly and dynamically switch 
        between all 8 animation states (including diagonals).
        """
        
        if self.is_dead == False:
            old_x, old_y = self.x, self.y
            
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy) # Calculates Hypotenuse: sqrt(dx^2 + dy^2)

            if dist > 0:
                # Calculate our step size for this specific frame
                move_x = (dx / dist) * self.speed
                move_y = (dy / dist) * self.speed

                # ------------------------------------------------------------------
                # ➡️ AXIS 1: HORIZONTAL RESOLUTION
                # ------------------------------------------------------------------
                old_x = self.x     # Set checkpoint for X
                self.x += move_x
                self.update_rect() # Push hitbox out to test the waters
                
                for item in items:
                    if item.ID != self.ID and self.rect.colliderect(item.rect) and (item.is_dead == False and self.is_dead == False):
                        manage.debugger("z_z", int(self.x), int(self.y))
                        self.x = old_x      # Collision! Snap back to checkpoint
                        self.update_rect()  # Sync hitbox back immediately
                        break               # Stop checking other items this frame
                    
                for tree in trees:
                    if self.rect.colliderect(tree.rect):
                        manage.debugger("z_t", int(self.x), int(self.y))
                        self.x = old_x      # Collision! Snap back to checkpoint
                        self.update_rect()  # Sync hitbox back immediately
                        break               # Stop checking other items this frame
                        

                # ------------------------------------------------------------------
                # ⬇️ AXIS 2: VERTICAL RESOLUTION
                # ------------------------------------------------------------------
                old_y = self.y     # Set checkpoint for Y
                self.y += move_y
                self.update_rect() # Push hitbox out to test the waters
                
                for item in items:
                    if item.ID != self.ID and self.rect.colliderect(item.rect) and (item.is_dead == False and self.is_dead == False):
                        manage.debugger("z_z", int(self.x), int(self.y))
                        self.y = old_y      # Collision! Snap back to checkpoint
                        self.update_rect()  # Sync hitbox back immediately
                        break               # Stop checking other items this frame
                    
                for tree in trees:
                    if self.rect.colliderect(tree.rect):
                        manage.debugger("z_t", int(self.x), int(self.y))
                        self.y = old_y      # Collision! Snap back to checkpoint
                        self.update_rect()  # Sync hitbox back immediately
                        break               # Stop checking other items this frame

                # 2. Angular Animation Logic: Get the angle in radians (-pi to pi)
                self.move_direction = manage.get_angle(dx, dy)
                self.die_direction = self.move_direction

            # 4. Animation Frame Tick

            self.move_current_frame += self.move_animation_speed
            if self.move_current_frame >= len(self.move_animations[self.move_direction]):
                self.move_current_frame = 0
        else:
            self.die_current_frame += self.die_animation_speed
            # self.die_direction = self.move_direction
            if self.die_current_frame >= len(self.die_animations[self.move_direction]):
                self.die_current_frame = len(self.die_animations[self.move_direction]) - 1
                self.die_animation_speed = 0
        

    def get_current_image(self, flag="move"):
        if flag == "move":
            return self.move_animations[self.move_direction][int(self.move_current_frame)]
        elif flag == "die":
            return self.die_animations[self.die_direction][int(self.die_current_frame)]

class Bullet(Entity):
    """💥 BALLISTIC PROJECTILE LOGIC"""
    def __init__(self, x, y, dir_x, dir_y, speed=50, max_dist=800):
        super().__init__(x, y, width=6, height=6)
        self.dir_x = dir_x  # Pre-calculated normalized direction trajectory x
        self.dir_y = dir_y  # Pre-calculated normalized direction trajectory y
        self.speed = speed
        self.max_dist = max_dist
        self.damage = random.randint(120, 180)
        self.ID = self.set_bullet_id()
        self.traveled = 0
        
    def set_bullet_id(self):
        global BULLET_ID
        BULLET_ID += 1
        return f"bullet_{BULLET_ID}"

    def update(self):
        """Advances muzzle distance. Returns True when projectile range expires."""
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        self.update_rect()
        manage.debugger("m_p", int(self.x), int(self.y))
        manage.debugger("b_d", manage.get_angle(self.dir_x, self.dir_y))
        self.traveled += self.speed
        return self.traveled >= self.max_dist

class Tree(Entity):
    """🌲 MAP OBSTACLE / STATIC SCRAPERS"""
    def __init__(self, x, y, image):
        # We offset the tree collision block. The player can walk behind tree branches,
        # but will hit a wall when passing through the bottom 40 pixels (the trunk base).
        super().__init__(x, y, image.get_width(), image.get_height())
        self.image = image
        # if you want to change any value about the collision, change the line below
        self.rect = pygame.Rect(x + 15, y + 260, image.get_width() - 40, image.get_height() - 170)