import pygame
import os
import sys
import random
import threading
import time
import math
from src.settings import *
import src.notification as notification
import src.minimap as minimap
import src.items as items
import src.assets_manager as assets
import src.central_managment as manage
from src.entities import Player, Zombie, Bullet, Tree


def get_random_value(choices=[]):
    return random.randint(0, 100) if len(choices) == 0 else random.choice(choices)

class GameEngine:
    """
    🕹️ THE CORE GAME CONTROLLER (v2.5)
    The brain center of Last Green. Initializes subsystems, tracks engine time states,
    coordinates data flow, and drives rendering blits to the graphics display.
    """
    def __init__(self):
        # os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 25"
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Last Green - Advanced State Engine v2.5")
        self.clock = pygame.time.Clock()
        
        # Pull graphics structures out into core memory addresses
        assets.load_all_assets()
        
        # Music configuration for background
        pygame.mixer.music.set_endevent(MUSIC_ENDED_EVENT)
        music_track = manage.get_music_randomly("background", assets.musics)
        pygame.mixer.music.load(music_track)
        pygame.mixer.music.play(loops=0)
        
        self.minimap = minimap.Minimap(size=200)
        
        # 🟢 SPAWN SURVIVOR UNIT
        # Pass the full animations dictionary mapping directly into our state engine
        self.player = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2, assets.animations)
        
        # 🧟 SPAWN THREAT MATRICES (Zombies)
        self.zombies = [
            Zombie(
                random.randint(100, 4900), 
                random.randint(100, 4900), 
                assets.animations["zombie_move"],
                assets.animations["zombie_die"]
            ) for _ in range(5)
        ]
        
        # 🌲 SPAWN MAP ENVIROMENT COLLIDERS
        self.trees = [
            Tree(random.randint(50, 4000), random.randint(50, 4000), assets.sprites["tree_1"]) 
            for _ in range(50)
        ]
        
        self.bullets            = []
        self.damage_indicators  = []
        self.notifications      = []
        self.items              = []
        
        # Camera initialization state boundary setups
        self.camera_x       = 0
        self.camera_y       = 0
        self.count          = 0
        self.global_counter = 1
        
        # Game loop condition control variable
        self.running = True

    def run(self):
        """The primary execution architecture loop."""
        while self.running:
            self.handle_events()       
            self.update_game_states()  # Calculate real-time vector alterations
            self.render_draw_calls()   # Flush image surfaces out to screen hardware
            self.clock.tick(FPS)       # Maintain rigid framerate pacing
        pygame.quit()
        sys.exit()
        
    def create_zombie(self, zombies):
        if len(zombies) < 50:
            zombie = Zombie(
                random.randint(100, 4900), 
                random.randint(100, 4900), 
                assets.animations["zombie_move"],
                assets.animations["zombie_die"]
            )
            game.zombies.append(zombie)
        if len(game.zombies) >= 10 and game.zombies[0].is_dead:
            manage.debugger("z_r", game.zombies[0].ID)
            del game.zombies[0]

    def handle_events(self):
        """Captures hardware peripherals interactions."""
        for event in pygame.event.get():
            manage.debugger("p_a", self.player.ammo_count, self.player.ammo_stack, self.player.weapon_ammo_count, self.player.ammo_type, self.player.weapon_type)
            if event.type == pygame.QUIT:
                self.running = False
            
            # 🎯 CATCH THE MUSIC END SIGNAL!
            elif event.type == MUSIC_ENDED_EVENT:
                music_track = manage.get_music_randomly("background", assets.musics)
                pygame.mixer.music.load(music_track)
                pygame.mixer.music.play(loops=0)
                
            # 🔫 BALLISTIC TRIGGERS (Weapon Systems)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # First check for the ammo count
                if self.player.ammo_count > 0:
                    # 0. Fire sound triggered
                    manage.get_sound_randomly("fire", assets.sounds).play()
                    self.player.firing = True
                    self.player.current_frame = 0.0  # Reset frame to track full weapon burst cycle cleanly
                    
                    # 1. Capture screen mouse position
                    ms_x, ms_y = pygame.mouse.get_pos()
                    
                    # 2. Add relative camera coordinates to translate screen mouse to actual Map coordinates
                    world_mx = ms_x + self.camera_x
                    world_my = ms_y + self.camera_y
                    
                    # 3. Locate fire starting position (Survivor core center points)
                    p_cx = self.player.x + self.player.width // 2
                    p_cy = self.player.y + self.player.height // 2
                    
                    # 4. Perform Hypotenuse normalizations to resolve consistent firing vector speed
                    dx, dy = world_mx - p_cx, world_my - p_cy
                    dist = math.hypot(dx, dy)
                    if dist > 0:
                        # Append a pristine new bullet tracking element to the physics stack
                        self.bullets.append(Bullet(p_cx, p_cy, dx/dist, dy/dist))
                        
                    # 5. Decrement inventory mag balances
                    self.player.ammo_count -= 1
                else:
                    manage.get_sound_randomly("no_ammo", assets.sounds).play()

    def update_game_states(self):
        """Executes all processing mathematics updates for this current time delta frame."""
        keys = pygame.key.get_pressed()
        
        # Process survivor inputs
        self.player.move(keys, self.trees)
        self.player.reload(keys)
        
        # Compute active state machine animations dynamically
        current_state = self.player.determine_action_state()
        self.player.update_animation(current_state)
            
        # Route pathfinding instructions for the horde tracking loops
        for zombie in self.zombies:
            zombie.update_ai(self.player, self.zombies, self.trees)
            
        # Iterate over tracer bullets array backward or as slice copies to prevent item deletion index skips!
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
            
            # Bullet - Zombie Damage
            decision = manage.bullet_zombie_collision(bullet, self.zombies)
            if decision["bullet_die"]:
                if decision["zombie"].health <= 0:
                    decision["zombie"].is_dead = True
                    
                    # Make items dropped randomly
                    if get_random_value() >= 80:
                        value = get_random_value(["ammo", "health_1", "health_2"])
                        if value == "ammo":
                            created_item = items.Ammo(
                                        decision["zombie"].x, 
                                        decision["zombie"].y,
                                        assets.sprites["ammo"],
                                        random.randrange(10, 25),
                                        "SniperAmmo"
                                    )
                        elif value in ["health_1", "health_2"]:
                            created_item = items.Health(
                                        x=decision["zombie"].x, 
                                        y=decision["zombie"].y,
                                        image=assets.sprites[value],
                                        type="Health"
                                    )
                        created_item.set_name_id(created_item.type, self.count)
                        self.items.append(created_item)
                        self.count += 1
                        manage.debugger("d_i", self.items[-1].ID, self.count)
                            
                bullet.traveled = 800
                # 💥 SPAWN THE DAMAGE TEXT INSTANCE HERE!
                # Pass the zombie's top center coordinates and hit damage parameters
                self.damage_indicators.append(
                    notification.DamageNumber(
                        x=decision["zombie"].x + 40, 
                        y=decision["zombie"].y +10, 
                        amount=bullet.damage
                        )
                )
                if bullet in self.bullets: 
                    self.bullets.remove(bullet)
                
            # Bullet - Trees Collision
            decision = manage.bullet_tree_collision(bullet, self.trees)
            if decision["bullet_die"]:
                bullet.traveled = 800
                if bullet in self.bullets: 
                    self.bullets.remove(bullet)
                    
        for indicator in self.damage_indicators[:]:
            if indicator.update():
                self.damage_indicators.remove(indicator)
                
        for notify in self.notifications[:]:
            if notify.update():
                self.notifications.remove(notify)

        if self.global_counter % 60 == 0:
            self.create_zombie(self.zombies)
            self.global_counter = 1
        else:
            self.global_counter += 1
        # 🎥 DYNAMIC VIRTUAL CAMERA TRACKING
        # Centers screen viewfinder view arrays exactly over the player's world position vector,
        # clamping the values down so the view can never scroll outside the active world dimensions.
        self.camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, self.player.x - SCREEN_WIDTH // 2))
        self.camera_y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, self.player.y - SCREEN_HEIGHT // 2))

    def render_draw_calls(self):
        """Flushes game buffer surfaces down onto active system frame layers."""
        # Clean background field canvas buffer
        self.screen.fill(GREEN_BG)

        # 2. DRAW OPPOSITION ENEMY GROUPS
        for zombie in self.zombies: 
            if zombie.is_dead:
                zombie_die_img = zombie.get_current_image(flag="die")
                self.screen.blit(zombie_die_img, (zombie.x - self.camera_x, zombie.y - self.camera_y + (zombie.height // 2) ))
            else:
                zombie_move_img = zombie.get_current_image()
                self.screen.blit(zombie_move_img, (zombie.x - self.camera_x, zombie.y - self.camera_y + (zombie.height // 2)))
        
        # 2. DROP ITEMS & PROCESS PICKUP TRIGGER
        for item in self.items[:]:
            if not item.is_taked and manage.player_item_collision(item, self.player):
                item.is_taked = True
                notify_icon = pygame.transform.scale(item.image, (32, 32))
                manage.debugger("p_h", self.player.health)
                self.notifications.append(
                    notification.Notification(
                        text=f"+{item.amount} {item.type} ",
                        image=notify_icon
                    )
                )
                manage.debugger("g_i", item.ID)
                
            if item.is_taked:
                self.items.remove(item)
            else:
                self.screen.blit(item.image, (item.x - self.camera_x + 40, ((item.y - self.camera_y) + 80) - item.vertical))
                item.up_down()
                # pygame.draw.rect(self.screen, (255, 0, 0), (item.rect.x - self.camera_x - 20, item.rect.y - self.camera_y - 20, item.width + 60, item.height + 60), 2)
        
        # 3. DRAW SURVIVOR UNIT HERO
        # Calculates centering margins to draw huge character visuals cleanly centered over tiny collision boxes.
        player_img = self.player.get_current_image(camera_x=self.camera_x, camera_y=self.camera_y)
        p_draw_x = (self.player.x - self.camera_x) - (player_img.get_width() - self.player.width) // 2
        p_draw_y = (self.player.y - self.camera_y) - (player_img.get_height() - self.player.height) // 2
        self.screen.blit(player_img, (p_draw_x, p_draw_y))
        
        # 4. DRAW ENVIRONMENT SCENERY (Y-sorted layer offset)     
        for tree in self.trees:
            self.screen.blit(tree.image, (tree.x - self.camera_x, (tree.y - self.camera_y) + 100))

        # ==============================================================================
        # 🛠️ DEBUG HITBOX OVERLAY LAYER 
        # ==============================================================================
        # Draw Player Hitbox (Should be a small 40x40 box at their feet)
        # pygame.draw.rect(self.screen, (255, 0, 0), (self.player.rect.x - self.camera_x, self.player.rect.y - self.camera_y, self.player.rect.width, self.player.rect.height), 2)
        
        # Draw Zombie Hitboxes
        # for zombie in self.zombies:
        #     pygame.draw.rect(self.screen, (255, 0, 0), (zombie.rect.x - self.camera_x, zombie.rect.y - self.camera_y, zombie.rect.width, zombie.rect.height), 2)
        
        # # Draw Trees Hitboxes
        # for tree in self.trees:
        #     pygame.draw.rect(self.screen, (255, 0, 0), (tree.rect.x - self.camera_x, tree.rect.y - self.camera_y, tree.rect.width, tree.rect.height), 2)
            
        # ✨ DRAW FLOATING the notifications!
        for indicator in self.damage_indicators:
            # Convert their world spawn positions to screen view coordinates
            dmg_screen_x = indicator.world_x - self.camera_x
            dmg_screen_y = indicator.world_y - self.camera_y
            indicator.draw(self.screen, dmg_screen_x, dmg_screen_y)
            
        # ✨ DRAW FLOATING NOTIFICATIONS
        for notify in self.notifications:
            # Pass the live player screen positions directly down!
            notify.draw(self.screen, self.player.x - self.camera_x + (self.player.width // 2), self.player.y - self.camera_y - 20)
            
        # Draw the minimap
        self.minimap.draw(
            self.screen,
            self.player,
            self.zombies,
            self.trees,
            self.camera_x,
            self.camera_y,
            self.screen.get_width(),
            self.screen.get_height()
        )
  
        # Swap framebuffers 
        pygame.display.flip()

if __name__ == "__main__":
    game = GameEngine()
    game.run()