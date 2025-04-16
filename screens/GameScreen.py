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
from screens.utility import center_text

class GameScreen:
    def __init__(self, app):
        file_id = int(world.TILE_MAP / 8)
        pyxel.load(f"map/{file_id}.pyxres") # load when the game start, so you can make more map and base on that to write the specific pyxres file
        self.app = app
        
        self.world = World(pyxel.tilemap(world.TILE_MAP % 8))  # Initialize World with TILE_MAP id
        self.player = Player(self.world)
        self.skills = Skills(self.player)
        self.enemies = None
        self.time_limit = 30
        if self.app.mode[0] == "Trackers":
            self.skills.skills["invincible"].cooldown = 40 * FPS
            self.enemies = Trackers(self.player)
        elif self.app.mode[0] == "Balls":
            self.enemies = Balls(self.player)
        
        if self.app.mode[1] == "TimeLimit":
            self.enemies.initial_velocity *= 1.5
            self.enemies.spawn_timer /= 2
            
        
        self.score = 0 #init the score 
        self.font = pygame.font.Font(None, 14)  # Default font
        self.keys_for_skills = []
        for key in self.skills.skills.values():
            self.keys_for_skills.append(key.key)
        self.pause = False
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_P): # for pausing
            self.pause = not self.pause
        if pyxel.btnp(pyxel.KEY_TAB):
            self.app.change_screen("MapOptionScreen")
        if self.pause == True:
            return
        
        self.score += 1
        
        #player
        self.player.update()
                
        #enemies
        if self.app.mode[0] == "Trackers":
            self.enemies.update_trackers()
        elif self.app.mode[0] == "Balls":
            self.enemies.update_balls() # for balls
            
        #skills
        for key in self.keys_for_skills:
            if pyxel.btn(key):
                self.skills.activate_skill(key)
        self.skills.update()
        
        #health bar
        if(self.player.health_bar <= 0):
            self.app.change_screen("LostScreen")
                    
        #mode
        if self.app.mode[1] == "TimeLimit":
            if self.score >= FPS * self.time_limit: # clear game if survive more than 30 seconds
                self.app.change_screen("WinScreen")

    def draw(self):
        pyxel.cls(0)
        
        for y in range(self.world.HEIGHT):
            for x in range(self.world.WIDTH):
                world_item = self.world.world_map[y][x]
                world_item_draw(x, y, world_item)

        pyxel.blt(self.player.x, self.player.y, self.player.img,
                      WorldItem.PLAYER[0] * TILE_SIZE, WorldItem.PLAYER[1] * TILE_SIZE,
                      self.player.WIDTH, self.player.HEIGHT) # for player
        draw_player_health_bar(self.player.max_health, self.player.health_bar)
        draw_skill_image(self.skills)
        
        if self.app.mode[0] == "Trackers":
            self.enemies.draw_trackers()
        elif self.app.mode[0] == "Balls":
            self.enemies.draw_balls() # for balls
            
        #score
        self.render_score()
        
        #for pausescreen
        if self.pause == True:
            draw_pause_screen()
        
    def render_score(self):
        #Score text with pygame
        if self.app.mode[1] == "Survival":
            display_score = self.score
            score_text = self.font.render(f"Score: {display_score}", False, (255, 255, 255))  # White text
        elif self.app.mode[1] == "TimeLimit":
            display_score = self.time_limit - int(self.score / FPS) # display time until clear map
            score_text = self.font.render(f"Game cleared in: {display_score}", False, (255, 255, 255))  # White text
            
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
                    pyxel.pset(x_pos + x, y_pos + y, 7)  # 7 = White

def draw_player_health_bar(max_hp, hp):
    total = pyxel.width / 4
    x = total/max_hp
    y = 10
    pyxel.rect(0, 290 - y, hp*x, y, 9)

def draw_skill_image(skills : Skills):
    x = pyxel.width / 4 + 10
    for skill in skills.skills.values():
        if skill.current_cooldown <= 0:
            img_x, img_y = skill.image  # Unpack tuple
            pyxel.blt(x, 290 - TILE_SIZE, 0, img_x * TILE_SIZE, img_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Draw 8x8 sprite
             # Ensure text is visible
        text_x = x  
        text_y = 290 - TILE_SIZE 
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