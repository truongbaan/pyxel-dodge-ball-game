# screens/game.py
import pyxel
import models.world as world
from models.world import World, world_item_draw, TILE_SIZE, WorldItem # Import from models
from models.player import Player
from models.ball import Balls
from models.tracker import Trackers
from models.skill import Skills
import pygame
from config import FPS
from screens.MapOptionScreen import MAP_AMOUNT
import random
from screens.utility import center_text

class ChallengeScreen:
    def __init__(self, app):
        world.TILE_MAP = random.randrange(0, MAP_AMOUNT)
        file_id = int(world.TILE_MAP / 8)
        pyxel.load(f"map/{file_id}.pyxres") # load when the game start, so you can make more map and base on that to write the specific pyxres file
        self.app = app
        self.world = World(pyxel.tilemap(world.TILE_MAP % 8))  # Initialize World with TILE_MAP id
        self.player = Player(self.world,6)
        
        self.skills = Skills(self.player)
        
        for skill in self.skills.skills.values():
            skill.cooldown = int(skill.cooldown / 2)
            
        #init enemy
        self.enemies = [
            Balls(self.player),
            Trackers(self.player)
        ]
        
        #diff increase
        for enemies in self.enemies:
            enemies.initial_velocity = int(enemies.initial_velocity * 1.1)
            enemies.spawn_timer = int(enemies.spawn_timer / 2)
        
        self.score = 0 #init the score 
        self.font = pygame.font.Font(None, 14)  # Default font
    
        self.pause = True
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_P): # for pausing
            self.pause = not self.pause
        if pyxel.btnp(pyxel.KEY_TAB):
            self.app.change_screen("MainMenuScreen")
        if self.pause == True:
            return
        
        #score increase
        self.score += 1

        #player update
        self.player.update()
        
        #enemies
        for enemies in self.enemies:
            if isinstance (enemies, Balls):
                enemies.update_balls()
            if isinstance (enemies, Trackers):
                enemies.update_trackers()
        
        #skill
        for skill in self.skills.skills.values():
            if pyxel.btn(skill.key):
                self.skills.activate_skill(skill.key)
        self.skills.update()
        
        if self.player.health_bar <= 0:
            self.app.change_screen("LostScreen") # end when both die (for testing now, will change to when 1 alive later)
                    
                    
    def draw(self):
        pyxel.cls(0)
        
        for y in range(self.world.HEIGHT):
            for x in range(self.world.WIDTH):
                world_item = self.world.world_map[y][x]
                world_item_draw(x, y, world_item)

        #draw player
        player = self.player
        pyxel.blt(player.x, player.y, player.img,
                WorldItem.PLAYER[0] * TILE_SIZE, WorldItem.PLAYER[1] * TILE_SIZE,
                player.WIDTH, player.HEIGHT)
        
        #draw player health bar
        draw_player_health_bar(player.max_health, player.health_bar, 10)
        
        #draw skills image
        draw_skill_image(self.skills, 0)

        #draw enemies
        for enemies in self.enemies:
            if isinstance (enemies, Balls):
                enemies.draw_balls()
            if isinstance (enemies, Trackers):
                enemies.draw_trackers()
            
        #score
        self.render_score()
        
        #for pausescreen
        if self.pause == True:
            draw_pause_screen()
        
    def render_score(self):
        #Score text with pygame
        display_score = self.score
        score_text = self.font.render(f"Score: {display_score}", False, (255, 255, 255))  # White text
            
        text_surface = pygame.Surface(score_text.get_size(), pygame.SRCALPHA)
        text_surface.blit(score_text, (0, 0))
        img_width, img_height = text_surface.get_size()
        
        padding = 2  # Padding from screen edges

        # Calculate bottom-right position
        x_pos = pyxel.width - img_width - padding  # Right aligned
        y_pos = pyxel.height - img_height  # Bottom aligned

        # Draw text pixel-by-pixel
        for y in range(img_height):
            for x in range(img_width):
                r, g, b, a = text_surface.get_at((x, y))  # Get RGBA values
                if a > 0:  # Only draw non-transparent pixels
                    pyxel.pset(x_pos + x, y_pos + y, 7)  # White color

def draw_player_health_bar(max_hp, hp, y):
    total = pyxel.width / 4
    x = total/max_hp
    pyxel.rect(0, 290 - y, hp*x, 10, 9)

def draw_skill_image(skills : Skills, y):
    x = pyxel.width / 4 + 10
    for skill in skills.skills.values():
        if skill.current_cooldown <= 0:
            img_x, img_y = skill.image  # Unpack tuple
            pyxel.blt(x, 290 - TILE_SIZE - y, 0, img_x * TILE_SIZE, img_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Draw 8x8 sprite
            # Ensure text is visible
        text_x = x  
        text_y = 290 - TILE_SIZE - y
        if skill.current_active_time > 0:  # Avoid negative values
            pyxel.text(text_x,text_y - 6, "Active:", 7)
            pyxel.text(text_x, text_y, str(int(skill.current_active_time/FPS)), 7)
        if skill.current_cooldown > 0 and skill.current_active_time <= 0: 
            pyxel.text(text_x,text_y - 6, "Cooldown:", 8)
            pyxel.text(text_x, text_y, str(int(skill.current_cooldown/FPS)), 8)
        x+= TILE_SIZE * 4

def draw_pause_screen():
    for y in range(0, pyxel.height, 5):
        for x in range(0, pyxel.width, 5):
            pyxel.pset(x, y, 5) #draw 
    center_text("Pause", pyxel.height/2 - 4 * 5, 9)
    center_text(f"MAP PLAYING: {int(world.TILE_MAP / 8)} and {world.TILE_MAP % 8}", pyxel.height/2 - 4 * 3, 9)