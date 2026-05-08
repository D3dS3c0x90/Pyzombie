import pygame
import random
import entities, characters, mousefeatures, map

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 830
WORLD_WIDTH = 2000
WORLD_HEIGHT = 2000
PLAYER_START_POINT = 1000

def entity_moving(entity, speed, frames):
    if entity.moving:
        entity.current_frame += speed
        if entity.current_frame >= frames:
            entity.current_frame = 0
    else:
        entity.current_frame = 0  # Idle frame

def check_collision(entity1, entity2):
    return (
        entity1.x < entity2.x + entity2.width and
        entity1.x + entity1.width > entity2.x and
        entity1.y < entity2.y + entity2.height and
        entity1.y + entity1.height > entity2.y
    )

def return_x_y_for_zombie(zombie, info):
    return max(0, min(info[0] - zombie.width, zombie.x)), max(0, min(info[1] - zombie.height, zombie.y))
    
def draw_blit(animation, info):
    screen.blit(animation, info)

pygame.init()

player = characters.Player(PLAYER_START_POINT, PLAYER_START_POINT, 
    animations = [
        entities.move1_animations, 
        entities.move1_animations,
        entities.attack1_animations,
        entities.attack1_animations
    ])

zombies = [
    characters.Zombie(random.randint(0, 2000), random.randint(0, 2000), animations = entities.zombie_move1_animations) for _ in range(5)
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Last Green - Huge Forest World")
clock = pygame.time.Clock()

running = True
bullets = []

# Get mouse position on screen

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Calculate direction to mouse
                mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()

                mouse_features = mousefeatures.MouseFeatures(mouse_screen_x, mouse_screen_y, player)
                bx, by, bdir_x, bdir_y = mouse_features.get_mouse_direction()
                bullet = characters.Bullet(bx, by, bdir_x, bdir_y, speed=12, max_distance=400)
                bullets.append(bullet)

    keys = pygame.key.get_pressed()
    mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
    
    player.move(keys)

    # Update player movement and direction
    entity_moving(player, player.animation_speed, player.frame_limit)

    # ----- WORLD BOUNDARIES (keep player inside world) -----
    player.x, player.y = max(0, min(WORLD_WIDTH - player.width, player.x)), max(0, min(WORLD_HEIGHT - player.height, player.y))

    # Update Zombies AI and movement
    for zombie in zombies:
        zombie.zombie_AI_chasing(player)
        entity_moving(zombie, zombie.animation_speed, zombie.frame_limit)
        # Update zombie boundaries (stay in world)
        zombie.x, zombie.y = return_x_y_for_zombie(zombie, [WORLD_WIDTH, WORLD_HEIGHT])

    # Update bullets and remove expired ones
    for bullet in bullets[:]:  # [:] creates a copy for safe removal
        if bullet.update():  # Returns True if max distance reached
            bullets.remove(bullet)

    ##### Camera follows player #####
    # Update camera (follow player)
    player.update_camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)

    # Get player's screen position
    screen_player_x, screen_player_y = player.get_screen_position()

    mouse_world_x, mouse_world_y = player.camera_x + mouse_screen_x, player.camera_y + mouse_screen_y

    # 1. Background (clears screen)
    # screen.fill((48, 158, 75))
    screen.fill((0, 0, 0))

    ### The main objects here
    map_tile_1  = entities.PyzombieImageComponent("./assets/tileset.png", screen)

    all_map_tiles = []
    all_map_tiles.append(map_tile_1)

    game_map = map.Map()
    game_map.create_map(player, all_map_tiles)

    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen, player.camera_x, player.camera_y)
        # Draw line from player to mouse (aiming line)
        mouse_screen_x, mouse_screen_y = pygame.mouse.get_pos()
        player_screen_x = player.x - player.camera_x
        player_screen_y = player.y - player.camera_y
        # pygame.draw.line(screen, (255, 255, 255), 
        #          (player_screen_x + player.width//2, player_screen_y + player.height//2),
        #          (mouse_screen_x, mouse_screen_y), 2)

    # 2. Draw Player
    pygame.draw.rect(screen, (139, 69, 19), (screen_player_x, screen_player_y, player.width, player.height))
    draw_blit(player.move0[player.direction][int(player.current_frame)], (screen_player_x - player.width * 4, screen_player_y - player.height * 3))

    # 3. Draw Zombies
    for zombie in zombies:

        screen_zombie_x, screen_zombie_y = player.world_to_screen(zombie.x, zombie.y)
        pygame.draw.rect(screen, (139, 69, 19), (screen_zombie_x, screen_zombie_y, zombie.width, zombie.height))
        draw_blit(zombie.animations[zombie.direction][int(zombie.current_frame)], (screen_zombie_x - zombie.width, screen_zombie_y - zombie.height ))

    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()