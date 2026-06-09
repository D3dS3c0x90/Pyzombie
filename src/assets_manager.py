import pygame
from pathlib import Path

# 🎒 THE GLOBAL INVENTORY (Asset Caches)
# These dictionaries hold our textures in RAM so we never fetch from disk during gameplay.
animations = {}
sprites = {}
sounds = {}
musics = {}
items = {}

def get_path_files(path):
    files = []
    dir = Path(path)
    if dir.exists() and dir.is_dir():
        for file in dir.iterdir():
            if file.is_file():
                files.append(file)
    return files

def image_load(image_path):
    # .convert_alpha() optimizes the image formats for blitting with transparency.
    return pygame.image.load(image_path).convert_alpha()

def slice_player_sheet(sheet, total_rows=8, total_cols=14, frame_w=128, frame_h=128, target_w=200, target_h=200):
    """
    ✂️ HELPER AUTOMATION METHOD
    Slices a standard 8-row player asset sheet and maps it directly 
    to the 8-way directional compass system used by the engine.
    """
    directions = ["right", "down_right", "down", "down_left", "left", "up_left", "up", "up_right"]
    sheet_anims = {}
    
    for row in range(min(total_rows, 8)):
        row_frames = []
        for col in range(total_cols):
            # Isolate the clean bounding box inside the atlas
            rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
            frame = sheet.subsurface(rect)
            # Scale up so characters are highly visible on screen
            row_frames.append(pygame.transform.scale(frame, (target_w, target_h)))
        
        # Assign the list of frames to its specific compass direction key
        direction_key = directions[row]
        sheet_anims[direction_key] = row_frames
        
    return sheet_anims

def load_all_assets():
    """
    CD ASSET PIPELINE INITIALIZATION
    Loads texture atlases and slices up animation sheets before the engine turns over.
    This prevents mid-game micro-stutters and maximizes performance.
    """
    global animations, sprites, musics, sounds, items
        
    # ==============================================================================
    # 📥 1. LOAD RAW TEXTURES FROM THE FILESYSTEM BUNKERS
    # ==============================================================================
    # Core Player Sheets (New Expanded Action Sets)
    player_idle_png             = image_load("assets/Idle.png")
    player_run_png              = image_load("assets/Run.png")
    player_attack_png           = image_load("assets/Attack1.png")
    player_run_attack_png       = image_load("assets/RunAttack.png")
    player_run_back_png         = image_load("assets/RunBackwards.png")
    player_run_back_atk_png     = image_load("assets/RunBackwardsAttack.png")
    player_strafe_l_png         = image_load("assets/StrafeLeft.png")
    player_strafe_l_atk_png     = image_load("assets/StrafeLeftAttack.png")
    player_strafe_r_png         = image_load("assets/StrafeRight.png")
    player_strafe_r_atk_png     = image_load("assets/StrafeRightAttack.png")
    player_damage_png           = image_load("assets/TakeDamage.png")
    
    # Dropped Items
    ammo_png                    = image_load("assets/Dropped_Items.png")
    money                       = image_load("assets/Dropped_Items.png")
    health_png                  = image_load("assets/Dropped_Items.png")
    
    # Opposition & Environment Atlases
    # zombie_move_png             = image_load("assets/zombie.png")
    zombie_move_png             = image_load("assets/zombie_move.png")
    zombie_die_png              = image_load("assets/Die.png")
    trees_png                   = image_load("assets/Trees1.png")
    
    # ==============================================================================
    # ✂️ 2. GENERATE UNIFIED PLAYER ANIMATION DICTIONARY MAPS
    # ==============================================================================
    # We pass each loaded atlas sheet straight into our clean slicing machine wrapper
    animations["Idle"]               = slice_player_sheet(player_idle_png, total_cols=14)
    animations["Run"]                = slice_player_sheet(player_run_png, total_cols=14)
    animations["Attack1"]            = slice_player_sheet(player_attack_png, total_cols=14)
    animations["RunAttack"]          = slice_player_sheet(player_run_attack_png, total_cols=14)
    animations["RunBackwards"]       = slice_player_sheet(player_run_back_png, total_cols=14)
    animations["RunBackwardsAttack"] = slice_player_sheet(player_run_back_atk_png, total_cols=14)
    animations["StrafeLeft"]         = slice_player_sheet(player_strafe_l_png, total_cols=14)
    animations["StrafeLeftAttack"]   = slice_player_sheet(player_strafe_l_atk_png, total_cols=14)
    animations["StrafeRight"]        = slice_player_sheet(player_strafe_r_png, total_cols=14)
    animations["StrafeRightAttack"]  = slice_player_sheet(player_strafe_r_atk_png, total_cols=14)
    animations["TakeDamage"]         = slice_player_sheet(player_damage_png, total_cols=14)

    # ==============================================================================
    # 🧟 3. SLICE THREAT MATRIX ASSET PACKS (Zombies)
    # ==============================================================================
    # Zombie Death Slicing Configuration (8 rows by 8 frames)
    all_z_die_frames = {}
    z_directions = ["right", "down_right", "down", "down_left", "left", "up_left", "up", "up_right"]
    z_row_mapping = [5, 6, 7, 0, 1, 2, 3, 4]  # Slices matching old custom atlas design allocations
    
    for row_idx, target_dir in enumerate(z_directions):
        row_frames = []
        source_row = z_row_mapping[row_idx]
        for col in range(8):
            frame = zombie_die_png.subsurface((col * 64, source_row * 64, 64, 64))
            row_frames.append(pygame.transform.scale(frame, (90, 90)))
        all_z_die_frames[target_dir] = row_frames
    animations["zombie_die"] = all_z_die_frames
    
    
    # Zombie Walk Slicing configurations (8 rows by 8 frames)
    all_z_move_frames = {}
    z_directions = ["right", "down_right", "down", "down_left", "left", "up_left", "up", "up_right"]
    z_row_mapping = [5, 6, 7, 0, 1, 2, 3, 4]  # Slices matching old custom atlas design allocations
    
    for row_idx, target_dir in enumerate(z_directions):
        row_frames = []
        source_row = z_row_mapping[row_idx]
        for col in range(8):
            frame = zombie_move_png.subsurface((col * 80, source_row * 64, 80, 64))
            row_frames.append(pygame.transform.scale(frame, (80, 80)))
        all_z_move_frames[target_dir] = row_frames
    animations["zombie_move"] = all_z_move_frames

    # animations["zombie_move"] = {
    #     "down_left":  [zombie_move_png.subsurface(((i + 4) * 125, 0, 125, 120)) for i in range(8)],
    #     "left":       [zombie_move_png.subsurface(((i + 4) * 125, 125, 110, 125)) for i in range(8)],
    #     "up_left":    [zombie_move_png.subsurface(((i + 4) * 125, 250, 125, 120)) for i in range(8)],
    #     "up":         [zombie_move_png.subsurface(((i + 4) * 125, 375, 125, 120)) for i in range(8)],
    #     "up_right":   [zombie_move_png.subsurface(((i + 4) * 125, 500, 125, 120)) for i in range(8)],
    #     "right":      [zombie_move_png.subsurface(((i + 4) * 125, 625, 125, 120)) for i in range(8)],
    #     "down_right": [zombie_move_png.subsurface(((i + 4) * 125, 750, 125, 120)) for i in range(8)],
    #     "down":       [zombie_move_png.subsurface(((i + 4) * 125, 875, 125, 120)) for i in range(8)],
    # }

    # ==============================================================================
    # 🌲 4. SCENERY & VEGETATION TILE SET ALIGNMENTS
    # ==============================================================================
    sprites["tree_1"] = pygame.transform.scale(trees_png.subsurface((0, 0, 80, 160)), (120, 240))
    sprites["bush_1"] = pygame.transform.scale(trees_png.subsurface((185, 75, 50, 50)), (80, 80))
    sprites["bush_2"] = pygame.transform.scale(trees_png.subsurface((190, 130, 40, 40)), (80, 80))
    
    # ==============================================================================
    # 🖋️ 5. SCENERY & VEGETATION TILE SET ALIGNMENTS
    # ==============================================================================

    sprites["ammo"] = pygame.transform.scale(ammo_png.subsurface((192, 0, 32, 32)), (30, 30))            # start from 224 7th item
    sprites["health_1"] = pygame.transform.scale(health_png.subsurface((0, 0, 32, 32)), (30, 30))        # start from 0 1st item
    sprites["health_2"] = pygame.transform.scale(health_png.subsurface((32, 0, 32, 32)), (30, 30))       # start from 32 2nd item

    # ==============================================================================
    # 🔊 6. SOUND EFFECTS & BALLISTICS AUDIO HARD CODING
    # ==============================================================================
    sounds["move"] = []
    sounds["fire"] = []
    sounds["no_ammo"] = []
    sounds["reload"] = []
    sounds["crow"] = []
    musics["background"] = []
    
    # Load primary action sounds safely
    sounds["fire"].append(pygame.mixer.Sound("assets/sounds/weapon/firing.ogg"))
    sounds["no_ammo"].append(pygame.mixer.Sound("assets/sounds/weapon/no_ammo.ogg"))
    sounds["reload"].append(pygame.mixer.Sound("assets/sounds/weapon/reload.ogg"))
    
    # Footstep directory loop trackers
    for move_sound_path in get_path_files("assets/sounds/footsteps"):
        sounds["move"].append(pygame.mixer.Sound(str(move_sound_path)))
        
    # Ambient sound arrays 
    for crow_sound_path in get_path_files("assets/sounds/crow"):
        sounds["crow"].append(pygame.mixer.Sound(str(crow_sound_path)))
    
    # Keep background soundtracks as standard paths for streaming chunks
    for background_path in get_path_files("assets/waves/horror"):
        musics["background"].append(str(background_path))