# src/core/game.py
import math
import random
import sys

import pygame

from src.world.tiled import TiledMap
import src.assets_manager as assets
import src.systems.combat_helpers as combat
import src.systems.collision_system as collisions
import src.systems.spawn_system as spawn
import src.core.just_one_time as jot
from src.core.camera import Camera
from src.entities.player import Player
from src.entities.zombie import Zombie
from src.entities.bullet import Bullet, DeadBullet
from src.ui import minimap as minimap_module
from src.ui import notification
from src.ui import inventory
from src.ui import player_state as player_state_module
from src.world.safe_zone import SafeZone
import src.core.clock as clock_and_time
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT,
    FPS, WHOLE_LIST, MUSIC_ENDED_EVENT, IS_INVENTORY_OPEN, BUILDINGS, IS_COLLISIONED, ITEMS, ACTION_LIST,
    GLOBAL_NOTIFICATIONS, HEALTH_INVENTORY_OPEN, AMMO_INVENTORY_OPEN, GEAR_INVENTORY_OPEN, CRAFTING_INVENTORY_OPEN, ITEMS_KEYS
    )

def _init_items():
    global ITEMS, WHOLE_LIST
    ITEMS = {
        "Health" : {
            "bandeg_1":{"name" : "Small Health", "amount" : 10, "image" : assets.sprites["bandeg_1"]},
            "bandeg_2":{"name" : "Normal Health", "amount" : 20, "image" : assets.sprites["bandeg_2"]},
            "bandeg_3":{"name" : "Large Health", "amount" : 30, "image" : assets.sprites["bandeg_3"]},
            "bandeg_4":{"name" : "XLarge Health", "amount" : 40, "image" : assets.sprites["bandeg_4"]},
            # {"name" : "health_3", "amount" : 35, "image" : sprites[""]},
            # {"name" : "health_4", "amount" : 50, "image" : sprites[""]},
            # {"name" : "health_5", "amount" : 80, "image" : sprites[""]},
            },
        # "Consumable" : [
        #     {"name" : "water_1", "amount" : 10, "image" : sprites[""]},
        #     {"name" : "water_2", "amount" : 20, "image" : sprites[""]},
        #     {"name" : "water_3", "amount" : 35, "image" : sprites[""]},
            
        #     {"name" : "food_1", "amount" : 10, "image" : sprites[""]},
        #     {"name" : "food_2", "amount" : 20, "image" : sprites[""]},
        #     {"name" : "food_3", "amount" : 35, "image" : sprites[""]},
        # ], 
        "Ammo" : {
            "7_62_ammo_1":{"name" : "Small 7.62", "amount" : 10, "image" : assets.sprites["7_62_ammo_1"]},
            "7_62_ammo_2":{"name" : "Normal 7.62", "amount" : 20, "image" : assets.sprites["7_62_ammo_2"]},
            "7_62_ammo_3":{"name" : "Large 7.62", "amount" : 35, "image" : assets.sprites["7_62_ammo_3"]},
            "7_62_ammo_4":{"name" : "XLarge 7.62", "amount" : 50, "image" : assets.sprites["7_62_ammo_4"]},
            # {"name" : "5.56×45mm", "amount" : 20, "image" : sprites[""]},
            # {"name" : "5.56×45mm", "amount" : 35, "image" : sprites[""]},
            
            # {"name" : "semi_ammo_1", "amount" : 40, "image" : sprites[""]},
            # {"name" : "semi_ammo_2", "amount" : 70, "image" : sprites[""]},
            # {"name" : "semi_ammo_3", "amount" : 100, "image" : sprites[""]},
            },
    }
    
    temp = []
    temp = [inventory.ListComponent(component) for component in WHOLE_LIST]
    
    WHOLE_LIST = []
    WHOLE_LIST = [component for component in temp]
        
    temp = None

class GameEngine:
    """
    THE CORE GAME CONTROLLER
    Orchestrates all subsystems: initialises entities, systems, and UI modules,
    then drives the main update/render loop. Gameplay logic lives in entities/
    and systems/; this class keeps them connected.
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Pyzombie - Survive or Die")
        self.clock = pygame.time.Clock()

        assets.load_all_assets()
        
        self.hovered_counter = [None for _ in ACTION_LIST]

        pygame.mixer.music.set_endevent(MUSIC_ENDED_EVENT)
        self._play_random_background_music()
        _init_items()
        
        self.tiled_map = TiledMap("assets/maps/main.tmx")

        self.world_width = self.tiled_map.width
        self.world_height = self.tiled_map.height

        self.all_sprites = pygame.sprite.Group()
        
        self.zombies_group = pygame.sprite.Group()
        self.trees_group = pygame.sprite.Group()
        
        self.items_group = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.dead_bullets_group = pygame.sprite.Group()
        
        self.inventory_group = pygame.sprite.Group()
        self.inventory_ammo_group = pygame.sprite.Group()
        self.inventory_health_group = pygame.sprite.Group()
        self.inventory_gear_group = pygame.sprite.Group()
        self.inventory_crafting_group = pygame.sprite.Group()

        self.minimap = minimap_module.Minimap()
        self.safezone = SafeZone(
            self.world_width - assets.sprites["base"].get_width() - 25, 0,
            assets.sprites["base"].get_width(), assets.sprites["base"].get_height(),
            image=assets.sprites["base"],
        )
        
        spawn.spawn_trees_from_map(self.tiled_map, self.trees_group)
        spawn.spawn_walls_collision(self.tiled_map)
        spawn.spawn_store_collision(self.tiled_map)
        spawn.spawn_dealer_collision(self.tiled_map)

        self.crosshair = assets.sprites["crosshair"]
        self.pointer = assets.sprites["crosshair_pointer"]
        pygame.mouse.set_visible(False)

        self.player = Player(WORLD_WIDTH - 300, 300, assets.animations, self.all_sprites)

        for _ in range(5):
            Zombie(
                random.randint(0, WORLD_WIDTH - 10),
                random.randint(0, WORLD_HEIGHT - 10),
                assets.animations["zombie_move"],
                assets.animations["zombie_die"],
                self.all_sprites, self.zombies_group,
            )
        
        self.inventory_start_x = (SCREEN_WIDTH - assets.sprites["inventory"]["Ammo"].get_width()) // 2
        self.inventory_start_y = (SCREEN_HEIGHT - assets.sprites["inventory"]["Ammo"].get_height() - 100) // 2
            
        self.item_start_x = self.inventory_start_x + 180   
        self.item_start_y = self.inventory_start_y + 75 
        
        self.inventory = {
            "Health" : inventory.Inventory(
                        self.inventory_start_x,
                        self.inventory_start_y,
                        assets.sprites["inventory"]["Health"].get_width(), assets.sprites["inventory"]["Health"].get_height(), 
                        assets.sprites["inventory"]["Health"], self.screen, []
                        ),
            "Ammo" : inventory.Inventory(
                        self.inventory_start_x,
                        self.inventory_start_y,
                        assets.sprites["inventory"]["Ammo"].get_width(), assets.sprites["inventory"]["Ammo"].get_height(), 
                        assets.sprites["inventory"]["Ammo"], self.screen, []
                        ),
            "Gear" : inventory.Inventory(
                        self.inventory_start_x,
                        self.inventory_start_y,
                        assets.sprites["inventory"]["Gear"].get_width(), assets.sprites["inventory"]["Gear"].get_height(), 
                        assets.sprites["inventory"]["Gear"], self.screen, []
                        ),
            "Crafting" : inventory.Inventory(
                        self.inventory_start_x,
                        self.inventory_start_y,
                        assets.sprites["inventory"]["Crafting"].get_width(), assets.sprites["inventory"]["Crafting"].get_height(), 
                        assets.sprites["inventory"]["Crafting"], self.screen, []
                        ),
        }
        
        self.player_info = player_state_module.PlayerState(
            self.screen, [0, SCREEN_HEIGHT - 120], [160, SCREEN_HEIGHT - 30], self.player
        )

        self.damage_indicators = []
        self.notifications = []
        self.fixed_notifications = []
        self.player_indicators = []
        self.blood = []

        self.camera = Camera()
        self.item_counter = 0
        self.global_counter = 1

        self.mx, self.my = 0, 0
        self.running = True
        
        self.delay = clock_and_time.Timer(0.25, FPS)
        self.inventory_timer = clock_and_time.Timer(0.2, FPS)
        
        self.init_items()

    def _play_random_background_music(self):
        music_track = combat.get_music_randomly("background", assets.musics)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.load(music_track)
        pygame.mixer.music.play(loops=0)
        
    def _reset_inventory_taps(self):
        global HEALTH_INVENTORY_OPEN, AMMO_INVENTORY_OPEN, GEAR_INVENTORY_OPEN, CRAFTING_INVENTORY_OPEN, IS_INVENTORY_OPEN
        IS_INVENTORY_OPEN = False
        self.player_info.selected_char = None
        
        HEALTH_INVENTORY_OPEN = False
        AMMO_INVENTORY_OPEN = False
        GEAR_INVENTORY_OPEN = False
        CRAFTING_INVENTORY_OPEN = False
        
        self.inventory["Health"].active_list = False
        self.inventory["Ammo"].active_list = False
        self.inventory["Gear"].active_list = False
        self.inventory["Crafting"].active_list = False
        
    def _inventory_preparing(self, inventory_items_group, category):
        self.inventory[category].items = inventory_items_group
        self.inventory[category].draw()   
        for item in self.inventory[category].items:
            quantity_surface = item.quantity_font.render(str(item.quantity), False, "#FFFFFF")
            quantity_shadow_surface = item.quantity_shadow_font.render(str(item.quantity), True, (0, 0, 0))
            
            self.screen.blit(quantity_shadow_surface, (item.rect.x + 3, item.rect.y + 3))
            self.screen.blit(quantity_surface, (item.rect.x + 5, item.rect.y + 5))
            
        if self.inventory[category].active_list:
            if len(inventory_items_group) > 0:
                self.screen.blit(assets.sprites["pointer"], (self.inventory[category].list_x - 8, self.inventory[category].list_y - next(iter(inventory_items_group)).rect.height - 4))
            first = 1
            y_value = 0
            self.hovered_counter = [None for _ in ACTION_LIST]
            
            # ACTION_LIST
            for i, (component, word) in enumerate(zip(WHOLE_LIST, ACTION_LIST)):
                if first:
                    component.reset()
                    self.screen.blit(component.image, (self.inventory[category].list_x - 10, self.inventory[category].list_y + 10))
                    
                    shadow_surf = self.inventory[category].selected_item.shadow_surface
                    text_surf = self.inventory[category].selected_item.text_surface
                    
                    self.screen.blit(shadow_surf, (self.inventory[category].list_x + 48, self.inventory[category].list_y + 33))
                    self.screen.blit(text_surf, (self.inventory[category].list_x + 50, self.inventory[category].list_y + 35))
                    component.rect.y = self.inventory[category].list_y + 10
                else:
                    self.screen.blit(component.image, (self.inventory[category].list_x - 10, self.inventory[category].list_y + 10 + y_value))
                    self.screen.blit(word, (self.inventory[category].list_x + 20, self.inventory[category].list_y + 10 + y_value))
                    component.rect.y = self.inventory[category].list_y + 10 + y_value
                    
                if component.rect.collidepoint(self.mx, self.my) and not first:
                    self.screen.blit(assets.sprites["hover_blood"], (self.inventory[category].list_x + 10, self.inventory[category].list_y + 10 + y_value))
                    self.hovered_counter[i] = 1
                    
                first = False
                component.rect.x = self.inventory[category].list_x - 10
                y_value += component.image.get_height()
        
    def init_items(self):
        jot.add_item_to_inventory(
            self.item_start_x, 
            self.item_start_y, 
            ITEMS["Health"]["bandeg_1"], 
            "Health", 
            self.player, 
            self.inventory_health_group, 
            self.inventory_group,
            amount=5)
        
        jot.add_item_to_inventory(
            self.item_start_x, 
            self.item_start_y, 
            ITEMS["Health"]["bandeg_2"], 
            "Health", 
            self.player, 
            self.inventory_health_group, 
            self.inventory_group,
            amount=3)
        
        jot.add_item_to_inventory(
            self.item_start_x, 
            self.item_start_y, 
            ITEMS["Health"]["bandeg_3"], 
            "Health", 
            self.player, 
            self.inventory_health_group, 
            self.inventory_group,
            amount=2)
        
        jot.add_item_to_inventory(
            self.item_start_x, 
            self.item_start_y, 
            ITEMS["Health"]["bandeg_4"], 
            "Health", 
            self.player, 
            self.inventory_health_group, 
            self.inventory_group,
            amount=1)
        
        jot.add_item_to_inventory(
            self.item_start_x, 
            self.item_start_y, 
            ITEMS["Ammo"]["7_62_ammo_1"], 
            "Ammo", 
            self.player, 
            self.inventory_ammo_group, 
            self.inventory_group,
            amount=5)
        
        jot.add_item_to_inventory(
            self.item_start_x, 
            self.item_start_y, 
            ITEMS["Ammo"]["7_62_ammo_2"], 
            "Ammo", 
            self.player, 
            self.inventory_ammo_group, 
            self.inventory_group,
            amount=3)
        
        jot.add_item_to_inventory(
            self.item_start_x, 
            self.item_start_y, 
            ITEMS["Ammo"]["7_62_ammo_3"], 
            "Ammo", 
            self.player, 
            self.inventory_ammo_group, 
            self.inventory_group,
            amount=2)
        
        jot.add_item_to_inventory(
            self.item_start_x, 
            self.item_start_y, 
            ITEMS["Ammo"]["7_62_ammo_4"], 
            "Ammo", 
            self.player, 
            self.inventory_ammo_group, 
            self.inventory_group,
            amount=1)

        
        # =================================================================
        # 🔥 PRESERVED ORIGINAL BUG AREA (As requested for manual debugging)
        # =================================================================
        for index, item in enumerate(self.inventory_group):
            if index <= 5:
                self.player_info.add_item(str(index + 2), item)
        
    def _active_inventory(self):
        if HEALTH_INVENTORY_OPEN:
            return self.inventory["Health"]
        if AMMO_INVENTORY_OPEN:
            return self.inventory["Ammo"]
        if GEAR_INVENTORY_OPEN:
            return self.inventory["Gear"]
        if CRAFTING_INVENTORY_OPEN:
            return self.inventory["Crafting"]
        return None
    
    def _set_active_tab(self, category):
        global HEALTH_INVENTORY_OPEN, GEAR_INVENTORY_OPEN, AMMO_INVENTORY_OPEN, CRAFTING_INVENTORY_OPEN
        if category == "Health":
            HEALTH_INVENTORY_OPEN = True
            AMMO_INVENTORY_OPEN = False
            GEAR_INVENTORY_OPEN = False
            CRAFTING_INVENTORY_OPEN = False
        elif category == "Ammo":
            HEALTH_INVENTORY_OPEN = False
            AMMO_INVENTORY_OPEN = True
            GEAR_INVENTORY_OPEN = False
            CRAFTING_INVENTORY_OPEN = False
        elif category == "Gear":
            HEALTH_INVENTORY_OPEN = False
            AMMO_INVENTORY_OPEN = False
            GEAR_INVENTORY_OPEN = True
            CRAFTING_INVENTORY_OPEN = False
        elif category == "Crafting":
            HEALTH_INVENTORY_OPEN = False
            AMMO_INVENTORY_OPEN = False
            GEAR_INVENTORY_OPEN = False
            CRAFTING_INVENTORY_OPEN = True
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update_game_states()
            self.render_draw_calls()
            self.clock.tick(FPS)
            combat.play_sound_randomly("background", rand=True)

        pygame.quit()
        sys.exit()

    # ==========================================================
    # 🎮 EVENTS
    # ==========================================================
    def handle_events(self):
        """Main event loop. Processes system, keyboard, and mouse inputs in a single method."""
        global ITEMS_KEYS
        
        # Define the hotbar numbers once outside the loop for better performance
        num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
        for event in pygame.event.get():
            
            # 1. Handle Window Quit & Escape Toggle
            if event.type == pygame.QUIT:
                self.running = False
                continue
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not IS_INVENTORY_OPEN:
                self.running = False
                continue

            # 2. Handle Audio & Background Music Tracking
            elif event.type == MUSIC_ENDED_EVENT:
                self._play_random_background_music()
                continue

            # 3. Handle Keyboard Inputs (Hotbar Slots & Key Releases)
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                key_name = pygame.key.name(event.key)
                
                if key_name in num_list:
                    # Reset all slots and activate the currently pressed number key
                    for key in num_list:
                        ITEMS_KEYS[key] = False
                    ITEMS_KEYS[str(key_name)] = True
                    self.selected_char = str(key_name)
                    
                    if event.type == pygame.KEYUP:
                        self.player_info.key_release = True

            # Get the currently active inventory tab state
            active_inv = self._active_inventory()

            # 4. Handle Mouse Clicks (Combat Firing & Inventory Tabs Context)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Context A: Gameplay is active -> Fire weapon
                if not IS_INVENTORY_OPEN and not (active_inv and active_inv.active_list):
                    self._try_fire()
                
                # Context B: Inventory Overlay is active -> Check tab switching clicks
                elif IS_INVENTORY_OPEN:
                    for i, tap_rect in enumerate(self.inventory["Health"].taps):
                        if tap_rect.collidepoint(event.pos):
                            self._set_active_tab(["Health", "Ammo", "Gear", "Crafting"][i])
                        
                    for key, rect in self.player_info.collisions.items():
                        if rect.collidepoint(event.pos):
                            for k in num_list:
                                ITEMS_KEYS[k] = False
                            ITEMS_KEYS[str(key)] = True
                            self.selected_char = str(key)
                            
                    self.player_info.drag_item(event.pos)

            # 5. Process Active Inventory Context Dropdowns
            if active_inv:
                active_inv.drop_down_list(event, self.hovered_counter, self.player_info.items)
                                
            # 6. Dispatch General Player Collision Event Detection
            self.player_info.collision_event_detection(event, IS_INVENTORY_OPEN)

    def _try_fire(self):
        if self.player.ammo_count <= 0:
            combat.play_sound_randomly("no_ammo")
            return

        combat.get_sound_randomly("fire", assets.sounds).play()
        self.player.firing = True
        self.player.current_frame = 0.0

        ms_x, ms_y = pygame.mouse.get_pos()
        world_mx = ms_x + self.camera.x
        world_my = ms_y + self.camera.y

        p_cx = self.player.x + self.player.width // 2
        p_cy = self.player.y + self.player.height // 2

        dx, dy = world_mx - p_cx, world_my - p_cy
        dist = math.hypot(dx, dy)
        if dist > 0:
            Bullet(p_cx, p_cy, dx / dist, dy / dist, self.all_sprites, self.bullets_group)

        self.player.ammo_count -= 1

    # ==========================================================
    # 🔄 UPDATE
    # ==========================================================
    def update_game_states(self):
        global IS_INVENTORY_OPEN, IS_COLLISIONED, HEALTH_INVENTORY_OPEN
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        self.mx, self.my = pygame.mouse.get_pos()
                
        if not self.inventory_timer.hold:
            if keys[pygame.K_e]:
                if IS_INVENTORY_OPEN:
                    if keys[pygame.K_ESCAPE] or keys[pygame.K_e]:
                        self._reset_inventory_taps()
                        HEALTH_INVENTORY_OPEN = True
                        self.hovered_counter = [None for _ in ACTION_LIST]
                elif not IS_INVENTORY_OPEN and True not in IS_COLLISIONED:
                    IS_INVENTORY_OPEN = True
                if True not in IS_COLLISIONED:
                    self.inventory_timer.pressed = True
        if keys[pygame.K_ESCAPE] and IS_INVENTORY_OPEN:
            self._reset_inventory_taps()
            HEALTH_INVENTORY_OPEN = True
        self.inventory_timer.delay()

        self.player.move(keys, trees=self.trees_group, base=self.safezone)
        if not IS_INVENTORY_OPEN:
            self.player.reload(keys, mouse)

        current_state = self.player.determine_action_state()
        self.player.update_animation(current_state)

        self._update_zombies()
        self._update_bullets()
        self._update_dead_bullets()
        self._update_items()
        self._update_floating_texts()
        self._maybe_spawn_zombie()
        
        self.fixed_notifications = []
        for _, (col_type, collision) in enumerate(BUILDINGS.items()):
            collision_hit = collisions.player_interact(self.player, collision, col_type, self.screen, keys)
            if collision_hit[0]:
                self.fixed_notifications.append([notification.FixedNotification(text=f"For {col_type} Press ", image=assets.sprites["E"]), collision_hit[1]])

        collisions.player_enter_exit(
            self.player, 
            self.safezone.door_rect_in, 
            self.safezone.door_rect_out, 
            self.fixed_notifications, 
            alert_list=self.notifications, 
            keys=keys, 
            amount=200,
            delay=self.delay,
            inventory_timer=self.inventory_timer 
            )
        self.camera.update(self.player.x, self.player.y)

    def _update_zombies(self):
        for zombie in self.zombies_group:
            zombie.update_ai(self.player, self.safezone, self.zombies_group, trees=self.trees_group)
            if collisions.player_zombie_collision(self.player, zombie):
                self.player_indicators.append(
                    notification.DamageNumber(
                        color=(100, 100, 0), lifetime=100,
                        x=self.player.x + 40, y=self.player.y + 10,
                        amount=zombie.damage,
                    )
                )
            collisions.zombie_zombie_collision(zombie, self.zombies_group)

    def _update_bullets(self):
        for bullet in list(self.bullets_group):
            expired = bullet.update()

            if (self.safezone.rect.colliderect(bullet.rect) or self.safezone.rect_e.colliderect(bullet.rect)
                    or self.safezone.rect_w.colliderect(bullet.rect) or self.safezone.rect_n.colliderect(bullet.rect)):
                expired = True

            if expired:
                bullet.kill()
                DeadBullet(self.player.x + 15, self.player.y + 5, self.all_sprites, self.dead_bullets_group)

        for event in collisions.bullet_zombies_collision(self.bullets_group, self.zombies_group, self.player):
            self._on_zombie_hit(event)

    def _on_zombie_hit(self, event):
        zombie, bullet = event["zombie"], event["bullet"]

        self.damage_indicators.append(
            notification.DamageNumber(x=zombie.x + 40, y=zombie.y + 10, amount=bullet.damage)
        )
        self.blood.append(
            (combat.get_random_value(assets.sprites["blood"]),
             zombie.x + zombie.width // 2, zombie.y + zombie.height // 2)
        )

        if event["zombie_died"]:
            item, self.item_counter = spawn.maybe_drop_item(
                zombie, self.items_group, self.all_sprites, self.item_counter
            )

        if bullet.alive():
            bullet.kill()
            DeadBullet(self.player.x + 15, self.player.y + 10, self.all_sprites, self.dead_bullets_group)

    def _update_dead_bullets(self):
        for dead_bullet in self.dead_bullets_group:
            dead_bullet.update()

    def _update_items(self):
        for item in list(self.items_group):
            if not item.is_taken and collisions.player_item_collision(item, self.player):
                item.is_taken = True
                if item.type == "Coins":
                    self.player.coins += item.amount
                    combat.play_sound_randomly("coins")
                elif item.type == "RifleAmmo":
                    combat.play_sound_randomly("ammo")
                elif item.type == "Health":
                    combat.play_sound_randomly("health")

                notify_icon = pygame.transform.scale(item.image, (30, 30))
                self.notifications.append(
                    notification.Notification(text=f"+{item.amount} {item.type} ", image=notify_icon)
                )

            if item.is_taken:
                item.kill()
            else:
                item.up_down()

    def _update_floating_texts(self):
        for indicator in self.damage_indicators[:]:
            if indicator.update():
                self.damage_indicators.remove(indicator)
        for indicator in self.player_indicators[:]:
            if indicator.update():
                self.player_indicators.remove(indicator)
        for notify in self.notifications[:]:
            if notify.update():
                self.notifications.remove(notify)

    def _maybe_spawn_zombie(self):
        if self.global_counter % (FPS * int(combat.get_random_value() * 0.5) + 1) == 0:
            spawn.spawn_zombie(self.zombies_group, self.all_sprites)
            self.global_counter = 1
        else:
            self.global_counter += 1
        spawn.cleanup_dead_zombie(self.zombies_group)

    # ==========================================================
    # 🖼️ RENDER
    # ==========================================================
    def render_draw_calls(self):
        global HEALTH_INVENTORY_OPEN
        # self.screen.fill(ZOMBIED)
        cam_x, cam_y = self.camera.x, self.camera.y
        
        self.tiled_map.draw(self.screen, cam_x, cam_y)
        self.safezone.draw(self.screen, cam_x, cam_y)        


        for zombie in self.zombies_group:
            if zombie.is_dead:
                img = zombie.get_current_image(flag="die")
                self.screen.blit(img, (zombie.x - cam_x, zombie.y - cam_y + zombie.height // 2))

        for dead_bullet in self.dead_bullets_group:
            self.screen.blit(dead_bullet.image, (dead_bullet.x - cam_x, dead_bullet.y - cam_y))

        for blood_img, bx, by in self.blood:
            self.screen.blit(blood_img, (bx - cam_x, by - cam_y))

        for zombie in self.zombies_group:
            if zombie.is_dead == False:
                img = zombie.get_current_image()
                self.screen.blit(img, (zombie.x - cam_x, zombie.y - cam_y + zombie.height // 2))
                if zombie.health != zombie.health_limit:
                    zombie.draw_health_bar(self.screen, zombie.x - cam_x - 10, zombie.y - cam_y + zombie.height // 2 - 2)
                
                # rect_draw_x = zombie.rect.x - cam_x
                # rect_draw_y = zombie.rect.y - cam_y
                
                # pygame.draw.rect(self.screen, (255,0,0), (rect_draw_x, rect_draw_y, zombie.rect.width, zombie.rect.height), 2)
                
                # zombie.update_damage_rect() 
                # damage_draw_x = zombie.damage_rect.x - cam_x
                # damage_draw_y = zombie.damage_rect.y - cam_y
                # pygame.draw.rect(self.screen, (0, 255, 0), (damage_draw_x, damage_draw_y, zombie.damage_rect.width, zombie.damage_rect.height), 2)


        for item in self.items_group:
            self.screen.blit(item.image, (item.x - cam_x + 10, (item.y - cam_y + 20) - item.vertical))
            
        player_img = self.player.get_current_image(camera_x=cam_x, camera_y=cam_y)
        p_draw_x = (self.player.x - cam_x) - (player_img.get_width() - self.player.width) // 2
        p_draw_y = (self.player.y - cam_y) - (player_img.get_height() - self.player.height) // 2
        
        
        # rect_draw_x = self.player.rect.x - cam_x
        # rect_draw_y = self.player.rect.y - cam_y
        
        # erect_draw_x = self.player.interact_rect.x - cam_x
        # erect_draw_y = self.player.interact_rect.y - cam_y
        
        # pygame.draw.rect(self.screen, (255,0,0), (rect_draw_x, rect_draw_y, self.player.rect.width, self.player.rect.height), 2)
        # pygame.draw.rect(self.screen, (255,100,0), (erect_draw_x, erect_draw_y, self.player.interact_rect.width, self.player.interact_rect.height), 2)

        self.screen.blit(player_img, (p_draw_x, p_draw_y))
        for tree in self.trees_group:
            if self.player.rect.colliderect(tree.opposite_rect):
                self.screen.blit(tree.image, (tree.x - cam_x, tree.y - cam_y))
                self.screen.blit(player_img, (p_draw_x, p_draw_y))
            else:
                self.screen.blit(tree.image, (tree.x - cam_x, tree.y - cam_y))

            pygame.draw.rect(self.screen, (55,0,0), (tree.opposite_rect.x - cam_x, tree.opposite_rect.y - cam_y, tree.opposite_rect.width, tree.opposite_rect.height), 2)

        for indicator in self.damage_indicators:
            indicator.draw(self.screen, indicator.world_x - cam_x, indicator.world_y - cam_y)
        for indicator in self.player_indicators:
            indicator.draw(self.screen, indicator.world_x - cam_x, indicator.world_y - cam_y)
        for index, notify in enumerate(self.notifications):
            if index <= 10:
                notify.draw(self.screen, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100 + (25 * index))
        for notify in self.fixed_notifications:
            notify[0].show_text(self.screen, self.player.x - self.camera.x, self.player.y - self.camera.y, flip=None)
            
        self.minimap.draw(
            self.screen, self.player, self.zombies_group, self.trees_group,
            cam_x, cam_y, self.screen.get_width(), self.screen.get_height(),
            base=self.safezone
        )
        
        # for wall_rect in WALLS:
        #     draw_x = wall_rect.x - cam_x
        #     draw_y = wall_rect.y - cam_y
            
        #     pygame.draw.rect(self.screen, (255, 0, 0), (draw_x, draw_y, wall_rect.width, wall_rect.height), 2)
            
        # for store_rect in STORIES:
        #     draw_x = store_rect.x - cam_x
        #     draw_y = store_rect.y - cam_y

        #     pygame.draw.rect(self.screen, (255, 0, 0), (draw_x, draw_y, store_rect.width, store_rect.height), 2)
            
        # for dealer_rect in DEALER:
        #     draw_x = dealer_rect.x - cam_x
        #     draw_y = dealer_rect.y - cam_y

        #     pygame.draw.rect(self.screen, (255, 0, 0), (draw_x, draw_y, dealer_rect.width, dealer_rect.height), 2)
        
        if IS_INVENTORY_OPEN:
            if AMMO_INVENTORY_OPEN:
                the_uni_inventory = self.inventory["Ammo"]
                self._inventory_preparing(self.inventory_ammo_group, "Ammo")
            elif GEAR_INVENTORY_OPEN:
                the_uni_inventory = self.inventory["Gear"]
                self._inventory_preparing(self.inventory_gear_group, "Gear")
            elif CRAFTING_INVENTORY_OPEN:
                the_uni_inventory = self.inventory["Crafting"]
                self._inventory_preparing(self.inventory_crafting_group, "Crafting")
            else:
                HEALTH_INVENTORY_OPEN = True
                the_uni_inventory = self.inventory["Health"]
                self._inventory_preparing(self.inventory_health_group, "Health")
            # for tap in the_uni_inventory.taps:
            #     pygame.draw.rect(self.screen, "#FF0000", (tap.x, tap.y, tap.width, tap.height), 2)
                
            for notify in GLOBAL_NOTIFICATIONS[:]:
                if HEALTH_INVENTORY_OPEN:
                    notify.draw(self.screen, the_uni_inventory.list_x + 130, the_uni_inventory.list_y + 10)
                elif AMMO_INVENTORY_OPEN:
                    notify.draw(self.screen, the_uni_inventory.list_x + 130, the_uni_inventory.list_y + 10)
                elif GEAR_INVENTORY_OPEN:
                    notify.draw(self.screen, the_uni_inventory.list_x + 130, the_uni_inventory.list_y + 10)
                elif CRAFTING_INVENTORY_OPEN:
                    notify.draw(self.screen, the_uni_inventory.list_x + 130, the_uni_inventory.list_y + 10)
                if notify.update():
                    GLOBAL_NOTIFICATIONS.remove(notify)

        self.player_info.draw()

        if IS_INVENTORY_OPEN:
            if self.player_info.dragged_item["char"]:
                self.screen.blit(self.player_info.dragged_item["item"].image, (self.mx - 20, self.my - 20))
            self.screen.blit(self.pointer, (self.mx, self.my))
        else:
            self.screen.blit(self.crosshair, (self.mx, self.my))
        pygame.display.flip()
