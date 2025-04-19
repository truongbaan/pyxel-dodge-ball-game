#this is the start screen of All
import pyxel
from models.button import Button
from screens.utility import center_text

class MainMenuScreen:
    def __init__(self, app):
        self.app = app
        self.buttons = [  # Opening bracket here
            Button(40 + int(pyxel.width /10), 10 + int(pyxel.height /5), 110, 20, "MapOptionScreen", "Select map"),
            Button(40 + int(pyxel.width /10), 35 + int(pyxel.height /5), 35, 30, "GuideScreen", "Guide"),
            Button(80 + int(pyxel.width /10), 35 + int(pyxel.height /5), 70, 30, "GameModeScreen", "Game Mode"),
            Button(40 + int(pyxel.width /10), 70 + int(pyxel.height /5), 45, 40, "HighScoreScreen", "High Score"),
            Button(90 + int(pyxel.width /10), 70 + int(pyxel.height /5), 60, 40, "ChallengeScreen", "Challenge"),
            Button(40 + int(pyxel.width /10), 115 + int(pyxel.height/5),110,30, "MultiplayerScreen", "Multiplay"),
            Button(40 + int(pyxel.width /10), 150 + int(pyxel.height/5),110,25, "PVEScreen", "PVE"),
            Button(40 + int(pyxel.width /10), 180 + int(pyxel.height/5), 110, 40, "Quit")
        ]  # Closing bracket here
        pyxel.mouse(visible=True)
        
    
    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for button in self.buttons:
                if button.is_clicked(pyxel.mouse_x, pyxel.mouse_y):
                    if(button.get_id() == "Quit"):
                        pyxel.quit()
                    self.app.change_screen(button.get_id())
    
    def draw(self):
        pyxel.cls(0)
        center_text("Dodge Balls",int(pyxel.height/5),  9)
        for button in self.buttons:
            button.draw()