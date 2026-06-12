import pygame
# ==============================================================================
# 🎮 LAST GREEN - GLOBAL CONFIGURATION MATRIX
# ==============================================================================
# This file holds all our immutable game constants. Changing these values 
# modifies the entire game state without messing up core mechanics.

# 📺 Battleground Resolution (Window Dimensions)
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 830
# SCREEN_WIDTH = 760
# SCREEN_HEIGHT = 830

MUSIC_ENDED_EVENT = pygame.USEREVENT + 1

# 🗺️ The Infinite Dread (World Map Boundary Constraints)
# The player can explore deep into this 5000x5000 pixel vector space.
WORLD_WIDTH = 5000
WORLD_HEIGHT = 5000

# ⚡ Engine Diagnostics
FPS = 60  # Frames Per Second (The heartbeat of our loop)
FRAME_NOW = 0 # Frames at this moment
PLAYER_START_POINT = WORLD_WIDTH // 2  # Drop zone right in the center of the map

# 🎨 Apocalypse Palette (RGB Triplets)
BLACK = (0, 0, 0)
GREEN_BG = (34, 68, 34)  # Overgrown forest grass tone
YELLOW = (255, 255, 0)    # Tracer bullet color

PIXEL_FONT = "assets/fonts/Minecraft.ttf"

ZOMBIE_ID, BULLET_ID = 0, 0

DEBUGGER = {
    "p_ammo":[None, None, None, None, None],
    "p_move":"IDLE",
    "p_health":100,
    "p_position_x":PLAYER_START_POINT,
    "p_position_y":PLAYER_START_POINT,
    "mouse_position_x":PLAYER_START_POINT,
    "mouse_position_y":PLAYER_START_POINT,
    "bullet_direction":"None",
    "zombie_tree_collision":[None, None],
    "zombie_zombie_collision":[None, None],
    "zombie_zombie_collision":[None, None],
    "bullet_zombie_collision":[None, None, None],
    "zombie_create":"None",
    "zombie_removed":"None",
    "dropped_item":"None",
    "get_item":"None",
}