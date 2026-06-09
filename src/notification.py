import pygame

class TextMessage:
    def __init__(self, text="", amount="", color=(255, 0, 0), lifetime=30, speed=2, image=None):
        self.text = text
        self.amount = str(amount)
        self.color = color
        self.image = image
        
        self.y = 0  
        self.vertical_speed = speed 
        self.lifetime = lifetime  
        self.max_lifetime = lifetime 
        self.alpha = 255            
        self.font = pygame.font.SysFont("Arial", 24, bold=True)

    def update(self):
        self.y -= self.vertical_speed  # Drifts upwards
        self.lifetime -= 1
        self.alpha = max(0, int((self.lifetime / self.max_lifetime) * 255))
        return self.lifetime <= 0

    def draw(self, surface, target_x, target_y):
        display_string = f"{self.text} {self.amount}".strip()
        text_surface = self.font.render(display_string, True, self.color)
        
        spacing = 8  
        total_width = text_surface.get_width()
        total_height = text_surface.get_height()
        
        if self.image:
            total_width += self.image.get_width() + spacing
            total_height = max(total_height, self.image.get_height())
            
        start_x = target_x - (total_width // 2) + 20
        start_y = target_y + self.y - 10
        
        # Blank of paper
        combined_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        
        current_x = 0
        text_y_offset = (total_height - text_surface.get_height()) // 2
        combined_surface.blit(text_surface, (current_x, text_y_offset))
        
        if self.image:
            img_y_offset = (total_height - self.image.get_height()) // 2
            combined_surface.blit(self.image, (current_x + text_surface.get_width(), img_y_offset))
            current_x += self.image.get_width() + spacing
        
        alpha_mask = pygame.Surface(combined_surface.get_size(), pygame.SRCALPHA)
        alpha_mask.fill((255, 255, 255, self.alpha))
        combined_surface.blit(alpha_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        surface.blit(combined_surface, (start_x, start_y))

class DamageNumber(TextMessage):
    def __init__(self, x, y, amount, color=(255, 0, 0)):
        super().__init__(text="", amount=amount, color=color, lifetime=30, speed=2)
        self.world_x = x
        self.world_y = y
        
class Notification(TextMessage):
    def __init__(self, text, image, color=(255, 255, 255)):
        super().__init__(text=text, amount="", image=image, color=color, lifetime=90, speed=1)