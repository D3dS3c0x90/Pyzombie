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
IS_INVENTORY_OPEN = False

HEALTH_INVENTORY_OPEN = True
AMMO_INVENTORY_OPEN = False
GEAR_INVENTORY_OPEN = False

BLACK = (0, 0, 0)
ZOMBIED = "#9d7d54"
GREEN_BG = (34, 68, 34)
YELLOW = (255, 255, 0)

PIXEL_FONT = "assets/fonts/Minecraft.ttf"

WALLS = []
WHOLE_LIST = []
ACTION_LIST = []
GLOBAL_NOTIFICATIONS = []

# 0 -> in, 1 -> out, 2 -> store, 3 -> dealer
IS_COLLISIONED = [False for _ in range(4)]

BUILDINGS = {
    "Store":[],
    "Dealer":[]
}

ITEMS = {}
ITEMS_KEYS = {
    "0": None,
    "1": None,
    "2": None,
    "3": None,
    "4": None,
    "5": None,
    "6": None,
    "7": None,
    "8": None,
    "9": None,
}
