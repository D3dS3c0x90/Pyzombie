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
        
        self.rect_e         = pygame.Rect(self.x + self.image.get_width() - 310, self.y + 25, 300, self.height - 25)
        self.rect_w         = pygame.Rect(self.x, self.y + 25, 300, self.height - 25)
        self.rect_n         = pygame.Rect(self.x + 90, self.y + 25, self.width - 100, 275)
        self.rect           = pygame.Rect(self.x + 15, self.y + self.image.get_height() - 240, self.width - 25, 225)
        self.door_rect_in   = pygame.Rect(self.x + (self.image.get_width() // 2) + 25, self.y + self.image.get_height() - 20, 125, 70)
        self.door_rect_out  = pygame.Rect(self.x + (self.image.get_width() // 2) + 25, self.y + self.image.get_height() - 300, 125, 70)
        
    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))
        
    