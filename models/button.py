import pyxel
GREEN = 11
BLACK = 0

class Button:
    def __init__(self, x, y, width, height, id, text = None, color = GREEN, text_color = BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = id
        self.clicked = False
        self.text = text if text is not None else self.id
        self.color = color
        self.text_color = text_color

    def is_clicked(self, mouse_x, mouse_y):
        return (
            self.x < mouse_x < self.x + self.width
            and self.y < mouse_y < self.y + self.height
        )

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)
        
        # Calculate text width (each character is 4 pixels wide in Pyxel)
        text_width = len(str(self.text)) * 4  
        text_height = 6  # Default Pyxel text height
        
        # Center the text within the button
        text_x = self.x + (self.width - text_width) // 2
        text_y = self.y + (self.height - text_height) // 2
        
        pyxel.text(text_x, text_y, str(self.text), self.text_color)

    def get_id(self):
        print("Button clicked: " + f"{self.id}")
        return self.id
            
            
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