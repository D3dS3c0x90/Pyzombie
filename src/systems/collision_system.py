# src/systems/collision_system.py
"""
⚔️ COLLISION SYSTEM
دلوقتي بنستخدم pygame.sprite.spritecollide / groupcollide بدل اللوبات اليدوية
القديمة في central_managment.py. الفرق الأساسي إن الـ Groups بقت "تعرف" تتفاعل
مع بعضها بسطر واحد بدل for loop كامل.
"""
import pygame
import src.assets_manager as assets


def bullet_zombies_collision(bullets_group, zombies_group, player):
    events = []
    hits = pygame.sprite.groupcollide(bullets_group, zombies_group, False, False)

    for bullet, zombies in hits.items():
        for zombie in zombies:
            if zombie.is_dead:
                continue
            zombie.health -= bullet.damage
            zombie_died = zombie.health <= 0
            if zombie_died:
                player.coins += 1
                zombie.is_dead = True

            events.append({
                "bullet": bullet,
                "zombie": zombie,
                "zombie_died": zombie_died,
            })
            bullet.traveled = bullet.max_dist  
            break 

    return events

def player_zombie_collision(player, zombie):
    zombie.update_damage_rect()
    
    if player.rect.colliderect(zombie.damage_rect) and not zombie.is_dead:
        
        if zombie.x < player.x:
            zombie.x -= 2
        else:
            zombie.x += 2 
            
        if zombie.y < player.y:
            zombie.y -= 2  
        else:
            zombie.y += 2 
        zombie.update_rect()
        
        if int(zombie.delay) == 1:
            player.health_system(entity=zombie)
            zombie.delay = 0
            return True
            
        zombie.delay += zombie.step_delay
        
    else:
        zombie.delay = zombie.step_delay
        
    return False

def zombie_zombie_collision(zombie, zombies_group):
    if zombie.is_dead:
        return

    zombie.update_rect()
    
    for current_zombie in zombies_group:
        if current_zombie == zombie or current_zombie.is_dead:
            continue
        
        current_zombie.update_rect()
        
        if zombie.rect.colliderect(current_zombie.rect) and current_zombie.is_dead == False:
            if current_zombie.x < zombie.x:
                current_zombie.x -= 1 
            else:
                current_zombie.x += 1 
                
            if current_zombie.y < zombie.y:
                current_zombie.y -= 1 
            else:
                current_zombie.y += 1 
    zombie.update_rect()

def player_item_collision(item, player):
    if item.rect.colliderect(player.rect):
        item.is_taked = True
        if item.type in ["RifleAmmo", "Auto"]:
            player.weapon_ammo_count += item.amount
        elif item.type == "Health":
            player.health_system(health=item.amount)
        return True
    return False

def bullet_tree_collision(bullets_group, trees_group):
    """بيقتل (kill) أي رصاصة اتصدمت بشجرة ويرجع اللستة اللي اتقتلت."""
    hit_bullets = list(pygame.sprite.groupcollide(bullets_group, trees_group, True, False).keys())
    return hit_bullets

def player_enteract(player, collision_rect, col_type, screen, keys):
    for col in collision_rect:
        if player.rect.colliderect(col):
            if col_type == "Store":
                # buy_health(player)
                # player.pay(25)
                return (True, "Store")
            elif col_type == "Dealler":
                return (True, "Dealler")
    return (False, None)
   
def player_enter_exit(player, door_rect_in, door_rect_out, notifications_list, alert_list=[], keys=None, amount=0, delay=None):
    pressed_key = keys[pygame.K_e]
    delay.pressed = False if delay.delay() else delay.pressed
    if player.rect.colliderect(door_rect_in):
        notifications_list.append([player.check_in_gate_notification(amount)])
        if pressed_key:
            pay_dessision = player.pay(amount)
            if pay_dessision:
                player.x += 350
            else:
                if delay.pressed == False:
                    alert_list.append(player.player_alert("Insufficient", assets.sprites["coins_2"]))
                    delay.pressed = True

    if player.rect.colliderect(door_rect_out):
        notifications_list.append([player.check_out_gate_notification()])
        if pressed_key:
            player.x -= 350 
        
    player.update_rect()
    
def buy_health(player):
    player.health_system(health=25)