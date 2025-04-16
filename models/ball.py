import math
import pyxel
import random
from config import FPS
from models.player import Player
from models.tracker import calculate_angle

RED = 8 

class Ball:
    def __init__(self, x, y, velocity, angle, lifetime):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.angle = angle
        self.lifetime = lifetime
        self.radius = 2  # Each ball has its own radius

    def update(self):
        self.x += self.velocity * math.cos(self.angle)
        self.y += self.velocity * math.sin(self.angle)

        # Reflecting off walls
        if self.x - self.radius < 0 or self.x + self.radius > pyxel.width:
            self.angle = math.pi - self.angle
        if self.y - self.radius < 0 or self.y + self.radius > pyxel.height:
            self.angle = -self.angle

        # Reduce lifetime
        self.lifetime -= 1

    def collides_with(self, player):
        """Returns True if the ball collides with the player."""
        distance = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
        return distance < (self.radius + player.radius)  # Collision condition

class Balls:
    def __init__(self, players: list[Player], color = RED):
        self.initial_velocity = 0.4
        self.spawn_timer = int(FPS * 2.5)
        self.balls = []
        self.buff_count = 0
        self.lifetime = FPS * 20  # Lifetime in frames (120 FPS = 20s)
        self.current_time = 0
        self.color = color
        # is list in both multiplayer and single
        if isinstance(players, Player):
            self.players = [players]  # Wrap single player in a list
        else:
            self.players = players
        self.start_position_x = 10
        self.start_position_y = 10
    def create_ball(self):
        random_person = random.randint(0, len(self.players) - 1) #random target a player to make start angle
        new_ball = Ball(
            x=self.start_position_x,
            y=self.start_position_y,
            velocity=self.initial_velocity,
            angle=calculate_angle(self.start_position_x, self.start_position_y, self.players[random_person].x, self.players[random_person].y),
            lifetime=self.lifetime
        )
        self.balls.append(new_ball)

    def update_balls(self):
        self.current_time += 1
            
        if self.current_time >= self.spawn_timer:  
            self.create_ball()
            self.current_time = 0
            self.buff_count += 1
            if self.buff_count > 1:
                self.initial_velocity += 0.1
                self.buff_count = 0

        # Update all balls
        for ball in self.balls:
            ball.update()

        # Remove balls that collide with the player or have expired
        new_balls = []
        for ball in self.balls:
            hit_player = False  # for ignore add ball that hit the player
    
            # Check collision
            for player in self.players:
                if ball.collides_with(player):
                    player.take_damage(1)
                    hit_player = True  
            
            if not hit_player and ball.lifetime > 0:
                new_balls.append(ball)

        self.balls = new_balls  # Replace old list


    def draw_balls(self):
        for ball in self.balls:
            pyxel.circ(round(ball.x), round(ball.y), ball.radius, self.color)  # draw the balls
