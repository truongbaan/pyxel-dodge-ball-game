# screens/game.py
import pyxel
import models.world as world
from models.world import World, world_item_draw, TILE_SIZE, WorldItem # Import from models
from models.player import Player
from models.ball import Balls
from models.skill import Skills
from config import FPS
from screens.MapOptionScreen import MAP_AMOUNT
import random

from screens.utility import draw_player_health_bar, draw_skill_image, draw_pause_screen, render_score

class MultiplayerScreen:
    def __init__(self, app):
        world.TILE_MAP = random.randrange(0, MAP_AMOUNT)
        file_id = int(world.TILE_MAP / 8)
        pyxel.load(f"map/{file_id}.pyxres") # load when the game start, so you can make more map and base on that to write the specific pyxres file
        self.app = app
        self.world = World(pyxel.tilemap(world.TILE_MAP % 8))  # Initialize World with TILE_MAP id
        self.players = [
            Player(self.world,5, [pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_KP_7, pyxel.KEY_KP_8, pyxel.KEY_KP_9]),
            Player(self.world,5, [pyxel.KEY_A, pyxel.KEY_D, pyxel.KEY_W, pyxel.KEY_S, pyxel.KEY_C, pyxel.KEY_V, pyxel.KEY_B])
        ]
        
        self.skills = [] #skills
        for player in self.players:
            self.skills.append(Skills(player))
        
        for skill_set in self.skills:
            for skill in skill_set.skills.values():
                skill.cooldown = int(skill.cooldown * 1.5)
            
        #init enemy
        self.enemies = Balls(self.players)
        self.enemies.initial_velocity = int(self.enemies.initial_velocity * 0.75)
        self.enemies.spawn_timer = int(self.enemies.spawn_timer / 3)
        
        self.score = 0 #init the score 
    
        self.pause = True
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_P): # for pausing
            self.pause = not self.pause
        if pyxel.btnp(pyxel.KEY_TAB):
            self.app.change_screen("MainMenuScreen")
        if self.pause == True:
            return
        
        self.score += 0.5
        
        players = []
        #remove dead player
        for player in self.players:
            if player.health_bar > 0:
                players.append(player)
        self.enemies.players = players
        
        #player
        for player in self.players:
            player.update()
        
        #enemies
        self.enemies.start_position_x = random.choice([10, pyxel.width - 10])
        self.enemies.start_position_y = random.choice([10, pyxel.height - 10])
        self.enemies.update_balls()
        
        #skill
        for skill_set in self.skills:
            for skill in skill_set.skills.values():
                if pyxel.btn(skill.key):
                    skill_set.activate_skill(skill.key)

        
        for skill in self.skills: #update time and cooldown
            skill.update()
        
        still_playing = False
        #health bar
        for player in self.players:
            if player.health_bar > 0:
                still_playing = True
                break
        if not still_playing:
            self.app.change_screen("LostScreen") # end when both die 
                    
                    
    def draw(self):
        pyxel.cls(0)
        
        for y in range(self.world.HEIGHT):
            for x in range(self.world.WIDTH):
                world_item = self.world.world_map[y][x]
                world_item_draw(x, y, world_item)

        #draw player
        for index, player in enumerate(self.players):
            if player.health_bar > 0:
                pyxel.text(player.x, player.y - TILE_SIZE, f"P{index+1}", 9)
                pyxel.blt(player.x, player.y, player.img,
                        WorldItem.PLAYER[0] * TILE_SIZE, WorldItem.PLAYER[1] * TILE_SIZE,
                        player.WIDTH, player.HEIGHT)
        
        #draw player health bar
        y = 10
        for player in self.players:
            draw_player_health_bar(player.max_health, player.health_bar, y)
            y += 20
        
        #draw skills image
        y = 0
        for skill in self.skills:
            draw_skill_image(skill, y)
            y += TILE_SIZE * 2
        
        self.enemies.draw_balls()
            
        #score
        render_score(self.score)
        
        #for pausescreen
        if self.pause == True:
            draw_pause_screen()
        
    