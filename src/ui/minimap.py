# src/ui/minimap.py
import pygame
from src.settings import WORLD_WIDTH


class Minimap:
    def __init__(self, margin=5, scale_factor=0.04):
        self.size = WORLD_WIDTH * scale_factor
        self.margin = margin
        self.scale = scale_factor
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

    def draw(self, main_screen, player, zombies, trees, camera_x, camera_y, screen_width, screen_height, base=None):
        self.surface.fill((30, 30, 30, 200))
        pygame.draw.rect(self.surface, (200, 200, 200), (0, 0, self.size, self.size), 2)

        for tree in trees:
            tx, ty = int(tree.x * self.scale), int(tree.y * self.scale)
            if 0 <= tx < self.size and 0 <= ty < self.size:
                pygame.draw.circle(self.surface, (0, 100, 0), (tx, ty), 2)

        for zombie in zombies:
            if not zombie.is_dead:
                zx, zy = int(zombie.x * self.scale), int(zombie.y * self.scale)
                if 0 <= zx < self.size and 0 <= zy < self.size:
                    pygame.draw.circle(self.surface, (220, 20, 60), (zx, zy), 2)

        px, py = int(player.x * self.scale), int(player.y * self.scale)
        if 0 <= px < self.size and 0 <= py < self.size:
            pygame.draw.circle(self.surface, (0, 191, 255), (px, py), 4)

        cam_x, cam_y = int(camera_x * self.scale), int(camera_y * self.scale)
        cam_w, cam_h = int(screen_width * self.scale), int(screen_height * self.scale)
        pygame.draw.rect(self.surface, (255, 255, 255), (cam_x, cam_y, cam_w, cam_h), 1)

        bx, by = int(base.x * self.scale), int(base.y * self.scale)
        bw, bh = int(base.width * self.scale), int(base.height * self.scale)
        if 0 <= bx < self.size and 0 <= by < self.size:
            pygame.draw.rect(self.surface, (50, 200, 50), (bx, by, bw, bh), 2)

        main_screen.blit(self.surface, (self.margin, self.margin))
