import pygame
import os
import sys
import random
import threading
import time
import math
from src.settings import *
import src.assets_manager as assets
import src.central_managment as manage
from src.entities import Player, Zombie, Bullet ,Tree

def create_zombie(game):
    while True:
        time.sleep(5.0)
        zombie = Zombie(
            random.randint(200, 4000), 
            random.randint(200, 4000), 
            assets.animations["zombie_move"])
        
        game.zombies.append(zombie)

class GameEngine:
    """
    🕹️ THE CORE GAME CONTROLLER (TREES REMOVED)
    The brain center of Last Green. Initializes subsystems, tracks engine time states,
    coordinates data flow, and drives rendering blits to the graphics display.
    """
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 75"
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Last Green - Refactored Engine v2.0")
        self.clock = pygame.time.Clock()
        
        # Pull graphics structures out into core memory addresses
        assets.load_all_assets()
        
        # 🟢 SPAWN SURVIVOR UNITS
        self.player     = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2, assets.animations["player_move"])
        
        # 🧟 SPAWN THREAT MATRICES (Zombies)
        self.zombies    = [
            Zombie(
                random.randint(200, 4500), 
                random.randint(200, 4500), 
                assets.animations["zombie_move"])
            for _ in range(5)]
        
        self.trees      = [
            Tree(
                random.randint(50, 4000), 
                random.randint(50, 4000), 
                assets.sprites["tree_1"]) 
            for _ in range(30)
            ]
        self.bullets = []
        
        # Game loop condition control variable
        self.running = True

    def run(self):
        """The primary execution architecture loop."""
        while self.running:
            self.handle_events()       # Listen for inputs/triggers
            self.update_game_states()  # Calculate real-time vector alterations
            self.render_draw_calls()   # Flush image surfaces out to screen hardware
            self.clock.tick(FPS)       # Maintain rigid framerate pacing
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Captures hardware peripherals interactions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # 🔫 BALLISTIC TRIGGERS (Weapon Systems)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

    def update_game_states(self):
        """Executes all processing mathematics updates for this current time delta frame."""
        keys = pygame.key.get_pressed()
        
        # Process survivor inputs (Passing an empty list [] instead of trees so collision check doesn't break)
        self.player.move(keys, self.trees)
        self.player.update_animation()
        
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
                manage.debugger("b_z", bullet.ID, zombie.ID, decision["bullet_damage"])
                bullet.traveled = 800
                self.bullets.remove(bullet)

        # 🎥 DYNAMIC VIRTUAL CAMERA TRACKING
        # Centers screen viewfinder view arrays exactly over the player's world position vector,
        # clamping the values down so the view can never scroll outside the active world dimensions.
        self.camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, self.player.x - SCREEN_WIDTH // 2))
        self.camera_y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, self.player.y - SCREEN_HEIGHT // 2))

    def render_draw_calls(self):
        """Flushes game buffer surfaces down onto active system frame layers."""
        # Clean background field canvas buffer
        self.screen.fill(GREEN_BG)
        
        # (Trees rendering section completely removed)
                
        # 1. DRAW BALLISTICS TRACERS
        for bullet in self.bullets:
            pygame.draw.rect(self.screen, YELLOW, (bullet.x - self.camera_x, bullet.y - self.camera_y, bullet.width, bullet.height))

        # 2. DRAW OPPOSITION ENEMY GROUPS
        for zombie in self.zombies:
            z_img = zombie.get_current_image()
            self.screen.blit(z_img, (zombie.x - self.camera_x, zombie.y - self.camera_y))
        
        # 3. DRAW SURVIVOR UNIT HERO
        # Calculates centering margins to draw huge character visuals cleanly centered over tiny collision boxes.
        p_img = self.player.get_current_image()
        p_draw_x = (self.player.x - self.camera_x) - (p_img.get_width() - self.player.width) // 2
        p_draw_y = (self.player.y - self.camera_y) - (p_img.get_height() - self.player.height) // 2
        self.screen.blit(p_img, (p_draw_x, p_draw_y))
        
        # Draw Tree Last One        
        for tree in self.trees:
            self.screen.blit(tree.image, (tree.x - self.camera_x, (tree.y - self.camera_y) + 100))

 
        # ==============================================================================
        # 🛠️ DEBUG HITBOX OVERLAY LAYER (Add this right here!)
        # ==============================================================================
        # We draw an unfilled bright red rectangle exactly where the physics engine 
        # calculates the entity bodies, adjusted for the camera position.
        
        # Draw Player Hitbox (Should be a small 40x40 box at their feet)
        pygame.draw.rect(self.screen, (255, 0, 0), 
                         (self.player.rect.x - self.camera_x, 
                          self.player.rect.y - self.camera_y, 
                          self.player.rect.width, 
                          self.player.rect.height), 2) # The '2' at the end makes it an outline, not filled
        
        # Draw Zombie Hitboxes (Should be 50x50 boxes around the horde)
        for zombie in self.zombies:
            pygame.draw.rect(self.screen, (255, 0, 0), 
                             (zombie.rect.x - self.camera_x, 
                              zombie.rect.y - self.camera_y, 
                              zombie.rect.width, 
                              zombie.rect.height), 2)
        # ==============================================================================
        
        # Draw Trees
        for tree in self.trees:
            pygame.draw.rect(self.screen, (255, 0, 0),
                (tree.rect.x - self.camera_x,
                 (tree.rect.y - self.camera_y),
                 tree.rect.width,
                 tree.rect.height), 2)
        # Swap framebuffers 
        pygame.display.flip()

if __name__ == "__main__":
    game = GameEngine()
    thread = threading.Thread(target=create_zombie, args=(game,))
    thread.daemon = True
    thread.start()
    game.run()