from models.player import Player
from models.world import TILE_SIZE, World
import math
from models.ball import Balls
from models.tracker import Trackers

class AIPlayer(Player): #rule base type
    def __init__(self, world: World, health_bar = 3):
        self.world = world
        self.x = world.player_grid_x * TILE_SIZE
        self.y = world.player_grid_y * TILE_SIZE
        self.health_bar = health_bar
        self.max_health = self.health_bar # this could be used for healing skill later
        self.invincible = False
        self.img = 0 #init
        self.danger_zone_radius = 30 # Adjustable parameter
        self.target = (130,130)

    def update(self, cballs):
        if isinstance(cballs, Balls):
            balls =cballs.balls
        elif isinstance(cballs, Trackers):
            balls = cballs.trackers
        # Simple reactive avoidance
        move_x = 0
        move_y = 0
        for ball in balls:
            distance = math.sqrt((self.x - ball.x)**2 + (self.y - ball.y)**2)
            if distance < self.danger_zone_radius:
                # Move away from the ball
                direction_x = self.x - ball.x
                direction_y = self.y - ball.y
                # Normalize direction (optional but can help with smoother movement)
                magnitude = math.sqrt(direction_x**2 + direction_y**2)
                if magnitude > 0:
                    direction_x /= magnitude
                    direction_y /= magnitude
                move_x += direction_x
                move_y += direction_y

        
        
        # Try to move in the determined direction
        if move_x > 0:
            self.update_pos(1.2, 0)
        elif move_x < 0:
            self.update_pos(-1.2, 0)

        if move_y > 0:
            self.update_pos(0, 1.2)
        elif move_y < 0:
            self.update_pos(0, -1.2)
        
        #target 130
        target_dx = self.target[0] - self.x
        target_dy = self.target[1] - self.y
        target_magnitude = math.sqrt(target_dx**2 + target_dy**2)
        if target_magnitude > 0:
            target_dx /= target_magnitude
            target_dy /= target_magnitude
            # Add the target vector to movement
            target_move_x = target_dx
            target_move_y = target_dy
        if target_move_x > 0:
            self.update_pos(0.2, 0)
        elif target_move_x < 0:
            self.update_pos(-0.2, 0)

        if target_move_y > 0:
            self.update_pos(0, 0.2)
        elif target_move_y < 0:
            self.update_pos(0, -0.2)
            
    
    def take_damage(self, amount):
        self.health_bar -=amount
    
    def update_pos(self, x, y):
        new_self_x = self.x + x
        new_self_y = self.y + y
        if new_self_x > 0 and new_self_x + super().WIDTH < 260 - TILE_SIZE:
            self.x = new_self_x
        if new_self_y > 0 and new_self_y + super().HEIGHT < 260 - TILE_SIZE:
            self.y = new_self_y
        
        
        if self.y + super().HEIGHT > 260 - 5 - TILE_SIZE:
            self.y = 15
        if self.x + super().WIDTH > 260 - 5 - TILE_SIZE:
            self.x = 15
        if self.x <= super().WIDTH:
            self.x = 256 - 15 - TILE_SIZE
        if self.y <= super().HEIGHT:
            self.y = 260 - 15 -TILE_SIZE

    def change_target(self, num : list):
        self.target = num
