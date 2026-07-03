# src/world/tiled.py
import pygame
import pytmx

class TiledMap:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        
        # Store single tile dimensions for convenience
        self.tilewidth = self.tmx_data.tilewidth
        self.tileheight = self.tmx_data.tileheight

    def draw(self, surface, camera_x, camera_y):
        """Draw only the tiles currently visible on screen — fast and camera-aware."""
        screen_w, screen_h = surface.get_size()

        # Calculate which tiles are visible in the current viewport
        start_col = max(0, int(camera_x // self.tilewidth))
        end_col = min(self.tmx_data.width, int((camera_x + screen_w) // self.tilewidth) + 1)
        
        start_row = max(0, int(camera_y // self.tileheight))
        end_row = min(self.tmx_data.height, int((camera_y + screen_h) // self.tileheight) + 1)

        # Iterate over all visible map layers
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                
                for row in range(start_row, end_row):
                    for col in range(start_col, end_col):
                        
                        # Fetch the GID from the tile layer data
                        tile_image = layer.data[row][col] # دي الطريقة الأسرع والأضمن في بايثون لجلب المربع من الـ Layer
                        # Alternative: self.tmx_data.get_tile_image(col, row, layer)
                        
                        # Resolve the GID to an actual tile image
                        gid = layer.data[row][col]
                        if gid:
                            tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                            
                            if tile_image:
                                world_x = col * self.tilewidth
                                world_y = row * self.tileheight
                                
                                draw_x = world_x - camera_x
                                draw_y = world_y - camera_y
                                
                                surface.blit(tile_image, (draw_x, draw_y))