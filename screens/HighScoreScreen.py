#this is used to present the highscore as well as cleared game for time limit challenge
import pyxel
from models.button import Button
SCROLL_SPEED = 10
BLUE = 12
class HighScoreScreen:
    def __init__(self, app):
        self.app = app
        self.scores = self.app.score_list
        self.buttons = []
        self.text_for_button = []
        for map_id, survival, timelimit in self.scores:
            self.text_for_button.append(f"{map_id + 1}          {survival}          {"Cleared" if timelimit == 1 else "Not Clear"}")

        self.button_height_percentage = 0.1 # for balance
        self.button_spacing_percentage = 0.02 # for balance
        self.start_y_percentage = 0.1 # for balance

        self.button_height = int(pyxel.height * self.button_height_percentage)
        self.row_spacing = int(pyxel.height * self.button_spacing_percentage)
        self.start_y = int(pyxel.height * self.start_y_percentage)

        self.scroll_y = 0  # Offset for scrolling
        
        self.buttons = []
        for i in range(len(self.text_for_button)):
            y = self.start_y + i * (self.button_height + self.row_spacing)
            self.buttons.append(Button(int(pyxel.width * 0.1), y, int(pyxel.width * 0.8), self.button_height, i, self.text_for_button[i]))
        
        self.board = Button(int(pyxel.width * 0.1), 0, int(pyxel.width * 0.8),self.button_height, i, "Map Id       Survive Score       Time limit Clear", BLUE)
        self.back_button = Button(0, 0, 30, 15, "MainMenuScreen", "Back")
        pyxel.mouse(True)
        
    def update(self):
        # Mouse wheel scrolling
        scroll_direction = pyxel.mouse_wheel
        if scroll_direction != 0:
            self.scroll_y -= scroll_direction * SCROLL_SPEED

        # Clamp scrolling
        max_scroll = max(0, self.buttons[-1].y + self.button_height - pyxel.height)
        self.scroll_y = max(0, min(self.scroll_y, max_scroll))
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.back_button.is_clicked(pyxel.mouse_x, pyxel.mouse_y):
                self.app.change_screen(self.back_button.get_id())
    
    def draw(self):
        pyxel.cls(0)
        for button in self.buttons:
            if 0 <= button.y - self.scroll_y < pyxel.height:
                button.y -= self.scroll_y  # Apply scrolling effect
                button.draw()
                button.y += self.scroll_y  # Reset position to avoid permanent shift
        self.back_button.draw()
        self.board.draw()