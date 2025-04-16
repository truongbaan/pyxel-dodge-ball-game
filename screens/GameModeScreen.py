from models.button import Button
import pyxel
from screens.utility import center_text

ORANGE = 9
GREEN = 11
class GameModeScreen:
    def __init__(self, app):
        self.app = app
 
        self.button_height_percentage = 0.15 # for balance
        self.button_spacing_percentage = 0.02 # for balance
        self.row_spacing_percentage = 0.1 # for balance
        

        self.button_height = int(pyxel.height * self.button_height_percentage)
        self.button_spacing = int(pyxel.width * self.button_spacing_percentage)
        self.row_spacing = int(pyxel.height * self.row_spacing_percentage)
        
        #enemy type buttons
        self.start_y = int(pyxel.height * 0.3)  
        self.enemy_type = ("Balls", "Trackers")
        self.enemy_text = ("Balls", "Trackers")
        self.available_width = pyxel.width - (len(self.enemy_type) - 1) * self.button_spacing
        self.button_width = self.available_width // len(self.enemy_type)
        
        
        self.enemy_buttons = []
        for i in range(len(self.enemy_type)):
            row = i // len(self.enemy_type)
            x = (pyxel.width - (len(self.enemy_type) * self.button_width + (len(self.enemy_type) - 1) * self.button_spacing)) // 2
            x += i * (self.button_width + self.button_spacing)  # Adjust x for each button
            y = self.start_y + row * (self.button_height + self.row_spacing)
            self.enemy_buttons.append(Button(x, y, self.button_width, self.button_height, self.enemy_type[i], self.enemy_text[i]))

        #mode buttons
        self.game_mode = ("Survival", "TimeLimit")
        self.game_mode_text = ("Survival", "Time Limit")
        self.available_width = pyxel.width - (len(self.enemy_type) - 1) * self.button_spacing
        self.button_width = self.available_width // len(self.enemy_type)
        self.start_y = int(pyxel.height * 0.6)
        
        self.game_mode_buttons = []
        for i in range(len(self.game_mode)):
            row = i // len(self.game_mode)
            x = (pyxel.width - (len(self.game_mode) * self.button_width + (len(self.game_mode) - 1) * self.button_spacing)) // 2
            x += i * (self.button_width + self.button_spacing)  # Adjust x for each button
            y = self.start_y + row * (self.button_height + self.row_spacing)
            self.game_mode_buttons.append(Button(x, y, self.button_width, self.button_height, self.game_mode[i], self.game_mode_text[i]))

        # Update button colors dynamically
        for button in self.enemy_buttons:
            button.color = ORANGE if button.id == self.app.mode[0] else GREEN

        for button in self.game_mode_buttons:
            button.color = ORANGE if button.id == self.app.mode[1] else GREEN
            self.back_button = Button(0,0, 30, 15, "MainMenuScreen", "Back")
        pyxel.mouse(True)
    
    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.back_button.is_clicked(pyxel.mouse_x, pyxel.mouse_y):
                self.app.change_screen(self.back_button.get_id())
            for button in self.enemy_buttons:
                if button.is_clicked(pyxel.mouse_x, pyxel.mouse_y):
                    self.app.mode[0] = button.id
                    print(self.app.mode[0])
            for button in self.game_mode_buttons:
                if button.is_clicked(pyxel.mouse_x, pyxel.mouse_y):
                    self.app.mode[1] = button.id
                    print(self.app.mode[1])
        
        # Update button colors dynamically
        for button in self.enemy_buttons:
            button.color = ORANGE if button.id == self.app.mode[0] else GREEN

        for button in self.game_mode_buttons:
            button.color = ORANGE if button.id == self.app.mode[1] else GREEN

    def draw(self):
        pyxel.cls(0)
        center_text(f"Your current enemy: {self.app.mode[0]}", int(pyxel.height * 0.2))
        center_text("Enemy Type Buttons",int(pyxel.height * 0.25))
        for button in self.enemy_buttons:
            button.draw()
        
        center_text(f"Your current mode: {self.app.mode[1]}",int(pyxel.height * 0.5))
        center_text("Game Mode Buttons",int(pyxel.height * 0.55))
        for button in self.game_mode_buttons:
            button.draw()
            
        self.back_button.draw()


