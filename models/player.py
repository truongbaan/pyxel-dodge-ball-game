from models.world import WorldItem, TILE_SIZE, World
import pyxel

class Player:
    WIDTH = 8
    HEIGHT = 8
    radius = WIDTH/2
    DX = 0.5
    
    def __init__(self, world: World, health_bar = 3, key_list = [pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_A, pyxel.KEY_S, pyxel.KEY_D]):
        self.world = world
        self.x = world.player_grid_x * TILE_SIZE
        self.y = world.player_grid_y * TILE_SIZE
        self.health_bar = health_bar
        self.max_health = self.health_bar # this could be used for healing skill later
        self.invincible = False
        self.img = 0 #init
        self.key_list = key_list

        
    def move_left(self):
        self.img = 1
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        
        new_x = self.x - self.DX
        new_tile_x = tile_x - 1
        if new_tile_x < 0:
            return
        
        next_tile_up = self.world.world_map[tile_y][new_tile_x]
        next_tile_bottom = self.world.world_map[tile_y + 1][new_tile_x]
        
        if (
            next_tile_up == WorldItem.WALL and sprites_collide(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
            next_tile_bottom == WorldItem.WALL and sprites_collide(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
        ):
            return
        
        self.x -= self.DX
    
    def move_right(self):
        self.img = 0
        tile_y = int(self.y / TILE_SIZE)
        tile_x = int(self.x / TILE_SIZE)
        
        new_x = self.x + self.DX
        new_tile_x = tile_x + 1
        if new_tile_x >= len(self.world.world_map[0]):
            return
        
        next_tile_up = self.world.world_map[tile_y][new_tile_x]
        next_tile_bottom = self.world.world_map[tile_y + 1][new_tile_x]
        
        if (
            next_tile_up == WorldItem.WALL and sprites_collide(new_x, self.y, new_tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        ) or (
            next_tile_bottom == WorldItem.WALL and sprites_collide(new_x, self.y, new_tile_x * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
        ):
            return
        
        self.x += self.DX
    
    def move_up(self):
        tile_x = int(self.x / TILE_SIZE)
        tile_y = int(self.y / TILE_SIZE)
        
        new_y = self.y - self.DX
        new_tile_y = tile_y - 1
        if new_tile_y < 0:
            return
        
        next_tile_left = self.world.world_map[new_tile_y][tile_x]
        next_tile_right = self.world.world_map[new_tile_y][tile_x + 1]
        
        if (
            next_tile_left == WorldItem.WALL and sprites_collide(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) or (
            next_tile_right == WorldItem.WALL and sprites_collide(self.x, new_y, (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE)
        ):
            return
        
        self.y -= self.DX
    
    def move_down(self):
        tile_x = int(self.x / TILE_SIZE)
        tile_y = int(self.y / TILE_SIZE)
        
        new_y = self.y + self.DX
        new_tile_y = tile_y + 1
        if new_tile_y >= len(self.world.world_map):
            return
        
        next_tile_left = self.world.world_map[new_tile_y][tile_x]
        next_tile_right = self.world.world_map[new_tile_y][tile_x + 1]
        
        if (
            next_tile_left == WorldItem.WALL and sprites_collide(self.x, new_y, tile_x * TILE_SIZE, new_tile_y * TILE_SIZE)
        ) or (
            next_tile_right == WorldItem.WALL and sprites_collide(self.x, new_y, (tile_x + 1) * TILE_SIZE, new_tile_y * TILE_SIZE)
        ):
            return
        
        self.y += self.DX
        
    def take_damage(self, amount):
        if self.invincible == False:
            self.health_bar -=amount
    
    def update(self):
        #Movement and restriction
        if pyxel.btn(self.key_list[0]):
            if self.x > 0:
                self.move_left()
        if pyxel.btn(self.key_list[1]):
            if self.x + self.WIDTH < 256:
                self.move_right()
        if pyxel.btn(self.key_list[2]):
            if self.y > 0:
                self.move_up()
        if pyxel.btn(self.key_list[3]):
            if self.y + self.HEIGHT < 260:
                self.move_down()
        
    
        
def sprites_collide(x1, y1, x2, y2):
    if x1 + TILE_SIZE <= x2 or x2 + TILE_SIZE <= x1:
        return False
    
    if y1 + TILE_SIZE <= y2 or y2 + TILE_SIZE <= y1:
        return False
    
    return True
