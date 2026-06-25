# src/systems/spawn_system.py

import random
import pytmx

import src.assets_manager as assets
import src.systems.combat_helpers as combat
from src.entities.tree import Tree
from src.entities.zombie import Zombie
from src.entities.items import Health, Coins, Ammo
from src.settings import WORLD_WIDTH, WORLD_HEIGHT


def spawn_zombie(zombies_group, all_sprites_group, max_zombies=50):
    if len(zombies_group) >= max_zombies:
        return None
    zombie = Zombie(
        random.randint(0, WORLD_WIDTH - 10),
        random.randint(0, WORLD_HEIGHT - 10),
        assets.animations["zombie_move"],
        assets.animations["zombie_die"],
        all_sprites_group,
        zombies_group,
    )
    return zombie

def cleanup_oldest_dead_zombie(zombies_group, min_count=10):
    zombies = list(zombies_group)
    if len(zombies) >= min_count and zombies and zombies[0].is_dead:
        zombies[0].kill()

def maybe_drop_item(zombie, items_group, all_sprites_group, item_counter):
    random_value = combat.get_random_value()

    item = None
    if random_value >= 90:
        item = Health(zombie.x, zombie.y,
                      assets.sprites[random.choice(["health_1", "health_2"])],
                      "Health", all_sprites_group, items_group)
    elif random_value >= 70:
        item = Coins(zombie.x, zombie.y,
                     assets.sprites[random.choice(["coins_1", "coins_2"])],
                     random.randrange(10, 18), "Coins",
                     all_sprites_group, items_group)
    elif random_value >= 45:
        item = Ammo(zombie.x, zombie.y,
                    assets.sprites["ammo"],
                    random.randrange(12, 18), "RifleAmmo",
                    all_sprites_group, items_group)

    if item:
        item.set_name_id(item.type, item_counter)
        item_counter += 1

    return item, item_counter

def spawn_trees_from_map(tiled_map, trees_group):
    for layer in tiled_map.tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "trees":
            for obj in layer:
                Tree(obj.x, obj.y, assets.sprites["tree_1"], trees_group) 
