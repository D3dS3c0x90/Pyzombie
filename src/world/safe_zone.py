# src/world/safe_zone.py
import pygame


class SafeZone:
    def __init__(self, x, y, width, height, type="base", image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.type = type
        self.image = image

        self.rect_e = pygame.Rect(self.x + self.image.get_width() - 50, self.y, 100, self.height - 20)
        self.rect_w = pygame.Rect(self.x + 20, self.y, 80, self.height - 20)
        self.rect_n = pygame.Rect(self.x + 20, self.y, self.width - 20, 150)
        self.rect = pygame.Rect(self.x + 20, self.y + self.image.get_height() - 120, self.width - 20, 100)
        self.door_rect_in = pygame.Rect(
            self.x - 80, self.y + (self.image.get_height() // 2) - 250, 100, 250
        )
        self.door_rect_out = pygame.Rect(
            self.x + 100, self.y + (self.image.get_height() // 2) - 250, 100, 250
        )
        
        self.walls = [self.rect_e, self.rect_w, self.rect_n, self.rect]

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))
        
        # pygame.draw.rect(screen, (255, 0, 0), (self.rect_e.x - camera_x, self.rect_e.y - camera_y, self.rect_e.width, self.rect_e.height), 2)
        # pygame.draw.rect(screen, (0, 0, 255), (self.rect_w.x - camera_x, self.rect_w.y - camera_y, self.rect_w.width, self.rect_w.height), 2)
        # pygame.draw.rect(screen, (255, 255, 0), (self.rect_n.x - camera_x, self.rect_n.y - camera_y, self.rect_n.width, self.rect_n.height), 2)
        # pygame.draw.rect(screen, (255, 0, 255), (self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height), 2)
        # pygame.draw.rect(screen, (0, 255, 0), (self.door_rect_in.x - camera_x, self.door_rect_in.y - camera_y, self.door_rect_in.width, self.door_rect_in.height), 2)
        # pygame.draw.rect(screen, (255, 165, 0), (self.door_rect_out.x - camera_x, self.door_rect_out.y - camera_y, self.door_rect_out.width, self.door_rect_out.height), 2)
