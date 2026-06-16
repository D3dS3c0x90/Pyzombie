# safe_zone.py
import pygame


class SafeZone:
    def __init__(self, x, y, width, height, type="base", image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.type = type
        self.image = image
        
        self.rect_e         = pygame.Rect(self.x + self.image.get_width() - 75, self.y, 100, self.height)
        self.rect_w         = pygame.Rect(self.x - 20, self.y, 100, self.height)
        self.rect_n         = pygame.Rect(self.x, self.y, self.width, 100)
        self.rect           = pygame.Rect(self.x, self.y + self.image.get_height() - 90, self.width, 100)
        self.door_rect_in   = pygame.Rect(self.x + (self.image.get_width() // 2) - 100, self.y + self.image.get_height() - 20, 100, 70)
        self.door_rect_out  = pygame.Rect(self.x + (self.image.get_width() // 2) - 100, self.y + self.image.get_height() - 120, 100, 70)
        
    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))
        
    