import pygame
import math
import random
import src.central_managment as manage
from src.settings import WORLD_WIDTH, WORLD_HEIGHT, ZOMBIE_ID, BULLET_ID

def set_id():
    global ZOMBIE_ID
    ZOMBIE_ID += 1
    manage.debugger("z_c", f"zombie_{ZOMBIE_ID}")
    return f"zombie_{ZOMBIE_ID}"

def set_bullet_id():
    global BULLET_ID
    BULLET_ID += 1
    return f"bullet_{BULLET_ID}"

class Entity(pygame.sprite.Sprite):
    """
    🧱 BASE GAME-OBJECT BLUEPRINT
    Every dynamic object inside Last Green inherits from this base class.
    We track independent world coordinates (x, y) and link them directly to a Pygame Rect.
    """
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # self.rect handles precise AABB (Axis-Aligned Bounding Box) collisions.
        self.rect = pygame.Rect(x, y, width, height)

    def update_rect(self):
        """Syncs the float/integer coordinate trackers with our engine collision system."""
        self.rect.x = self.x
        self.rect.y = self.y + 20


class Player(Entity):
    """🧑‍🚀 THE SURVIVOR CLASS"""
    def __init__(self, x, y, animation_dict):
        # We specify a small 40x40 hitbox. This means the player's FEET collide with 
        # obstacles, while their upper body can overlappingly pass behind trees realistically!
        super().__init__(x, y, width=60, height=90)
        self.animations = animation_dict
        self.direction = "down"
        self.weapon_type = "Sniper"
        self.moving = False
        self.current_frame = 0
        self.speed = 5
        self.ammo_type = "7.62"
        self.ammo_count = 64
        self.weapon_ammo_count = 6
        self.animation_speed = 0.2
        # self.rect = pygame.Rect(x, y, self.width, self.height)

    def move(self, keys, trees):
        """
        🕹️ 2-AXIS SEPARATED MOVEMENT MECHANIC
        Moves the player and checks for collisions independently along each axis.
        This prevents the player from getting 'stuck' completely when walking diagonally into obstacles.
        """
        old_x, old_y = self.x, self.y
        dx, dy = 0, 0

        # Read movement vectors
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy = self.speed

        # --- STEP 1: Execute Horizontal Movement and Verify Walls ---
        self.x += dx
        self.update_rect()
        for tree in trees:
            if self.rect.colliderect(tree.rect):
                self.x = old_x  # Crash detected! Revert x position immediately.
                self.update_rect()

        # --- STEP 2: Execute Vertical Movement and Verify Walls ---
        self.y += dy
        self.update_rect()
        for tree in trees:
            if self.rect.colliderect(tree.rect):
                self.y = old_y  # Crash detected! Revert y position immediately.
                self.update_rect()

        # --- STEP 3: Zone Perimeter Constraints (World Border Boundaries) ---
        self.x = max(0, min(WORLD_WIDTH - self.width, self.x))
        self.y = max(0, min(WORLD_HEIGHT - self.height, self.y))
        self.update_rect()
        
        manage.debugger("p_p", self.x, self.y)

        # Update which way our survivor is looking based on input vectors
        self.update_direction_name(dx, dy)

    def update_direction_name(self, dx, dy):
        """Translates basic velocity inputs into an 8-way compass system."""
        self.moving = (dx != 0 or dy != 0)
        if dx == 0 and dy < 0:    self.direction = "up"
        elif dx == 0 and dy > 0:  self.direction = "down"
        elif dx < 0 and dy == 0:  self.direction = "left"
        elif dx > 0 and dy == 0:  self.direction = "right"
        elif dx > 0 and dy < 0:   self.direction = "up_right"
        elif dx < 0 and dy < 0:   self.direction = "up_left"
        elif dx > 0 and dy > 0:   self.direction = "down_right"
        elif dx < 0 and dy > 0:   self.direction = "down_left"

    def update_animation(self):
        """Cycles through running animation frames if our survivor is putting in miles."""
        if self.moving:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.animations[self.direction]):
                self.current_frame = 0  # Loop back around
        else:
            self.current_frame = 0  # Idle default (rest frame)

    def get_current_image(self):
        """Returns the specific graphical texture mapped for this animation loop interval."""
        return self.animations[self.direction][int(self.current_frame)]


class Zombie(Entity):
    """🧟 THE HORDE"""
    def __init__(self, x, y, animation_dict):
        super().__init__(x, y, width=70, height=70)
        self.animations = animation_dict
        self.direction = "down"
        self.speed = 2
        self.current_frame = 0
        self.animation_speed = 0.2
        self.ID = set_id()
        
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
                if item.ID != self.ID and self.rect.colliderect(item.rect):
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
                if item.ID != self.ID and self.rect.colliderect(item.rect):
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
            # We invert dy because Pygame's Y axis goes down instead of up
            angle = math.atan2(-dy, dx)
            # Convert radians to degrees (0 to 360)
            degrees = math.degrees(angle)
            if degrees < 0:
                degrees += 360

            # 3. Compass Mapping: Map the 360° circle into 8 directional slices of 45° each
            if 22.5 <= degrees < 67.5:
                self.direction = "up_right"
            elif 67.5 <= degrees < 112.5:
                self.direction = "up"
            elif 112.5 <= degrees < 157.5:
                self.direction = "up_left"
            elif 157.5 <= degrees < 202.5:
                self.direction = "left"
            elif 202.5 <= degrees < 247.5:
                self.direction = "down_left"
            elif 247.5 <= degrees < 292.5:
                self.direction = "down"
            elif 292.5 <= degrees < 337.5:
                self.direction = "down_right"
            else:
                self.direction = "right"  # Covers 337.5 to 360 and 0 to 22.5

        # 4. Animation Frame Tick
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.animations[self.direction]):
            self.current_frame = 0

    def get_current_image(self):
        return self.animations[self.direction][int(self.current_frame)]

class Bullet(Entity):
    """💥 BALLISTIC PROJECTILE LOGIC"""
    def __init__(self, x, y, dir_x, dir_y, speed=18, max_dist=800):
        super().__init__(x, y, width=6, height=6)
        self.dir_x = dir_x  # Pre-calculated normalized direction trajectory x
        self.dir_y = dir_y  # Pre-calculated normalized direction trajectory y
        self.speed = speed
        self.max_dist = max_dist
        self.damage = random.randint(120, 180)
        self.ID = set_bullet_id()
        self.traveled = 0

    def update(self):
        """Advances muzzle distance. Returns True when projectile range expires."""
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        self.update_rect()
        manage.debugger("m_p", int(self.x), int(self.y))
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