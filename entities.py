import pygame
import entities

all_trees_png_1 = pygame.image.load("./assets/Trees1.png")
all_trees_png_2 = pygame.image.load("./assets/Trees2.png")
all_tileset_png = pygame.image.load("./assets/Tileset.png")

tree_1 = all_trees_png_1.subsurface((0, 0, 80, 160))
tree_1 = pygame.transform.scale(tree_1, (120, 240)) 

boush_1 = all_trees_png_1.subsurface((185, 75, 50, 50))
boush_1 = pygame.transform.scale(boush_1, (80, 80))

boush_2 = all_trees_png_1.subsurface((190, 130, 40, 40))
boush_2 = pygame.transform.scale(boush_2, (80, 80))

# Player Movies
player_move_png = pygame.image.load("assets/CrouchRun.png")     

# Player Attacks
player_attack_png = pygame.image.load("assets/Attack1.png")   

# Zombie Movies
zombie_move1_png = pygame.image.load("assets/zombie.png")    

total_columns = 36
total_rows = 8

# Change this to change player size (for better visibility)
PLAYER_SIZE = 200
# 1792 x 1024 (14 frames, 8 directions) 
move1_animations = {
    "right": [pygame.transform.scale(entities.player_move_png.subsurface((i * 128, 0, 128, 128)), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(14)],
    "down_right": [pygame.transform.scale(entities.player_move_png.subsurface((i * 128, 128, 128, 128)), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(14)],
    "down": [pygame.transform.scale(entities.player_move_png.subsurface((i * 128, 256, 128, 128)), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(14)],
    "down_left": [pygame.transform.scale(entities.player_move_png.subsurface((i * 128, 384, 128, 128)), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(14)],
    "left": [pygame.transform.scale(entities.player_move_png.subsurface((i * 128, 512, 128, 128)), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(14)],
    "up_left": [pygame.transform.scale(entities.player_move_png.subsurface((i * 128, 640, 128, 128)), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(14)],
    "up": [pygame.transform.scale(entities.player_move_png.subsurface((i * 128, 768, 128, 128)), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(14)],
    "up_right": [pygame.transform.scale(entities.player_move_png.subsurface((i * 128, 896, 128, 128)), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(14)],
}

zombie_move1_animations = {
    "down_left": [entities.zombie_move1_png.subsurface(((i + 4) * 125, 0, 125, 120)) for i in range(8)],
    "left": [entities.zombie_move1_png.subsurface(((i + 4) * 125, 125, 110, 125)) for i in range(8)],
    "up_left": [entities.zombie_move1_png.subsurface(((i + 4) * 125, 250, 125, 120)) for i in range(8)],
    "up": [entities.zombie_move1_png.subsurface(((i + 4) * 125, 375, 125, 120)) for i in range(8)],
    "up_right": [entities.zombie_move1_png.subsurface(((i + 4) * 125, 500 , 125, 120)) for i in range(8)],
    "right": [entities.zombie_move1_png.subsurface(((i + 4) * 125, 625, 125, 120)) for i in range(8)],
    "down_right": [entities.zombie_move1_png.subsurface(((i + 4) * 125, 750, 125, 120)) for i in range(8)],
    "down": [entities.zombie_move1_png.subsurface(((i + 4) * 125, 875, 125, 120)) for i in range(8)],
}

# 1792 x 1024 (14 frames, 8 directions) 
attack1_animations = {
    "down": [entities.player_attack_png.subsurface((i * 128, 0, 128, 128)) for i in range(14)],
    "down_right": [entities.player_attack_png.subsurface((i * 128, 128, 128, 128)) for i in range(14)],
    "right": [entities.player_attack_png.subsurface((i * 128, 256, 128, 128)) for i in range(14)],
    "up_right": [entities.player_attack_png.subsurface((i * 128, 384, 128, 128)) for i in range(14)],
    "up": [entities.player_attack_png.subsurface((i * 128, 512, 128, 128)) for i in range(14)],
    "up_left": [entities.player_attack_png.subsurface((i * 128, 640, 128, 128)) for i in range(14)],
    "left": [entities.player_attack_png.subsurface((i * 128, 768, 128, 128)) for i in range(14)],
    "down_left": [entities.player_attack_png.subsurface((i * 128, 896, 128, 128)) for i in range(14)],
}
# Get total size
player_move_total_width = player_move_png.get_width()
player_move_total_height = player_move_png.get_height()