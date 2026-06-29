# settings.py
import pygame
# ==============================================================================
# 🎮 LAST GREEN - GLOBAL CONFIGURATION MATRIX
# ==============================================================================

WORLD_WIDTH = 4968
WORLD_HEIGHT = 4968

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 830

PLAYER_START_POINT = WORLD_WIDTH // 2

MUSIC_ENDED_EVENT = pygame.USEREVENT + 1

FPS = 60
COUNTER = 1

BLACK = (0, 0, 0)
ZOMBIED = "#9d7d54"
GREEN_BG = (34, 68, 34)
YELLOW = (255, 255, 0)

PIXEL_FONT = "assets/fonts/Minecraft.ttf"

WALLS = []

BUILDINGS = {
    "Store":[],
    "Dealler":[]
}