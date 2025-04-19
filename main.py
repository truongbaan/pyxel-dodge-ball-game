# main.py
import pyxel
import pygame
from config import FPS
from screens.MainMenuScreen import MainMenuScreen
from screens.GuideScreen import GuideScreen
from screens.MapOptionScreen import MapOptionScreen
from screens.GameScreen import GameScreen
from screens.LostScreen import LostScreen
from screens.GameModeScreen import GameModeScreen
from screens.WinScreen import WinScreen
from screens.HighScoreScreen import HighScoreScreen
from screens.MultiplayerScreen import MultiplayerScreen
from screens.ChallengeScreen import ChallengeScreen
from screens.PVEScreen import PVEScreen
from screens.LoseToAiScreen import LostToAiScreen
from screens.WinToAiScreen import WinToAiScreen

from score import load_scores

class App:
    def __init__(self):
        #256, 260
        pygame.init()
        pyxel.init(256, 290,display_scale=2, fps=FPS)
        
        self.mode = ["Balls","Survival"] # first one is for enemy type, second one is for Game type
        self.current_screen = "MainMenuScreen"  # Use an instance variable instead
        self.last_score = 0
        self.last_screen = ""
        self.score_list = []
        self.score_list = load_scores() #storing the score when first init
        
        #init this way so if there is any variable in the app that would be used in the screens, will be inited before
        self.screens = {
            "MainMenuScreen": MainMenuScreen(self),
            "GuideScreen": GuideScreen(self),
            "MapOptionScreen" : MapOptionScreen(self),
            "GameModeScreen" : GameModeScreen(self),
            "GameScreen" : None,
            "LostScreen" : None,
            "WinScreen": None,
            "HighScoreScreen": None,
            "MultiplayerScreen": None,
            "ChallengeScreen": None,
            "PVEScreen": None,
            "LostToAiScreen": None,
            "WinToAiScreen": None
            
        }

        pyxel.mouse(visible=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.screens[self.current_screen].update()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
    def draw(self):
        pyxel.cls(0)
        self.screens[self.current_screen].draw()

    def change_screen(self, new_screen):
        print("Change to screen: " + new_screen)
        """Function to switch screens"""
        
        if new_screen == "GameScreen":
            self.screens["GameScreen"] = GameScreen(self)  # Reinitialize with updated TILE_MAP
       
        if new_screen == "LostScreen":
            self.last_screen = self.current_screen
            self.last_score = self.screens[self.current_screen].score
            self.screens["LostScreen"] = LostScreen(self, self.last_score)  # Reinitialize with updated score
        
        if new_screen == "WinScreen":
            self.last_score = self.screens["GameScreen"].score
            self.screens["WinScreen"] = WinScreen(self, self.last_score)  # Reinitialize with updated score
        
        if new_screen == "HighScoreScreen":
            self.screens["HighScoreScreen"] = HighScoreScreen(self)  # Reinitialize with updated TILE_MAP
        
        if new_screen == "MultiplayerScreen":
            self.screens["MultiplayerScreen"] = MultiplayerScreen(self)  # Reinitialize with updated TILE_MAP
        
        if new_screen == "PVEScreen":
            self.screens["PVEScreen"] = PVEScreen(self)  # Reinitialize with updated TILE_MAP
        
        if new_screen == "ChallengeScreen":
            self.screens["ChallengeScreen"] = ChallengeScreen(self)  # Reinitialize with updated TILE_MAP
        
        if new_screen == "LostToAiScreen":
            self.last_screen = self.current_screen
            self.last_score = self.screens[self.current_screen].score
            self.screens["LostToAiScreen"] = LostToAiScreen(self, self.last_score)  # Reinitialize with updated score
        
        if new_screen == "WinToAiScreen":
            self.last_screen = self.current_screen
            self.last_score = self.screens[self.current_screen].score
            self.screens["WinToAiScreen"] = WinToAiScreen(self, self.last_score)  # Reinitialize with updated score
            
        
            
        if new_screen in self.screens:
            self.current_screen = new_screen

if __name__ == "__main__":
    App()
