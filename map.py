import pygame

class Map:
    def __init__(self):
        pass

    def create_map(self, player, map_objects):
        LIGHT_GREEN_GROUND_X = 30
        LIGHT_GREEN_GROUND_Y = 28
        LIGHT_GREEN_GROUND_W = 20
        LIGHT_GREEN_GROUND_H = 25

        DESERT_GROUND_X = 97
        DESERT_GROUND_Y = 0
        DESERT_GROUND_W = 16
        DESERT_GROUND_H = 34

        DESERT_ROCKS_GROUND_1_X = 112
        DESERT_ROCKS_GROUND_1_Y = 0
        DESERT_ROCKS_GROUND_1_W = 16
        DESERT_ROCKS_GROUND_1_H = 34

        DESERT_ROCKS_GROUND_2_X = 127
        DESERT_ROCKS_GROUND_2_Y = 0
        DESERT_ROCKS_GROUND_2_W = 16
        DESERT_ROCKS_GROUND_2_H = 34

        DESERT_ROCKS_GROUND_3_X = 144
        DESERT_ROCKS_GROUND_3_Y = 0
        DESERT_ROCKS_GROUND_3_W = 16
        DESERT_ROCKS_GROUND_3_H = 34

        DESERT_ROCKS_GROUND_4_X = 96
        DESERT_ROCKS_GROUND_4_Y = 30
        DESERT_ROCKS_GROUND_4_W = 32
        DESERT_ROCKS_GROUND_4_H = 18

        DESERT_ROCKS_GROUND_5_X = 126
        DESERT_ROCKS_GROUND_5_Y = 32
        DESERT_ROCKS_GROUND_5_W = 19
        DESERT_ROCKS_GROUND_5_H = 15

        light_green_ground = None
        desert_ground = None
        desert_rock_ground_1 = None
        desert_rock_ground_2 = None
        desert_rock_ground_3 = None
        desert_rock_ground_4 = None
        desert_rock_ground_5 = None

        ###########################################################
        ### ._draw_(X, Y, player.x, player.y, world_x, world_y) ###
        ###########################################################
        ### X, Y, Width, Height <== cut the Image  
        ### player.x, player.y <=== screen coordinates
        ### world_x, world_y <===== for position the tile on the world

        light_green_ground = map_objects[0]
        desert_ground = map_objects[0]
        desert_rock_ground_1 = map_objects[0]
        desert_rock_ground_2 = map_objects[0]
        desert_rock_ground_3 = map_objects[0]
        desert_rock_ground_4 = map_objects[0]
        desert_rock_ground_5 = map_objects[0]

        light_green_ground._draw_(
            LIGHT_GREEN_GROUND_X, LIGHT_GREEN_GROUND_Y, LIGHT_GREEN_GROUND_W, LIGHT_GREEN_GROUND_H, 
            player.x, player.y, 
            1000, 1000, 
            scale=True, new_width=75, new_height=75)
        
        desert_ground._draw_(
            DESERT_GROUND_X, DESERT_GROUND_Y, DESERT_GROUND_W, DESERT_GROUND_H, 
            player.x, player.y, 
            1100, 1100, 
            scale=True, new_width=50, new_height=75)
        
        desert_rock_ground_1._draw_(
            DESERT_ROCKS_GROUND_1_X, DESERT_ROCKS_GROUND_1_Y, DESERT_ROCKS_GROUND_1_W, DESERT_ROCKS_GROUND_1_H, 
            player.x,player.y, 
            1200, 1200, 
            scale=True, new_width=50, new_height=75)
        
        desert_rock_ground_2._draw_(
            DESERT_ROCKS_GROUND_2_X, DESERT_ROCKS_GROUND_2_Y, DESERT_ROCKS_GROUND_2_W, DESERT_ROCKS_GROUND_2_H, 
            player.x,player.y, 
            1300, 1300, 
            scale=True, new_width=50, new_height=75)
        
        desert_rock_ground_3._draw_(
            DESERT_ROCKS_GROUND_3_X, DESERT_ROCKS_GROUND_3_Y, DESERT_ROCKS_GROUND_3_W, DESERT_ROCKS_GROUND_3_H, 
            player.x,player.y, 
            1400, 1400, 
            scale=True, new_width=50, new_height=75)
        
        desert_rock_ground_4._draw_(
            DESERT_ROCKS_GROUND_4_X, DESERT_ROCKS_GROUND_4_Y, DESERT_ROCKS_GROUND_4_W, DESERT_ROCKS_GROUND_4_H, 
            player.x,player.y, 
            1500, 1500, 
            scale=True, new_width=50, new_height=75)
        
        desert_rock_ground_5._draw_(
            DESERT_ROCKS_GROUND_5_X, DESERT_ROCKS_GROUND_5_Y, DESERT_ROCKS_GROUND_5_W, DESERT_ROCKS_GROUND_5_H, 
            player.x,player.y, 
            1600, 1600, 
            scale=True, new_width=50, new_height=75)