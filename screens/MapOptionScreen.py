import pyxel
from models.button import Button
import models.world as world

MAP_AMOUNT = 24
SCROLL_SPEED = 10  # Adjust scrolling speed
ORANGE = 7

#This is for map choosing
class MapOptionScreen:
    def __init__(self, app):
        self.app = app
        self.num_buttons = MAP_AMOUNT # total number of button
        self.buttons_per_row = 4 # number per rows
        self.button_height_percentage = 0.15 # for balance
        self.button_spacing_percentage = 0.02 # for balance
        self.row_spacing_percentage = 0.1 # for balance
        self.start_y_percentage = 0.2 # for balance

        self.button_height = int(pyxel.height * self.button_height_percentage)
        self.button_spacing = int(pyxel.width * self.button_spacing_percentage)
        self.row_spacing = int(pyxel.height * self.row_spacing_percentage)
        self.start_y = int(pyxel.height * self.start_y_percentage)

        self.available_width = pyxel.width - (self.buttons_per_row - 1) * self.button_spacing
        self.button_width = self.available_width // self.buttons_per_row

        self.scroll_y = 0  # Offset for scrolling
        
        self.buttons = []
        for i in range(self.num_buttons):
            row = i // self.buttons_per_row
            col = i % self.buttons_per_row
            x = (pyxel.width - (self.buttons_per_row * self.button_width + (self.buttons_per_row - 1) * self.button_spacing)) // 2 + col * (self.button_width + self.button_spacing) + pyxel.width * 0.01
            y = self.start_y + row * (self.button_height + self.row_spacing)
            if self.app.score_list[i][2] == 1:
                self.buttons.append(Button(x, y, self.button_width, self.button_height, i, i+1, ORANGE))
            else: self.buttons.append(Button(x, y, self.button_width, self.button_height, i, i+1))

        self.back_button = Button(0,0, 30, 15, "MainMenuScreen", "Back")
        pyxel.mouse(True)
       

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.back_button.is_clicked(pyxel.mouse_x, pyxel.mouse_y):
                self.app.change_screen(self.back_button.get_id())
            for button in self.buttons:
                # Adjust mouse click detection with scroll offset
                if button.is_clicked(pyxel.mouse_x, pyxel.mouse_y + self.scroll_y):
                    world.TILE_MAP = button.get_id()
                    self.app.change_screen("GameScreen")
        
        # Mouse wheel scrolling
        scroll_direction = pyxel.mouse_wheel
        if scroll_direction != 0:
            self.scroll_y -= scroll_direction * SCROLL_SPEED

        # Clamp scrolling
        max_scroll = max(0, self.buttons[-1].y + self.button_height - pyxel.height)
        self.scroll_y = max(0, min(self.scroll_y, max_scroll))


    def draw(self):
        pyxel.cls(0)
        
        for button in self.buttons:
            if 20 <= button.y - self.scroll_y < pyxel.height:
                button.y -= self.scroll_y  # Apply scrolling effect
                button.draw()
                button.y += self.scroll_y  # Reset position to avoid permanent shift
                
        pyxel.text(int(pyxel.width / 2) - 4, 10, "Map", 9)
        self.back_button.draw()