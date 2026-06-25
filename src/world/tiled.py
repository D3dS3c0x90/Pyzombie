# src/world/tiled.py
import pygame
import pytmx

class TiledMap:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        
        # حفظ أبعاد المربع الواحد للسهولة
        self.tilewidth = self.tmx_data.tilewidth
        self.tileheight = self.tmx_data.tileheight

    def draw(self, surface, camera_x, camera_y):
        """🖌️ رسم المربعات اللي باينة على الشاشة بس بكود متوافق وسريع جداً"""
        screen_w, screen_h = surface.get_size()

        # حساب المربعات المرئية حالياً
        start_col = max(0, int(camera_x // self.tilewidth))
        end_col = min(self.tmx_data.width, int((camera_x + screen_w) // self.tilewidth) + 1)
        
        start_row = max(0, int(camera_y // self.tileheight))
        end_row = min(self.tmx_data.height, int((camera_y + screen_h) // self.tileheight) + 1)

        # اللف على الطبقات
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                
                for row in range(start_row, end_row):
                    for col in range(start_col, end_col):
                        
                        # ✨ التعديل السحري هنا: بنادي get_tile_image_by_gid مباشرة وبنبعت الـ layer نفسه للـ layer object!
                        tile_image = layer.data[row][col] # دي الطريقة الأسرع والأضمن في بايثون لجلب المربع من الـ Layer
                        # أو باستخدام الدالة دي لو التانية منعتك: tile_image = self.tmx_data.get_tile_image(col, row, layer)
                        
                        # لو السطر اللي فوق ضايقك، البديل الأضمن والأسرع في المكتبة هو سحب الـ GID مباشرة:
                        gid = layer.data[row][col]
                        if gid:
                            tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                            
                            if tile_image:
                                world_x = col * self.tilewidth
                                world_y = row * self.tileheight
                                
                                draw_x = world_x - camera_x
                                draw_y = world_y - camera_y
                                
                                surface.blit(tile_image, (draw_x, draw_y))