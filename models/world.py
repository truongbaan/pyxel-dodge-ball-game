TILE_SIZE = 8
SPRITE_BANK = 0
TILE_MAP = 0
import pyxel
#note: pyxel can only store 7 maps

class WorldItem:
    WALL = (4, 0)
    CORRIDOR = (0,0)
    PLAYER = (2,0)
    
class World:
    #each tile is 8x8
    player_grid_x = 1
    player_grid_y = 1
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.world_map = []
        self.HEIGHT = tilemap.height
        self.WIDTH = tilemap.width
        for y in range(self.HEIGHT):
            self.world_map.append([])
            for x in range(self.WIDTH):
                if self.tilemap.pget(x, y) == WorldItem.WALL:
                    self.world_map[y].append(WorldItem.WALL)
                elif self.tilemap.pget(x, y) == WorldItem.PLAYER:
                    self.world_map[y].append(WorldItem.CORRIDOR)
                    self.player_grid_x = x
                    self.player_grid_y = y
                else:
                    self.world_map[y].append(WorldItem.CORRIDOR) 
                    
                    
def world_item_draw(x, y, world_item):
    pyxel.blt(x * TILE_SIZE,
                y * TILE_SIZE,
                SPRITE_BANK,
                world_item[0] * TILE_SIZE,
                world_item[1] * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
                )