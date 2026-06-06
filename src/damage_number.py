import pygame
import random

class DamageNumber:
    """⚡ FLOATING DAMAGE TEXT ENGINE
    Spawns a rendering string at a vector coordinate, drifts upward,
    and handles automatic alpha transparency decay over its life cycle.
    """
    def __init__(self, x, y, amount, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.amount = str(amount)
        self.color = color
        
        # Setup drift vectors & longevity states
        self.vertical_speed = 1.5   # Pixels climbed per frame
        self.lifetime = 45          # Total frames this element remains alive
        self.alpha = 255            # Starting opacity
        
        # Initialize internal font rendering configuration
        # Fallback to system font if your project assets don't have custom TTF paths
        self.font = pygame.font.SysFont("Arial", 26, bold=True)

    def update(self):
        """Drifts the tracking position upward and fades transparency levels."""
        self.y -= self.vertical_speed
        self.lifetime -= 1
        
        # Calculate percentage decay rate to lower alpha cleanly
        if self.lifetime < 15:
            self.alpha = max(0, int((self.lifetime / 15) * 255))
            
        return self.lifetime <= 0  # Returns True when dead to flag deletion

    def draw(self, surface, camera_x, camera_y):
        """Renders the text to surface while maintaining alpha capabilities."""
        # ⚠️ Note: standard font render layers do not support alpha directly in Pygame.
        # We must blit the font onto a temporary alpha-capable subsurface first!
        text_surface = self.font.render(self.amount, True, self.color)
        
        # Create an empty surface matching the text frame size that accepts alpha adjustments
        alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, self.alpha)) # Match alpha setting
        
        # Composite text texture elements over transparency surface matrix configurations
        alpha_surface.blit(text_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Blit text to screen accounting for current virtual camera viewport offsets
        surface.blit(alpha_surface, (self.x - camera_x, self.y - camera_y))