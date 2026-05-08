import characters

class MouseFeatures:
    def __init__(self, screen_x, screen_y, player):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.player = player
    
    def get_mouse_direction(self):
        # Convert screen to WORLD using player's camera
        world_x = self.screen_x + self.player.camera_x
        world_y = self.screen_y + self.player.camera_y
        
        # Calculate difference (both in WORLD)
        dx = world_x - self.player.x
        dy = world_y - self.player.y
        distance = (dx**2 + dy**2) ** 0.5
        
        if distance > 0:
            dir_x = dx / distance
            dir_y = dy / distance
            
            # Bullet spawn at player center (WORLD)
            bullet_x = self.player.x + self.player.width // 2
            bullet_y = self.player.y + self.player.height // 2
            
            return bullet_x, bullet_y, dir_x, dir_y
        
        # Mouse exactly on player
        return self.player.x, self.player.y, 0, 0