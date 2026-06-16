# main.py
import pygame
import sys
import random
import math
from src.settings import *
import src.notification as notification
import src.minimap as minimap
import src.safe_zone as safe_zone
import src.items as items
import src.player_state as player_state
import src.assets_manager as assets
import src.central_managment as manage
import src.entities as entity


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
        
        self.minimap  = minimap.Minimap()
        self.safezone = safe_zone.SafeZone(1000, 2500, assets.sprites["base"].get_width(), assets.sprites["base"].get_height(), image=assets.sprites["base"])
        
        # Crosshairs
        self.crosshair = assets.sprites["crosshair"]
        pygame.mouse.set_visible(False)
        
        # 🟢 SPAWN SURVIVOR UNIT
        # Pass the full animations dictionary mapping directly into our state engine
        self.player = entity.Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2, assets.animations)
        
        # 🧟 SPAWN THREAT MATRICES (Zombies)
        self.zombies = [
            entity.Zombie(
                random.randint(0, WORLD_WIDTH - 10), 
                random.randint(0, WORLD_HEIGHT - 10),  
                assets.animations["zombie_move"],
                assets.animations["zombie_die"]
            ) for _ in range(5)
        ]
        
        # 🌲 SPAWN MAP ENVIROMENT COLLIDERS
        self.trees = [
            entity.Tree(
                random.randint(0, WORLD_WIDTH - assets.sprites["tree_1"].get_width()), 
                random.randint(0, WORLD_HEIGHT - assets.sprites["tree_1"].get_height()),  
                assets.sprites["tree_1"]) 
            for _ in range(50)
        ]
        
        self.bullets               = []
        self.empty_bullets         = []
        self.damage_indicators     = []
        self.notifications         = []
        self.player_indicators     = []
        self.items                 = []
        self.blood                 = []
        
        # Camera initialization state boundary setups
        self.camera_x              = 0
        self.camera_y              = 0
        self.count                 = 0
        self.global_counter        = 1
        
        # Mouse Position X, Y
        self.mx, self.my = None, None
        
        # Game loop condition control variable
        self.running = True

    def run(self):
        """The primary execution architecture loop."""
        while self.running:
            self.handle_events()       
            self.update_game_states()  # Calculate real-time vector alterations
            self.render_draw_calls()   # Flush image surfaces out to screen hardware
            self.clock.tick(FPS)       # Maintain rigid framerate pacing
            
            manage.play_sound_randomly("background", rand=True)
            # for blood in self.blood:
            #     print(f"{blood[0]} - {blood[1]} - {blood[2]}")
            # manage.play_sound_randomly("owl", rand=True)
            
        pygame.quit()
        sys.exit()
        
    def create_zombie(self, zombies):
        if len(zombies) < 50:
            zombie = entity.Zombie(
                random.randint(0, WORLD_WIDTH - 10), 
                random.randint(0, WORLD_HEIGHT - 10), 
                assets.animations["zombie_move"],
                assets.animations["zombie_die"]
            )
            game.zombies.append(zombie)
        if len(game.zombies) >= 10 and game.zombies[0].is_dead:
            del game.zombies[0]

    def handle_events(self):
        """Captures hardware peripherals interactions."""
        for event in pygame.event.get():
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
                        self.bullets.append(entity.Bullet(p_cx, p_cy, dx/dist, dy/dist))
                        
                    # 5. Decrement inventory mag balances
                    self.player.ammo_count -= 1
                else:
                    manage.play_sound_randomly("no_ammo")

    def update_game_states(self):
        """Executes all processing mathematics updates for this current time delta frame."""
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        self.mx, self.my = pygame.mouse.get_pos()
        
        # Process survivor inputs
        self.player.move(keys, self.trees, self.safezone)
        self.player.reload(keys, mouse)
        
        # Compute active state machine animations dynamically
        current_state = self.player.determine_action_state()
        self.player.update_animation(current_state)
            
        # Route pathfinding instructions for the horde tracking loops
        for zombie in self.zombies:
            zombie.update_ai(self.player, self.safezone, self.zombies, self.trees)
            if manage.player_zombie_collision(self.player, zombie):
                self.player_indicators.append(
                    notification.DamageNumber(
                        color=(100, 100, 0),
                        lifetime=100,
                        x=self.player.x + 40, 
                        y=self.player.y +10, 
                        amount=zombie.damage
                        )
                )
            
        # Iterate over tracer bullets array backward or as slice copies to prevent item deletion index skips!
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
                self.empty_bullets.append(
                    entity.DeadBullet(
                        self.player.x + 15,
                        self.player.y + 5,
                    )
                )
            
            # Bullet - Zombie Damage
            decision = manage.bullet_zombie_collision(bullet, self.zombies, self.player)
            if decision["bullet_die"]:
                if decision["zombie"].health <= 0:
                    decision["zombie"].is_dead = True
                    
                    # Make items dropped randomly
                    random_value = manage.get_random_value()
                    
                    created_item = items.Health(
                            x=decision["zombie"].x, 
                            y=decision["zombie"].y,
                            image=assets.sprites[random.choice(["health_1", "health_2"])],
                            type="Health"
                        ) if random_value >= 90 else items.Coins(
                            x=decision["zombie"].x, 
                            y=decision["zombie"].y,
                            image=assets.sprites[random.choice(["coins_1", "coins_2"])],
                            amount=random.randrange(10, 18),
                            type="Coins"
                        ) if random_value >= 70 else items.Ammo(
                            decision["zombie"].x, 
                            decision["zombie"].y,
                            assets.sprites[random.choice(["ammo"])],
                            random.randrange(12, 18),
                            "RifleAmmo"
                        ) if random_value >= 45 else None

                    if created_item:
                        created_item.set_name_id(created_item.type, self.count)
                        self.items.append(created_item)
                        self.count += 1
                            
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
                # Show blood
                self.blood.append(
                    (
                        manage.get_random_value(assets.sprites["blood"]), 
                        decision["zombie"].x + decision["zombie"].width // 2, 
                        decision["zombie"].y + decision["zombie"].height // 2
                        )
                    )
                
                if bullet in self.bullets: 
                    self.bullets.remove(bullet)
                    self.empty_bullets.append(
                    entity.DeadBullet(
                        self.player.x + 15,
                        self.player.y + 10,
                    )
                )
                
            # Bullet - Base Collision
            if self.safezone.rect.colliderect(bullet.rect) or self.safezone.rect_e.colliderect(bullet.rect) or self.safezone.rect_w.colliderect(bullet.rect) or self.safezone.rect_n.colliderect(bullet.rect):
                bullet.traveled = 800
            
            # Bullet - Trees Collision
            decision = manage.bullet_tree_collision(bullet, self.trees)
            if decision["bullet_die"]:
                bullet.traveled = 800
                if bullet in self.bullets: 
                    self.bullets.remove(bullet)
                    
        for indicator in self.damage_indicators[:]:
            if indicator.update():
                self.damage_indicators.remove(indicator)
                
        for indicator in self.player_indicators[:]:
            if indicator.update():
                self.player_indicators.remove(indicator)
                
        for notify in self.notifications[:]:
            if notify.update():
                self.notifications.remove(notify)

        if self.global_counter % (FPS * int(manage.get_random_value() * 0.5) + 1) == 0:
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
        self.screen.fill(ZOMBIED)
        
        # Dead Bullets
        for dead_bullet in self.empty_bullets[:]:
            dead_bullet.update()
            self.screen.blit(dead_bullet.image, (dead_bullet.x - self.camera_x, dead_bullet.y - self.camera_y))
            pygame.draw.rect(self.screen, (0, 255, 0), dead_bullet.rect, 2)
            
        for blood in self.blood[:]:
            self.screen.blit(blood[0], (blood[1] - self.camera_x, blood[2] - self.camera_y))
        
        # Door Rect Collision Detection
        door_rect_in = self.safezone.door_rect_in.move(-self.camera_x, -self.camera_y)
        door_rect_out = self.safezone.door_rect_out.move(-self.camera_x, -self.camera_y)
        rect_e = self.safezone.rect_e.move(-self.camera_x, -self.camera_y)
        rect_w = self.safezone.rect_w.move(-self.camera_x, -self.camera_y)
        rect_n = self.safezone.rect_n.move(-self.camera_x, -self.camera_y)
        
        pygame.draw.rect(self.screen, (255, 0, 0), (self.safezone.rect.x - self.camera_x - 10, self.safezone.rect.y - self.camera_y - 10, self.safezone.rect.width + 20, self.safezone.rect.height + 20), 2)
        pygame.draw.rect(self.screen, (0, 0, 50), door_rect_in, 2)
        pygame.draw.rect(self.screen, (0, 0, 255), door_rect_out, 2)
        pygame.draw.rect(self.screen, (0, 130, 0), rect_e, 2)
        pygame.draw.rect(self.screen, (150, 10, 70), rect_w, 2)
        pygame.draw.rect(self.screen, (0, 240, 0), rect_n, 2)

        # 1. DRAW OPPOSITION ENEMY GROUPS
        for zombie in self.zombies: 
            if zombie.is_dead:
                zombie_die_img = zombie.get_current_image(flag="die")
                self.screen.blit(zombie_die_img, (zombie.x - self.camera_x, zombie.y - self.camera_y + (zombie.height // 2) ))
            else:
                zombie_move_img = zombie.get_current_image()
                self.screen.blit(zombie_move_img, (zombie.x - self.camera_x, zombie.y - self.camera_y + (zombie.height // 2)))
                zombie.draw_health_bar(self.screen, zombie.x - self.camera_x - 10, zombie.y - self.camera_y + (zombie.height // 2) - 2)
        
        # 2. DROP ITEMS & PROCESS PICKUP TRIGGER
        for item in self.items[:]:
            if not item.is_taked and manage.player_item_collision(item, self.player):
                item.is_taked = True
                if item.type == "Coins":
                    self.player.coins += item.amount
                    manage.play_sound_randomly("coins")
                elif item.type in ["RifleAmmo",]:
                    manage.play_sound_randomly("ammo")
                elif item.type in ["Health",]:
                    manage.play_sound_randomly("health")
                notify_icon = pygame.transform.scale(item.image, (30, 30))
                self.notifications.append(
                    notification.Notification(
                        text=f"+{item.amount} {item.type} ",
                        image=notify_icon
                    )
                )
                
            if item.is_taked:
                self.items.remove(item)
            else:
                self.screen.blit(item.image, (item.x - self.camera_x + 10, ((item.y - self.camera_y) + 20) - item.vertical))
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
        
        ## Draw Zombie Hitboxes
        # for zombie in self.zombies:
            # pygame.draw.rect(self.screen, (255, 0, 0), (zombie.rect.x - self.camera_x, zombie.rect.y - self.camera_y, zombie.rect.width, zombie.rect.height), 2)

            # Damage Rect Collision Detection
            # damage_rect = zombie.damage_rect.move(-self.camera_x, -self.camera_y)
            # pygame.draw.rect(self.screen, (0, 0, 255), damage_rect, 2)
        
        # # Draw Trees Hitboxes
        # for tree in self.trees:
        #     pygame.draw.rect(self.screen, (255, 0, 0), (tree.rect.x - self.camera_x, tree.rect.y - self.camera_y, tree.rect.width, tree.rect.height), 2)
            
        # ✨ DRAW SAFE ZONE MARKET!
        self.safezone.draw(
            self.screen,
            self.camera_x, 
            self.camera_y
        )
            
        # ✨ DRAW FLOATING the notifications!
        for indicator in self.damage_indicators:
            # Convert their world spawn positions to screen view coordinates
            dmg_screen_x = indicator.world_x - self.camera_x
            dmg_screen_y = indicator.world_y - self.camera_y
            indicator.draw(self.screen, dmg_screen_x, dmg_screen_y)
            
        for indicator in self.player_indicators:
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
            self.safezone,
            self.player,
            self.zombies,
            self.trees,
            self.camera_x,
            self.camera_y,
            self.screen.get_width(),
            self.screen.get_height()
        )
        
        player_info = player_state.PlayerState(
            self.screen,
            [0, SCREEN_HEIGHT - 120],
            [160, SCREEN_HEIGHT - 105],
            self.player
        )
        
        player_info.draw()
  
        # Crosshair drawing
        self.screen.blit(self.crosshair, (self.mx, self.my))
  
        # Swap framebuffers 
        pygame.display.flip()

if __name__ == "__main__":
    game = GameEngine()
    game.run()