import pygame

# 🎒 THE GLOBAL INVENTORY (Asset Caches)
# These dictionaries hold our textures in RAM so we never fetch from disk during gameplay.
animations = {}
sprites = {}

def image_load(image_path):
    return pygame.image.load(image_path).convert_alpha()

def load_all_assets():
    """
    💿 ASSET PIPELINE INITIALIZATION
    Loads texture atlases and slices up animation sheets before the engine turns over.
    This prevents mid-game micro-stutters and maximizes performance.
    """
    global animations, sprites
        
    # 📥 Load raw image files from the assets bunker
    # .convert_alpha() optimizes the image formats for blitting with transparency.
    player_move_png = image_load("assets/CrouchRun.png")
    player_attack_png = image_load("assets/Attack1.png")
    zombie_move_png = image_load("assets/zombie.png")
    trees_png = image_load("assets/Trees1.png")

    # ✂️ SURVIVOR MOVEMENT SPRITE-SHEET SLICING
    # The sheet is built out of 8 rows (directions) and 14 columns (frames per action).
    all_frames = {}
    for row in range(8):
        row_frames = []
        for col in range(14):
            # .subsurface isolates a clean bounding box inside the sprite sheet atlas
            frame = player_move_png.subsurface((col * 128, row * 128, 128, 128))
            # Scale up the frame so our survivor doesn't look like an ant on high-res monitors
            row_frames.append(pygame.transform.scale(frame, (200, 200)))
        all_frames[row] = row_frames

    # Map raw rows to semantic movement directions
    animations["player_move"] = {
        "right": all_frames[0], "down_right": all_frames[1], "down": all_frames[2],
        "down_left": all_frames[3], "left": all_frames[4], "up_left": all_frames[5],
        "up": all_frames[6], "up_right": all_frames[7]
    }

    # 🧟 UNDEAD MOVEMENT SPRITE-SHEET SLICING
    # Slices 8 animation directions for the zombie horde.
    animations["zombie_move"] = {
        "down_left": [zombie_move_png.subsurface(((i + 4) * 125, 0, 125, 120)) for i in range(8)],
        "left": [zombie_move_png.subsurface(((i + 4) * 125, 125, 110, 125)) for i in range(8)],
        "up_left": [zombie_move_png.subsurface(((i + 4) * 125, 250, 125, 120)) for i in range(8)],
        "up": [zombie_move_png.subsurface(((i + 4) * 125, 375, 125, 120)) for i in range(8)],
        "up_right": [zombie_move_png.subsurface(((i + 4) * 125, 500, 125, 120)) for i in range(8)],
        "right": [zombie_move_png.subsurface(((i + 4) * 125, 625, 125, 120)) for i in range(8)],
        "down_right": [zombie_move_png.subsurface(((i + 4) * 125, 750, 125, 120)) for i in range(8)],
        "down": [zombie_move_png.subsurface(((i + 4) * 125, 875, 125, 120)) for i in range(8)],
    }

    # 🌲 THE VEGETATION SHIELD
    # Slices environment tiles. We scale them to give them an imposing, dense presence.
    sprites["tree_1"] = pygame.transform.scale(trees_png.subsurface((0, 0, 80, 160)), (120, 240))
    sprites["bush_1"] = pygame.transform.scale(trees_png.subsurface((185, 75, 50, 50)), (80, 80))
    sprites["bush_2"] = pygame.transform.scale(trees_png.subsurface((190, 130, 40, 40)), (80, 80))
    