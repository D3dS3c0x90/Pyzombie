import pygame

class Entity:
    def __init__(self, x, y, width = 0, height = 0, image = None, entitytype = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.entitytype = entitytype

class Player(Entity):
    def __init__(self, x, y, animations, frame_limit = 14, animation_speed = 0.2):
        super().__init__(x,y, width = 20, height = 35, entitytype = "player")  # Collision size
        self.move0 = animations[0]
        self.move1 = animations[1]
        self.attack1 = animations[2]
        self.attack2 = animations[3]
        self.direction = "down"
        self.moving = False
        self.current_frame = 0
        self.camera_x = 0
        self.camera_y = 0
        self.move_x = 0
        self.move_y = 0
        self.speed = 2
        self.animation_speed = animation_speed
        self.frame_limit = frame_limit

    def move(self, keys):
        """Move player based on keys pressed (supports 8 directions)"""
        # Calculate movement
        move_x = 0
        move_y = 0
        
        if keys[pygame.K_a]:
            move_x = -self.speed
        if keys[pygame.K_d]:
            move_x = self.speed
        if keys[pygame.K_w]:
            move_y = -self.speed
        if keys[pygame.K_s]:
            move_y = self.speed
        
        # Get direction name from movement values
        direction = self.get_direction_from_movement(move_x, move_y)
        
        if direction:
            self.direction = direction
            self.moving = True
        else:
            self.moving = False
        
        # Apply movement
        self.x += move_x
        self.y += move_y
            
    def get_direction_from_movement(self, dx, dy):
        """Convert movement (dx, dy) to direction name"""
        if dx == 0 and dy < 0:
            return "up"
        elif dx == 0 and dy > 0:
            return "down"
        elif dx < 0 and dy == 0:
            return "left"
        elif dx > 0 and dy == 0:
            return "right"
        elif dx > 0 and dy < 0:
            return "up_right"
        elif dx < 0 and dy < 0:
            return "up_left"
        elif dx > 0 and dy > 0:
            return "down_right"
        elif dx < 0 and dy > 0:
            return "down_left"
        else:
            return None  # No movement

    def update_camera(self, screen_width, screen_height, world_width, world_height):
        """Update camera to follow player"""
        # Center camera on player
        self.camera_x = self.x + self.width//2 - screen_width // 2
        self.camera_y = self.y + self.height//2 - screen_height // 2
        
        # Keep camera inside world boundaries
        self.camera_x = max(0, min(world_width - screen_width, self.camera_x))
        self.camera_y = max(0, min(world_height - screen_height, self.camera_y))
    
    def world_to_screen(self, x, y):
        """Convert world coordinates to screen coordinates"""
        screen_x = x - self.camera_x
        screen_y = y - self.camera_y
        return screen_x, screen_y
    
    def get_screen_position(self):
            """Get player's screen position"""
            return self.world_to_screen(self.x, self.y)

class Zombie(Entity):
    def __init__(self, x, y, animations, frame_limit = 8, animation_speed = 0.2):
        super().__init__(x, y, width = 30, height = 45, entitytype = "zombie")  # Collision size
        self.animations = animations
        self.direction = "down"
        self.moving = True
        self.speed = 1
        self.screen_x = 0
        self.screen_y = 0
        self.current_frame = 0
        self.frame_limit = frame_limit
        self.animation_speed = animation_speed

    def zombie_AI_chasing(self, player):
        # Store old position to calculate movement
        old_x, old_y = self.x, self.y
        
        # Move toward player on X axis
        if self.x < player.x:
            self.x += self.speed
        elif self.x > player.x:
            self.x -= self.speed
        
        # Move toward player on Y axis
        if self.y < player.y:
            self.y += self.speed
        elif self.y > player.y:
            self.y -= self.speed
        
        # Calculate actual movement direction
        dx = self.x - old_x
        dy = self.y - old_y
        
        # Determine 8-direction name from movement
        if dx == 0 and dy < 0:
            self.direction = "up"
        elif dx == 0 and dy > 0:
            self.direction = "down"
        elif dx < 0 and dy == 0:
            self.direction = "left"
        elif dx > 0 and dy == 0:
            self.direction = "right"
        elif dx > 0 and dy < 0:
            self.direction = "up_right"
        elif dx < 0 and dy < 0:
            self.direction = "up_left"
        elif dx > 0 and dy > 0:
            self.direction = "down_right"
        elif dx < 0 and dy > 0:
            self.direction = "down_left"
        # If no movement, keep previous direction

        # print(f"Zombie at ({self.x}, {self.y}), Player at ({player.x}, {player.y}) moving {self.direction}")

class Bullet(Entity):
    def __init__(self, x, y, dir_x, dir_y, speed=10, max_distance=300):
        super().__init__(x, y, width=5, height=5)
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = speed
        self.max_distance = max_distance
        self.traveled = 0
        self.color = (255, 255, 0)  # Yellow
    
    def update(self):
        # Move bullet
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        
        # Track distance traveled
        self.traveled += self.speed
        
        # Return True if bullet should disappear
        return self.traveled >= self.max_distance

    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.width, self.height))

class Tree(Entity):
    def __init__(self, x, y, image):
        width = image.get_width()
        height = image.get_height()
        super().__init__(x, y, width, height, image = image, entitytype = "tree")
        self.image = image
        self.entitytype = "tree"

