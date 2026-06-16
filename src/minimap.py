# minimap.py
import pygame
from src.settings import WORLD_WIDTH


class Minimap:
    def __init__(self, margin=5, scale_factor=0.04):
        """
        size: The pixel width and height of the minimap box.
        margin: How far from the top-left edge of the screen the box sits.
        scale_factor: 0.05 means 5% of real world sizes (e.g., 2000 world px = 100 minimap px)
        """
        self.size = WORLD_WIDTH * scale_factor
        self.margin = margin
        self.scale = scale_factor
        
        # Create a static background box surface with a dark alpha blend
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
    def draw(self, main_screen, base, player, zombies, trees, camera_x, camera_y, screen_width, screen_height):
        # 1. Clear the minimap canvas surface with a semi-transparent dark gray
        self.surface.fill((30, 30, 30, 200)) 
        
        # 2. Draw a clean border outline around the minimap box
        pygame.draw.rect(self.surface, (200, 200, 200), (0, 0, self.size, self.size), 2)
        
        # 🌲 DRAW TREES (Tiny Dark Green Circles)
        for tree in trees:
            tx = int(tree.x * self.scale)
            ty = int(tree.y * self.scale)
            if 0 <= tx < self.size and 0 <= ty < self.size:
                pygame.draw.circle(self.surface, (0, 100, 0), (tx, ty), 2)
                    
        # 🧟 DRAW ENEMIES (Tiny Red Circles)
        for zombie in zombies:
            if not zombie.is_dead:
                zx = int(zombie.x * self.scale)
                zy = int(zombie.y * self.scale)
                if 0 <= zx < self.size and 0 <= zy < self.size:
                    pygame.draw.circle(self.surface, (220, 20, 60), (zx, zy), 2)
                    
        # 🤠 DRAW PLAYER (Bright Blue Circle - Always on top of environmental objects)
        px = int(player.x * self.scale)
        py = int(player.y * self.scale)
        if 0 <= px < self.size and 0 <= py < self.size:
            pygame.draw.circle(self.surface, (0, 191, 255), (px, py), 4)

        # 🔲 DRAW CAMERA VIEWPORT BOX (Shows current field of view range)
        cam_x = int(camera_x * self.scale)
        cam_y = int(camera_y * self.scale)
        cam_w = int(screen_width * self.scale)
        cam_h = int(screen_height * self.scale)
        pygame.draw.rect(self.surface, (255, 255, 255), (cam_x, cam_y, cam_w, cam_h), 1)
        
        bx = int(base.x * self.scale)
        by = int(base.y * self.scale)
        bw = int(base.width * self.scale)
        bh = int(base.height * self.scale)
        if 0 <= bx < self.size and 0 <= by < self.size:
            pygame.draw.rect(self.surface, (50, 200, 50), (bx, by, bw, bh), 2)

        # 3. Final Output Blit: Stamp the compiled map directly onto the viewport window screen layer
        main_screen.blit(self.surface, (self.margin, self.margin))