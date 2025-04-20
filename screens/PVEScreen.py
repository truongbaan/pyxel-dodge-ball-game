# screens: PVESScreen
import pyxel
from models.world import World, world_item_draw, TILE_SIZE, WorldItem # Import from models
from models.player import Player
from models.AIplayer import AIPlayer
from models.ball import Balls
from models.skill import Skills
from config import FPS
import random
from screens.utility import draw_player_health_bar, draw_skill_image, draw_pause_screen, render_score

#AI gaming
class PVEScreen:
    def __init__(self, app):
        self.app = app
        #const map 17
        pyxel.load(f"map/2.pyxres") 
        self.world = World(pyxel.tilemap(0))  
        
        self.players = [
            Player(self.world, 10, [pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_A, pyxel.KEY_S, pyxel.KEY_D]),
            AIPlayer(self.world,10)
        ]
        
        self.skills = [] #skills
        for player in self.players:
            if isinstance(player, AIPlayer): continue # AI cant do skill yet
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
        
        self.score += 1
        
        
        players = []
        #remove dead player
        for player in self.players:
            if player.health_bar > 0:
                players.append(player)
        self.enemies.players = players
        
        #player
        for player in self.players:
            if type(player) is AIPlayer:
                player.update(self.enemies)
                if self.score % 1000 == 0:
                    player.change_target((random.randint(40, 240), random.randint(40, 240)))
                    continue
            elif type(player) is Player:
                player.update()
        
        #enemies
        self.enemies.start_position_x = random.choice([10, pyxel.width - 10])
        self.enemies.start_position_y = random.choice([10, pyxel.height - 10])
        self.enemies.update_balls()
        
        #skill
        
        for skill_set in self.skills:
            if skill_set.player.health_bar <= 0:
                continue  # skip dead player
            for skill in skill_set.skills.values():
                if pyxel.btn(skill.key):
                    skill_set.activate_skill(skill.key)

        
        for skill in self.skills: #update time and cooldown
            skill.update()
        
        player_win, ai_win = False, False
        #health bar
        for player in self.players:
            if player.health_bar <= 0 and type(player) is AIPlayer:
                player_win = True
                break
            elif player.health_bar <= 0 and type(player) is Player:
                ai_win = True
                break
            
        if player_win:
            self.app.change_screen("WinToAiScreen") # to win the bot, so cool! 
        elif ai_win:
            self.app.change_screen("LostToAiScreen") # you just lose to a bot
                    
                    
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
        