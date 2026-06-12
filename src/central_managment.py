from src.settings import *
import src.assets_manager as assets
import math
import random


def bullet_zombie_collision(bullet, zombies, player):
    for zombie in zombies:
        if zombie.rect.colliderect(bullet.rect) and zombie.is_dead == False:
            zombie.health -= bullet.damage
            if zombie.health <= 0:
                player.coins += 1
            return {
                "zombie_damage":True,
                "bullet_die":True,
                "bullet_damage":bullet.damage,
                "zombie_die":True,
                "zombie":zombie
            }
    return {
        "bullet_die":False,
    }

def player_zombie_collision(player, zombie):
    zombie.update_damage_rect()
    if player.rect.colliderect(zombie.damage_rect) and zombie.is_dead == False:
        if int(zombie.delay) == 1:
            player.health_system(entity=zombie)
            zombie.delay = 0
            return True
        else:
            zombie.delay += zombie.step_delay
    else:
        zombie.delay = zombie.step_delay
        return False
    
def player_item_collision(item, player):
    if item.rect.colliderect(player.rect):
        item.is_taked = True
        if item.type in ["SniperAmmo", "Auto"]:
            player.weapon_ammo_count += item.amount
        elif item.type == "Health" :
            player.health_system(health=item.amount)
        return True
    return False
    
def bullet_tree_collision(bullet, trees):
    for tree in trees:
        if tree.rect.colliderect(bullet.rect):
            return {
                "bullet_die":True,
            }
    return {
        "bullet_die":False,
    }
    
def get_angle(dx, dy):
    # We invert dy because Pygame's Y axis goes down instead of up
    angle = math.atan2(-dy, dx)
    # Convert radians to degrees (0 to 360)
    degrees = math.degrees(angle)
    if degrees < 0:
        degrees += 360

    # 3. Compass Mapping: Map the 360° circle into 8 directional slices of 45° each
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
        direction = "right"  # Covers 337.5 to 360 and 0 to 22.5
    return direction

def get_sound_randomly(type, sounds):
    return sounds[type][random.randrange(0, len(sounds[type]))]

def get_music_randomly(type, musics):
    return musics[type][random.randrange(0, len(musics[type]))]

def play_sound_randomly(sound):
    if random.randint(0, 2500) >= 2499:
        get_sound_randomly(sound, assets.sounds).play()
 