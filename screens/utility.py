import pyxel

def center_text(text, y, color = 7):
    x = (pyxel.width - len(text) * 4) // 2
    pyxel.text(x, y, text, color)