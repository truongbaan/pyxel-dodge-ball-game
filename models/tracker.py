#similar to tracker, but instead of moving in 1 direction and bouncing, just move straight to the player
# this will sspawn 1 random 4 corner, slow speed but no disappear

import math
import random
import pyxel
from config import FPS
from models.player import Player

class Tracker:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = 2  # Each tracker has its own radius

    def update(self, player : Player):
        angle_radians = calculate_angle(self.x, self.y, player.x, player.y)
        
        self.x += self.velocity * math.cos(angle_radians)  # Move in X direction
        self.y += self.velocity * math.sin(angle_radians)  # Move in Y direction

    def collides_with(self, player: Player):
        """Returns True if the tracker collides with the player."""
        distance = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
        return distance < (self.radius + player.radius)  # Collision condition
    
class Trackers:
    def __init__(self, player: Player):
        self.initial_velocity = player.DX * 0.6
        self.spawn_timer = int(FPS * 2.5)
        self.trackers = []
        self.buff_count = 0
        self.player = player
        self.current_time = 0

    def create_tracker(self):
        spawn_positions = [
            (0, 0), (pyxel.width, 0),
            (0, pyxel.height), (pyxel.width, pyxel.height)
        ]
        x, y = random.choice(spawn_positions)

        print(f"Spawning tracker at ({x}, {y})")  # Debugging output
        new_tracker = Tracker(x=x, y=y, velocity=self.initial_velocity)
        self.trackers.append(new_tracker)

    def update_trackers(self):
        self.current_time += 1
        
        if self.current_time >= self.spawn_timer:  
            self.create_tracker()
            if self.initial_velocity < self.player.DX:
                self.initial_velocity += self.player.DX * 0.02
            else: self.initial_velocity = self.player.DX
            self.current_time = 0

        # Update all trackers
        for tracker in self.trackers:
            tracker.update(self.player)

        # Remove trackers that collide with the player or have expired
        new_trackers = []
        for tracker in self.trackers:
            if tracker.collides_with(self.player):
                self.player.take_damage(1)
                continue  # Skip adding this tracker

            new_trackers.append(tracker)  # Keep valid trackers

        self.trackers = new_trackers  # Replace old list


    def draw_trackers(self):
        for tracker in self.trackers:
            pyxel.circ(round(tracker.x), round(tracker.y), tracker.radius, 8)  # Use tracker.radius instead of self.circle_radius

def calculate_angle(tracker_x, tracker_y, player_x, player_y):
    """Calculates the angle (in degrees) from the tracker to the player."""
    delta_x = player_x - tracker_x
    delta_y = player_y - tracker_y
    angle_radians = math.atan2(delta_y, delta_x)
    return angle_radians