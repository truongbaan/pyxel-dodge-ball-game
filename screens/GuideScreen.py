import pyxel
from models.button import Button
from models.skill import SkillItem
from models.world import TILE_SIZE
from screens.utility import center_text

TRI_SIZE = 5
LINE_SIZE = 15
SQUARE_SIZE = int((LINE_SIZE + TRI_SIZE) * 1.2)
BLACK = 0
WHITE = 7
COLOR = WHITE
class GuideScreen:
    def __init__(self, app):
        self.app = app
        self.back_button = Button(0,0, 60, 20, "MainMenuScreen")
        pyxel.load("map/0.pyxres")
        self.buttons = [
            Button(0, int(pyxel.height/2), 40, 20, -1, "Prev Page"),
            Button(pyxel.width - 40, int(pyxel.height/2), 40, 20, 1, "Next Page")
        ]
        self.page = 0
    
    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.back_button.is_clicked(pyxel.mouse_x, pyxel.mouse_y):
                   self.app.change_screen(self.back_button.get_id())
                for button in self.buttons:
                    if button.is_clicked(pyxel.mouse_x, pyxel.mouse_y):
                        if 0 <= self.page <= 3:
                            self.page += button.get_id()
                        if self.page < 0: self.page = 0
                        if self.page > 3: self.page = 3
    
    def draw(self):
        #for image
        skills = {
            "Accelerate": SkillItem.ACCELERATE,
            "Invincible": SkillItem.INVINCIBLE,
            "Healing": SkillItem.HEALING
        }
            
        if self.page == 0:
            SCALE_ON_HEIGHT = int(pyxel.height / 7)
        
            pyxel.cls(BLACK)
            center_text("Guide", int(pyxel.height / 10))
            
            # Up-pointing arrow
            pyxel.line(int(pyxel.width/3), SCALE_ON_HEIGHT, int(pyxel.width/3), SCALE_ON_HEIGHT + LINE_SIZE, COLOR)
            pyxel.tri(int(pyxel.width/3) - TRI_SIZE, SCALE_ON_HEIGHT, int(pyxel.width/3) + TRI_SIZE, SCALE_ON_HEIGHT, int(pyxel.width/3), SCALE_ON_HEIGHT - TRI_SIZE, COLOR)
            pyxel.rectb(int(pyxel.width/3) - TRI_SIZE - int(SQUARE_SIZE/4), SCALE_ON_HEIGHT - TRI_SIZE - 1, SQUARE_SIZE, SQUARE_SIZE, COLOR)
            
            # Down-pointing arrow
            pyxel.line(int(pyxel.width/3), SCALE_ON_HEIGHT + int(LINE_SIZE * 1.4), int(pyxel.width/3), SCALE_ON_HEIGHT + int(LINE_SIZE * 2.4), COLOR)
            pyxel.tri(int(pyxel.width/3) - TRI_SIZE, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.4), int(pyxel.width/3) + TRI_SIZE, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.4), int(pyxel.width/3), SCALE_ON_HEIGHT + int(LINE_SIZE * 2.4) + TRI_SIZE, COLOR)
            pyxel.rectb(int(pyxel.width/3) - TRI_SIZE - int(SQUARE_SIZE/4), SCALE_ON_HEIGHT + int(LINE_SIZE * 1.4) - 1, SQUARE_SIZE, SQUARE_SIZE, COLOR)
            
            # Left-pointing arrow
            pyxel.line(int(pyxel.width/3) - LINE_SIZE, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1), int(pyxel.width/3) - LINE_SIZE * 2, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1), COLOR)  # Horizontal line
            pyxel.tri(int(pyxel.width/3) - LINE_SIZE * 2 - TRI_SIZE, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1), int(pyxel.width/3) - int(LINE_SIZE * 2), SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1) + TRI_SIZE, int(pyxel.width/3) - int(LINE_SIZE * 2), SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1) - TRI_SIZE, COLOR) # Triangle tip
            pyxel.rectb(int(pyxel.width/3) - LINE_SIZE * 2 - TRI_SIZE - 1, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1) - TRI_SIZE - int(SQUARE_SIZE/4), SQUARE_SIZE, SQUARE_SIZE, COLOR)

            # Right-pointing arrow
            pyxel.line(int(pyxel.width/3) + LINE_SIZE, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1), int(pyxel.width/3) + LINE_SIZE * 2, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1), COLOR)  # Horizontal line
            pyxel.tri(int(pyxel.width/3) + LINE_SIZE * 2 + TRI_SIZE, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1), int(pyxel.width/3) + int(LINE_SIZE * 2), SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1) + TRI_SIZE, int(pyxel.width/3) + int(LINE_SIZE * 2), SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1) - TRI_SIZE, COLOR) # Triangle tip
            pyxel.rectb(int(pyxel.width/3) + LINE_SIZE - 1, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1) - TRI_SIZE - int(SQUARE_SIZE/4), SQUARE_SIZE, SQUARE_SIZE, COLOR)
            
            text_spacing = 20
            pyxel.text(int(pyxel.width/3) + LINE_SIZE * 2 + TRI_SIZE + text_spacing, SCALE_ON_HEIGHT + int(LINE_SIZE * 2.1), "Use arrow key to move", COLOR)
            
            #skill guide
            center_text("Skills", int(pyxel.height / 10) + int(LINE_SIZE * 5))

            x = pyxel.width / 4 + 10
            y = SCALE_ON_HEIGHT + int(LINE_SIZE * 5)

            usage = [
                "Press A to X2 Speed",
                "Press S to become Invincible",
                "Press D to Regenerate"
            ]
            for i,(img_x, img_y) in enumerate(skills.values()):
                pyxel.blt(x, y, 0, img_x * TILE_SIZE, img_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Draw skill sprite
                pyxel.text(x + 20, y, usage[i], COLOR)
                y += LINE_SIZE  # Move down for the next skill
            
            y += 2 * LINE_SIZE # make some space
            #pause and tab guide
            line = (
                "Pause Game",
                "Press P to pause the game (only works for normal play)",
                "Tab usage",
                "Press TAB when you're in the game",
                "to return to the map choosing screen",
                "(only works for normal play)"
            )    
            for line in line:
                center_text(line, y)
                y += LINE_SIZE
        
        if self.page == 1:
            center_text("How to play", int(pyxel.height / 10))
            pyxel.text(50, int(pyxel.height / 10) + LINE_SIZE * 2, "This is you     ->   ", 7)
            pyxel.blt(150, int(pyxel.height / 10) + LINE_SIZE * 2, 0, 2 * TILE_SIZE, 0 * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Draw skill sprite
            pyxel.text(50, int(pyxel.height / 10) + LINE_SIZE * 4, "This is the ball     ->   ", 7)
            pyxel.circ(150, int(pyxel.height / 10) + LINE_SIZE * 4, 3, 8)
            center_text("You will need to dodge the ball",int(pyxel.height / 10) + LINE_SIZE * 6)
            center_text("If you dont dodge it, you will lose health",int(pyxel.height / 10) + LINE_SIZE * 8)
            center_text("You will lose after a certain hit",int(pyxel.height / 10) + LINE_SIZE * 10)
            center_text("Try to survive as long as possible, have fun!",int(pyxel.height / 10) + LINE_SIZE * 12)
            
        if self.page == 2:
            #multiplayer guide
            center_text("Multiplayer Guide", int(pyxel.height / 10))
            usage = [
                "Press C to X2 Speed",
                "Press V to become Invincible",
                "Press B to Regenerate",
                "Press keypad[7] to X2 Speed",
                "Press keypad[8] to become Invincible",
                "Press keypad[9] to Regenerate"
            ]
            
            x = pyxel.width / 4 + 10
            y = 60
            for i,(img_x, img_y) in enumerate(skills.values()):
                pyxel.blt(x, y, 0, img_x * TILE_SIZE, img_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Draw skill sprite
                pyxel.text(x + 20, y, usage[i], COLOR)
                pyxel.blt(x, y + int(pyxel.height / 2), 0, img_x * TILE_SIZE, img_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Draw skill sprite
                pyxel.text(x + 20, y + int(pyxel.height / 2), usage[i + int(len(usage)/2)], COLOR)
                y += LINE_SIZE  # Move down for the next skill
            pyxel.text(10, int(pyxel.height / 10) + 10, "Key for P1: WASD for movement", COLOR)
            pyxel.text(10, int(pyxel.height / 2) + 40, "Key for P2: Arrows Key for movement", COLOR)
            center_text("Note", y + int(pyxel.height / 2))
            center_text("If one player dies, you can still revive with regeneration", y + int(pyxel.height / 2) + LINE_SIZE )
            center_text("The game only ends when both players dies", y + int(pyxel.height / 2) + LINE_SIZE *2)
        
        
        if self.page == 3:
            #challenge guide
            center_text("Challenge Guide", int(pyxel.height / 10))
            
            guideline = (
                "Your map will be random",
                "Can not choose enemy and mode type",
                "More enemies will appear",
                "Skill cooldown is reduced by half"
            )
            
            y = int(pyxel.height / 10) + 10
            
            for line in guideline:
                center_text(line, y)
                y += LINE_SIZE
    
            
        #draw button for all screen
        for button in self.buttons:
            button.draw()
        self.back_button.draw()
        
#Color list:
# 0: Black
# 1: Dark Blue
# 2: Dark Purple
# 3: Dark Green
# 4: Brown
# 5: Dark Gray
# 6: Light Gray
# 7: White
# 8: Red
# 9: Orange
# 10: Yellow
# 11: Green
# 12: Blue1   
# 13: Lavender
# 14: Pink
# 15: Light Yellow

#page 0: for single play guide
#page 1: explain how to unlock maps
#page 2: guide key bind for multiple player
#page 3: explain about challenge (map will be random, could save score)