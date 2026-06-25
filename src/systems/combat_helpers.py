# src/systems/combat_helpers.py
import math
import random
import src.assets_manager as assets


def get_angle(dx, dy):
    angle = math.atan2(-dy, dx)
    degrees = math.degrees(angle)
    if degrees < 0:
        degrees += 360

    if 22.5 <= degrees < 67.5:
        direction = "up_right"
    elif 67.5 <= degrees < 112.5:
        direction = "up"
    elif 112.5 <= degrees < 157.5:
        direction = "up_left"
    elif 157.5 <= degrees < 202.5:
        direction = "left"
    elif 202.5 <= degrees < 247.5:
        direction = "down_left"
    elif 247.5 <= degrees < 292.5:
        direction = "down"
    elif 292.5 <= degrees < 337.5:
        direction = "down_right"
    else:
        direction = "right"
    return direction

def get_sound_randomly(type, sounds):
    return sounds[type][random.randrange(0, len(sounds[type]))]

def get_music_randomly(type, musics):
    return musics[type][random.randrange(0, len(musics[type]))]

def play_sound_randomly(sfx, rand=False):
    if rand:
        if random.randint(0, 2500) < 2499:
            return
    get_sound_randomly(sfx, assets.sounds).play()

def get_random_value(choices=()):
    return random.randint(1, 101) if len(choices) == 0 else random.choice(choices)
