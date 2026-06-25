# src/assets_manager.py
import pygame
from pathlib import Path

# 🎒 الكاش العام - في الرامات طول وقت تشغيل اللعبة
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
    return pygame.image.load(image_path).convert_alpha()


def slice_player_sheet(sheet, total_rows=8, total_cols=14, frame_w=128, frame_h=128, target_w=180, target_h=180):
    directions = ["right", "down_right", "down", "down_left", "left", "up_left", "up", "up_right"]
    sheet_anims = {}
    for row in range(min(total_rows, 8)):
        row_frames = []
        for col in range(total_cols):
            rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
            frame = sheet.subsurface(rect)
            row_frames.append(pygame.transform.scale(frame, (target_w, target_h)))
        sheet_anims[directions[row]] = row_frames
    return sheet_anims


def _slice_zombie_sheet(sheet, frame_w, frame_h, target_size=(60, 60)):
    directions = ["right", "down_right", "down", "down_left", "left", "up_left", "up", "up_right"]
    row_mapping = [5, 6, 7, 0, 1, 2, 3, 4]
    result = {}
    for row_idx, target_dir in enumerate(directions):
        source_row = row_mapping[row_idx]
        row_frames = []
        for col in range(8):
            frame = sheet.subsurface((col * frame_w, source_row * frame_h, frame_w, frame_h))
            row_frames.append(pygame.transform.scale(frame, target_size))
        result[target_dir] = row_frames
    return result


def load_player_assets():
    sheets = {
        "Idle":               "assets/Player/Idle.png",
        "Run":                "assets/Player/Run.png",
        "Attack1":            "assets/Player/Attack1.png",
        "RunAttack":          "assets/Player/RunAttack.png",
        "RunBackwards":       "assets/Player/RunBackwards.png",
        "RunBackwardsAttack": "assets/Player/RunBackwardsAttack.png",
        "StrafeLeft":         "assets/Player/StrafeLeft.png",
        "StrafeLeftAttack":   "assets/Player/StrafeLeftAttack.png",
        "StrafeRight":        "assets/Player/StrafeRight.png",
        "StrafeRightAttack":  "assets/Player/StrafeRightAttack.png",
        "TakeDamage":         "assets/Player/TakeDamage.png",
    }
    for key, path in sheets.items():
        animations[key] = slice_player_sheet(image_load(path), total_cols=14)

    player_state_png = image_load("assets/Player/player_state.png")
    sprites["player_state"] = pygame.transform.scale(
        player_state_png, (player_state_png.get_width(), player_state_png.get_height() + 30)
    )

    player_health_bar_png = image_load("assets/Player/player_health_bar.png")
    sprites["player_health_bar"] = [
        pygame.transform.scale(player_health_bar_png.subsurface((col * 224, 0, 224, 48)), (180, 20)).copy()
        for col in range(11)
    ]


def load_dropped_item_assets():

    dropped_png = image_load("assets/Player/Dropped_Items.png")
    sprites["ammo"] = pygame.transform.scale(dropped_png.subsurface((192, 0, 32, 32)), (30, 30))
    sprites["coins_1"] = pygame.transform.scale(dropped_png.subsurface((64, 0, 32, 32)), (30, 30))
    sprites["coins_2"] = pygame.transform.scale(dropped_png.subsurface((96, 0, 32, 32)), (30, 30))
    sprites["health_1"] = pygame.transform.scale(dropped_png.subsurface((0, 0, 32, 32)), (30, 30))
    sprites["health_2"] = pygame.transform.scale(dropped_png.subsurface((32, 0, 32, 32)), (30, 30))


def load_zombie_assets():

    zombie_move_png = image_load("assets/Zombie/zombie_move.png")
    zombie_die_png = image_load("assets/Zombie/Die.png")

    animations["zombie_die"] = _slice_zombie_sheet(zombie_die_png, 64, 64, (70, 70))
    animations["zombie_move"] = _slice_zombie_sheet(zombie_move_png, 80, 64, (70, 70))

    zombie_health_bar_png = image_load("assets/Zombie/zombie_health_bar.png")
    sprites["zombie_health_bar"] = [
        pygame.transform.scale(zombie_health_bar_png.subsurface((col * 36, 0, 36, 7)), (70, 10)).copy()
        for col in range(12)
    ]


def load_scenery_assets():
    # trees_png = image_load("assets/Trees1.png")
    sprites["tree_1"] = pygame.transform.scale(image_load("assets/\decorations/tree_1.png").subsurface((0, 0, 112, 192)), (120, 240))
    # sprites["bush_1"] = pygame.transform.scale(trees_png.subsurface((185, 75, 50, 50)), (80, 80))
    # sprites["bush_2"] = pygame.transform.scale(trees_png.subsurface((190, 130, 40, 40)), (80, 80))


def load_misc_assets():
    crosshair_png = image_load("assets/crosshair/fire_crosshair.png")
    sprites["crosshair"] = pygame.transform.scale(crosshair_png, (25, 25))

    base_png = image_load("assets/building/SafeZone_1.png")
    sprites["base"] = base_png.subsurface(0, 0, base_png.get_width(), base_png.get_height())
    # pygame.transform.scale(base_png, (base_png.get_width() - 300, base_png.get_height() - 300))

    empty_bullets_png = image_load("assets/components/empty_bullets.png")
    sprites["empty_bullets"] = [
        pygame.transform.scale(empty_bullets_png.subsurface((col * 16, 0, 16, 16)), (8, 8)).copy()
        for col in range(8)
    ]

    blood_png = image_load("assets/blood/blood.png")
    sprites["blood"] = [
        pygame.transform.scale(blood_png.subsurface((col * 64, 0, 64, 64)), (32, 32)).copy()
        for col in range(14)
    ]


def _load_sound_folder(path, volume=None):
    loaded = []
    for sound_path in get_path_files(path):
        sound = pygame.mixer.Sound(str(sound_path))
        if volume is not None:
            sound.set_volume(volume)
        loaded.append(sound)
    return loaded


def load_audio_assets():
    """🔊 كل المؤثرات الصوتية والموسيقى"""
    sounds["no_ammo"] = [pygame.mixer.Sound("assets/sounds/no_ammo/no_ammo.ogg")]
    sounds["ammo"] = [pygame.mixer.Sound("assets/sounds/weapon/collect.ogg")]

    health_sound = pygame.mixer.Sound("assets/sounds/bags/health.ogg")
    health_sound.set_volume(0.3)
    sounds["health"] = [health_sound]

    sounds["move"] = _load_sound_folder("assets/sounds/footsteps", volume=0.2)
    sounds["coins"] = _load_sound_folder("assets/sounds/coins", volume=0.2)
    sounds["fire"] = _load_sound_folder("assets/sounds/firing/rifle", volume=0.3)
    sounds["reload"] = _load_sound_folder("assets/sounds/reload", volume=0.3)
    sounds["dead_bullets"] = _load_sound_folder("assets/sounds/dead_bullet", volume=0.8)
    sounds["background"] = _load_sound_folder("assets/sounds/background", volume=0.8)

    musics["background"] = [str(p) for p in get_path_files("assets/waves/horror")]


def load_all_assets():
    """
    🚚 ASSET PIPELINE INITIALIZATION
    بيتنده مرة واحدة بس في بداية اللعبة. كل نوع أصول بقى في فنكشن منفصلة
    عشان لو حبيت تضيف entity جديد (مثلاً NPC) تضيف load_npc_assets() بس
    من غير ما تلمس باقي الفنكشنز.
    """
    load_player_assets()
    load_dropped_item_assets()
    load_zombie_assets()
    load_scenery_assets()
    load_misc_assets()
    load_audio_assets()
