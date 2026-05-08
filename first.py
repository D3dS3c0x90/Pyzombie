import pygame
import random

class Entity:
    def __init__(self, x, y, width, height, color = None, image = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = image  
        self.speed = 2

class Player(Entity):
    def __init__(self, x, y, animations):
        first_frame = animations["down"][0]
        
        # BIG image size (for drawing)
        image_width = first_frame.get_width()   # 128+80 = 208
        image_height = first_frame.get_height()
        
        # SMALL collision size (for gameplay)
        collision_width = 40
        collision_height = 40
        
        # Entity uses collision size
        super().__init__(x, y, collision_width, collision_height, color=None)
        
        # Store image for drawing
        self.image = first_frame
        self.visual_width = image_width
        self.visual_height = image_height
        self.animations = animations
        self.speed = 5
        self.direction = "down"
        self.current_frame = 0
        self.animation_speed = 0.2
        self.moving = False
    
    def set_direction_from_keys(self, keys):
        """Set direction based on which keys are pressed"""
        left = keys[pygame.K_a]
        right = keys[pygame.K_d]
        up = keys[pygame.K_w]
        down = keys[pygame.K_s]
        
        # Check diagonals first (8 directions!)
        if up and left:
            self.direction = "up_left"
            self.moving = True
        elif up and right:
            self.direction = "up_right"
            self.moving = True
        elif down and left:
            self.direction = "down_left"
            self.moving = True
        elif down and right:
            self.direction = "down_right"
            self.moving = True
        elif left:
            self.direction = "left"
            self.moving = True
        elif right:
            self.direction = "right"
            self.moving = True
        elif up:
            self.direction = "up"
            self.moving = True
        elif down:
            self.direction = "down"
            self.moving = True
        else:
            self.moving = False

    def update_animation(self):
        """Update which frame to show"""
        if self.moving:
            self.current_frame += self.animation_speed
            num_frames = len(self.animations[self.direction])
            if self.current_frame >= num_frames:
                self.current_frame = 0
        else:
            self.current_frame = 0  # Idle frame (first frame)

    def get_current_image(self):
        """Return the current frame image"""
        frames = self.animations[self.direction]
        return frames[int(self.current_frame)]

class Zombie(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, color = (60, 100, 40))
        self.speed = 2

class Tree(Entity):
    def __init__(self, x, y, image):
        width = image.get_width()
        height = image.get_height()
        super().__init__(x, y, width, height, image = image)
        self.image = image

def check_collision(player, tree):
    return (player.x < tree.x + tree.width and
            player.x + player.width > tree.x and
            player.y < tree.y + tree.height and
            player.y + player.height > tree.y)

# Pick from multiple colors
colors = [
    (101, 67, 33),   # Brown
    (34, 139, 34),   # Forest green
    (50, 100, 50),   # Dark green
    (85, 107, 47),   # Olive
    (60, 80, 40)     # Moss
]
 
pygame.init()

# Load the entire sprite sheet
all_trees_png = pygame.image.load("Trees.png")
single_tree = all_trees_png.subsurface((0, 0, 80, 160))
single_tree = pygame.transform.scale(single_tree, (120, 240)) 

single_boush_1 = all_trees_png.subsurface((185, 75, 50, 50))
single_boush_1 = pygame.transform.scale(single_boush_1, (80, 80))

single_boush_2 = all_trees_png.subsurface((190, 130, 40, 40))
single_boush_2 = pygame.transform.scale(single_boush_2, (80, 80))

# Player Movies
player_move_png = pygame.image.load("CrouchRun.png")                    # 1792 x 1024 (14 frames, 8 directions)
# Get total size
total_width = player_move_png.get_width()
total_height = player_move_png.get_height()

# Calculate frame size
FRAME_WIDTH = total_width // 14   # 14 frames per row
FRAME_HEIGHT = total_height // 8  # 8 directions (rows)

all_frames = {}

for row in range(8):
    row_frames = []
    for col in range(14):
        x = col * FRAME_WIDTH
        y = row * FRAME_HEIGHT
        frame = player_move_png.subsurface((x, y, FRAME_WIDTH, FRAME_HEIGHT))
        frame = pygame.transform.scale(frame, (frame.get_width() + 80, frame.get_height() + 80))  # Scale up for better visibility
        row_frames.append(frame)
    all_frames[row] = row_frames

animations = {
    "right": all_frames[0],
    "down_right": all_frames[1],
    "down": all_frames[2],
    "down_left": all_frames[3],
    "left": all_frames[4],
    "up_left": all_frames[5],
    "up": all_frames[6],
    "up_right": all_frames[7],
}

# player_move = player_move_png.subsurface((0, 0, 80, 160))

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 830
WORLD_WIDTH = 5000
WORLD_HEIGHT = 5000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Last Green - Huge Forest World")

player = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2, animations)
zombie = Zombie(1000, 1000)

# Create trees scattered across the world
trees = []

for i in range(100):  # 100 trees
    trees.append(Tree(
    random.randint(0, WORLD_WIDTH - 60),
    random.randint(0, WORLD_HEIGHT - 80),
    image = random.choice([single_tree, single_boush_1, single_boush_2])
))

running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # In your game loop:

    # Store old position
    old_x, old_y = player.x, player.y

    # Get keys
    keys = pygame.key.get_pressed()

    # Set direction for animation
    player.set_direction_from_keys(keys)

    # Calculate movement
    move_x = 0
    move_y = 0

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        move_x = -player.speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        move_x = player.speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        move_y = -player.speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        move_y = player.speed

    # Apply movement
    player.x += move_x
    player.y += move_y

    # Check collision with trees
    for tree in trees:
        if check_collision(player, tree):
            player.x, player.y = old_x, old_y
            break

    # World boundaries
    player.x = max(0, min(WORLD_WIDTH - player.width, player.x))
    player.y = max(0, min(WORLD_HEIGHT - player.height, player.y))

    # Update animation
    player.update_animation()

    # Player boundaries (WORLD limits)
    player.x = max(0, min(WORLD_WIDTH - player.width, player.x))
    player.y = max(0, min(WORLD_HEIGHT - player.height, player.y))

    # Zombie AI
    if zombie.x < player.x:
        zombie.x += zombie.speed
    elif zombie.x > player.x:
        zombie.x -= zombie.speed
    if zombie.y < player.y:
        zombie.y += zombie.speed
    elif zombie.y > player.y:
        zombie.y -= zombie.speed

    # Camera follows player
    camera_x = player.x + player.width//2 - SCREEN_WIDTH // 2
    camera_y = player.y + player.height//2 - SCREEN_HEIGHT // 2
    camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, camera_x))
    camera_y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, camera_y))

    # Convert to screen coordinates
    screen_player_x = player.x - camera_x
    screen_player_y = player.y - camera_y
    screen_zombie_x = zombie.x - camera_x
    screen_zombie_y = zombie.y - camera_y
    
    # 1. Background (clears screen)
    screen.fill((34, 68, 34))

    for tree in trees:
        if check_collision(player, tree):
            player.x, player.y = old_x, old_y  # Revert to old position
            break
    
    counter = 0
    # 2. Trees (behind player and zombie)
    for tree in trees:
        screen_tree_x = tree.x - camera_x
        screen_tree_y = tree.y - camera_y

        # Only draw if visible (optimization)
        if -80 < screen_tree_x < SCREEN_WIDTH + 80 and -80 < screen_tree_y < SCREEN_HEIGHT + 80:
            screen.blit(tree.image, (screen_tree_x, screen_tree_y))
    
    # 3. Zombie
    pygame.draw.rect(screen, zombie.color, (screen_zombie_x, screen_zombie_y, zombie.width, zombie.height))
    
    # 4. Player (on top) - with centering!
    current_player_image = player.get_current_image()

    # Center the big image over the small collision box
    draw_x = screen_player_x - (current_player_image.get_width() - player.width) // 2
    draw_y = screen_player_y - (current_player_image.get_height() - player.height) // 2

    screen.blit(current_player_image, (draw_x, draw_y))

    # 5. Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()