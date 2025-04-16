from models.button import Button
import pyxel
import models.world as world
from score import save_score
from screens.utility import center_text
class LostScreen:
    def __init__(self, app, score: int):
        self.score = score
        self.app = app
        self.buttons = [
            Button(int(pyxel.width / 10), int(pyxel.height / 4), 60, 40, self.app.last_screen, "Restart"), #restart the game
            Button(int(pyxel.width / 2) + 60, int(pyxel.height / 4), 60, 40, "MainMenuScreen", "Main Menu"),
        ] 
        
        #score is saved in this order: (map number, survival score, cleared for time limit)
        self.map_id = world.TILE_MAP
        if self.app.score_list[self.map_id][1] < score:
            self.app.score_list[self.map_id][1] = score
            save_score(self.app.score_list)
    
    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for button in self.buttons:
                if button.is_clicked(pyxel.mouse_x, pyxel.mouse_y):
                    self.app.change_screen(button.id)
    
    def draw(self):
        pyxel.cls(0)
        center_text("You lost!", 10, 9)
        center_text("Your Score: " + f"{self.score}", 30 , 9)
        center_text("Your best score: " + f"{self.app.score_list[self.map_id][1]}",50, 9)
        for button in self.buttons:
            button.draw()
