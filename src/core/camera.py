# src/core/camera.py
from src.settings import WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target_x, target_y):
        self.x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, target_x - SCREEN_WIDTH // 2))
        self.y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, target_y - SCREEN_HEIGHT // 2))

    def apply(self, x, y):
        return x - self.x, y - self.y
