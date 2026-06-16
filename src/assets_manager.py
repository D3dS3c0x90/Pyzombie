# assets_manager.py
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

def slice_player_sheet(sheet, total_rows=8, total_cols=14, frame_w=128, frame_h=128, target_w=160, target_h=160):
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
    player_idle_png             = image_load("assets/Player/Idle.png")
    player_run_png              = image_load("assets/Player/Run.png")
    player_attack_png           = image_load("assets/Player/Attack1.png")
    player_run_attack_png       = image_load("assets/Player/RunAttack.png")
    player_run_back_png         = image_load("assets/Player/RunBackwards.png")
    player_run_back_atk_png     = image_load("assets/Player/RunBackwardsAttack.png")
    player_strafe_l_png         = image_load("assets/Player/StrafeLeft.png")
    player_strafe_l_atk_png     = image_load("assets/Player/StrafeLeftAttack.png")
    player_strafe_r_png         = image_load("assets/Player/StrafeRight.png")
    player_strafe_r_atk_png     = image_load("assets/Player/StrafeRightAttack.png")
    player_damage_png           = image_load("assets/Player/TakeDamage.png")
    
    player_state_png            = image_load("assets/Player/player_state.png")
    player_health_bar_png       = image_load("assets/Player/player_health_bar.png")
    
    # Dropped Items
    ammo_png                    = image_load("assets/Player/Dropped_Items.png")
    coins_png                   = image_load("assets/Player/Dropped_Items.png")
    health_png                  = image_load("assets/Player/Dropped_Items.png")
    
    # Zombie's dependences
    zombie_move_png             = image_load("assets/Zombie/zombie_move.png")
    zombie_die_png              = image_load("assets/Zombie/Die.png")
    zombie_health_bar_png       = image_load("assets/Zombie/zombie_health_bar.png")
    
    # Trees
    trees_png                   = image_load("assets/Trees1.png")
    
    # Crosshairs
    crosshair_png                   = image_load("assets/crosshair/fire_crosshair.png")
    
    # Blood
    blood_png                   = image_load("assets/blood/blood.png")
    
    # Safe Zone Area Dependences
    base_png                    = image_load("assets/building/safe_zone.png")
    
    # Components
    empty_bullets_png                    = image_load("assets/components/empty_bullets.png")
    
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
            row_frames.append(pygame.transform.scale(frame, (60, 60)))
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
            row_frames.append(pygame.transform.scale(frame, (60, 60)))
        all_z_move_frames[target_dir] = row_frames
    animations["zombie_move"] = all_z_move_frames

    # ==============================================================================
    # 🌲 4. SCENERY & VEGETATION TILE SET ALIGNMENTS
    # ==============================================================================
    sprites["tree_1"] = pygame.transform.scale(trees_png.subsurface((0, 0, 80, 160)), (120, 240))
    sprites["bush_1"] = pygame.transform.scale(trees_png.subsurface((185, 75, 50, 50)), (80, 80))
    sprites["bush_2"] = pygame.transform.scale(trees_png.subsurface((190, 130, 40, 40)), (80, 80))
    
    # ==============================================================================
    # 🖋️ 5. DROP ITEMS FOR PLAYER
    # ==============================================================================

    sprites["ammo"] = pygame.transform.scale(ammo_png.subsurface((192, 0, 32, 32)), (30, 30))               # start from 224 7th item
    sprites["coins_1"] = pygame.transform.scale(coins_png.subsurface((64, 0, 32, 32)), (30, 30))            # start from 64 3rd item
    sprites["coins_2"] = pygame.transform.scale(coins_png.subsurface((96, 0, 32, 32)), (30, 30))            # start from 96 4th item
    sprites["health_1"] = pygame.transform.scale(health_png.subsurface((0, 0, 32, 32)), (30, 30))           # start from 0 1st item
    sprites["health_2"] = pygame.transform.scale(health_png.subsurface((32, 0, 32, 32)), (30, 30))          # start from 32 2nd item
    
    # Player State
    sprites["player_state"] = pygame.transform.scale(player_state_png.subsurface((0, 0, player_state_png.get_width(), player_state_png.get_height())), (player_state_png.get_width(), player_state_png.get_height() + 30))                            # normal image without scalling
    
    # Crosshairs
    sprites["crosshair"] = pygame.transform.scale(crosshair_png.subsurface((0, 0, crosshair_png.get_width(), crosshair_png.get_height())), (25, 25))                            # normal image without scalling
    
    # ==============================================================================
    # 🖋️ 6. ALL SAFE ZONE DEPENDENCES
    # ==============================================================================
    
    # sprites["base"] = []
    sprites["base"] = base_png.subsurface((0, 0, base_png.get_width(), base_png.get_height()))
    
    # ==============================================================================
    # 🖋️ 7. ALL ZOMBIE HEALTH BAR CASES
    # ==============================================================================
    
    sprites["zombie_health_bar"] = []
    for col in range(12):
        sub_img = zombie_health_bar_png.subsurface((col * 36, 0, 36, 7))
        scaled_frame = pygame.transform.scale(sub_img, (80, 10)).copy()
        
        sprites["zombie_health_bar"].append(scaled_frame)
        
    # ==============================================================================
    # 🖋️ 8. ALL PLAYER HEALTH BAR CASES
    # ==============================================================================
    
    sprites["player_health_bar"] = []
    for col in range(11):
        sub_img = player_health_bar_png.subsurface((col * 224, 0, 224, 48))
        scaled_frame = pygame.transform.scale(sub_img, (180, 20)).copy()
        
        sprites["player_health_bar"].append(scaled_frame)
        
    # ==============================================================================
    # 🖋️ 9. EMPTY BULLETS CASES
    # ==============================================================================
    
    sprites["empty_bullets"] = []
    for col in range(8):
        sub_img = empty_bullets_png.subsurface((col * 16, 0, 16, 16))
        scaled_frame = pygame.transform.scale(sub_img, (8, 8)).copy()
        
        sprites["empty_bullets"].append(scaled_frame)
        
    # ==============================================================================
    # 🖋️ 9. BLOOD CASES
    # ==============================================================================
    
    sprites["blood"] = []
    for col in range(14):
        sub_img = blood_png.subsurface((col * 64, 0, 64, 64))
        scaled_frame = pygame.transform.scale(sub_img, (32, 32)).copy()
        
        sprites["blood"].append(scaled_frame)
        
    # ==============================================================================
    # 🔊 9. SOUND EFFECTS & BALLISTICS AUDIO HARD CODING
    # ==============================================================================
    sounds["fire"] = []
    sounds["no_ammo"] = []
    sounds["reload"] = []
    sounds["collect"] = []
    sounds["dead_bullets"] = []
    
    sounds["move"] = []
    
    sounds["background"] = []
    
    sounds["coins"] = []
    sounds["ammo"] = []
    sounds["health"] = []
    
    musics["background"] = []
    
    # Load primary action sounds safely
    sounds["no_ammo"].append(pygame.mixer.Sound("assets/sounds/no_ammo/no_ammo.ogg"))
    
    sounds["ammo"].append(pygame.mixer.Sound("assets/sounds/weapon/collect.ogg"))
    
    sound = pygame.mixer.Sound("assets/sounds/bags/health.ogg")
    sound.set_volume(0.3)
    sounds["health"].append(sound)
    
    # Footstep directory loop trackers
    for move_sound_path in get_path_files("assets/sounds/footsteps"):
        sound = pygame.mixer.Sound(str(move_sound_path))
        sound.set_volume(0.2)
        sounds["move"].append(sound)
    
    # Coins sound arrays 
    for coins_sound_path in get_path_files("assets/sounds/coins"):
        sound = pygame.mixer.Sound(str(coins_sound_path))
        sound.set_volume(0.2)
        sounds["coins"].append(sound)
        
    # Firing sound arrays 
    for firing_sound_path in get_path_files("assets/sounds/firing/rifle"):
        sound = pygame.mixer.Sound(str(firing_sound_path))
        sound.set_volume(0.3)
        sounds["fire"].append(sound)
        
    # Reload sound arrays 
    for reload_sound_path in get_path_files("assets/sounds/reload"):
        sound = pygame.mixer.Sound(str(reload_sound_path))
        sound.set_volume(0.3)
        sounds["reload"].append(sound)
        
    # Dead Bullets sound arrays 
    for dead_bullets_sound_path in get_path_files("assets/sounds/dead_bullet"):
        sound = pygame.mixer.Sound(str(dead_bullets_sound_path))
        sound.set_volume(0.8)
        sounds["dead_bullets"].append(sound)
        
    # Background sound arrays 
    for background_sound_path in get_path_files("assets/sounds/background"):
        sound = pygame.mixer.Sound(str(background_sound_path))
        sound.set_volume(0.8)
        sounds["background"].append(sound)
        
    # Health sound arrays 
    # for health_sound_path in get_path_files("assets/sounds/bags"):
    #     sounds["health"].append(pygame.mixer.Sound(str(health_sound_path)))
    
    # Keep background soundtracks as standard paths for streaming chunks
    for background_path in get_path_files("assets/waves/horror"):
        musics["background"].append(str(background_path))
        
