# src/systems/collision_system.py
"""
⚔️ COLLISION SYSTEM
دلوقتي بنستخدم pygame.sprite.spritecollide / groupcollide بدل اللوبات اليدوية
القديمة في central_managment.py. الفرق الأساسي إن الـ Groups بقت "تعرف" تتفاعل
مع بعضها بسطر واحد بدل for loop كامل.
"""
import pygame


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
            bullet.traveled = bullet.max_dist  # علّمه إنه خلص مداه
            break  # رصاصة واحدة بتضرب زومبي واحد بس، زي السلوك الأصلي

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

