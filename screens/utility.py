import pyxel
from models.skill import Skills
from models.world import TILE_SIZE
from config import FPS
import models.world as world
import pygame

#just a file to store some functions to reuse in many files
def center_text(text, y, color = 7):
    x = (pyxel.width - len(text) * 4) // 2
    pyxel.text(x, y, text, color)
    
def draw_player_health_bar(max_hp, hp, y):
    total = pyxel.width / 4
    x = total/max_hp
    pyxel.rect(0, 290 - y, hp*x, 10, 9)
    
def draw_skill_image(skills : Skills, y):
    x = pyxel.width / 4 + 10
    for skill in skills.skills.values():
        if skill.current_cooldown <= 0:
            img_x, img_y = skill.image  # Unpack tuple
            pyxel.blt(x, 290 - TILE_SIZE - y, 0, img_x * TILE_SIZE, img_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Draw 8x8 sprite
             # Ensure text is visible
        text_x = x  
        text_y = 290 - TILE_SIZE - y
        if skill.current_active_time > 0:  # Avoid negative values
            pyxel.text(text_x,text_y - 6, "Active:", 7)
            pyxel.text(text_x, text_y, str(int(skill.current_active_time/FPS)), 7)
        if skill.current_cooldown > 0 and skill.current_active_time <= 0: 
            pyxel.text(text_x,text_y - 6, "Cooldown:", 8)
            pyxel.text(text_x, text_y, str(int(skill.current_cooldown/FPS)), 8)
        x+= TILE_SIZE * 4
        
def draw_pause_screen():
    for y in range(0, pyxel.height, 5):
        for x in range(0, pyxel.width, 5):
            pyxel.pset(x, y, 5) #draw 
    center_text("Pause", pyxel.height/2 - 4 * 5, 9)
    center_text(f"MAP PLAYING: {int(world.TILE_MAP / 8)} and {world.TILE_MAP % 8}", pyxel.height/2 - 4 * 3, 9)
    
def render_score(score):
    
    font = pygame.font.Font(None, 14)  # Default font
    #Score text with pygame
    display_score = score
    score_text = font.render(f"Score: {display_score}", False, (255, 255, 255))  # White text
        
    text_surface = pygame.Surface(score_text.get_size(), pygame.SRCALPHA)
    text_surface.blit(score_text, (0, 0))
    img_width, img_height = text_surface.get_size()
    
    padding = 2  # Padding from screen edges

    # Calculate bottom-right position
    x_pos = pyxel.width - img_width - padding  # Right aligned
    y_pos = pyxel.height - img_height  # Bottom aligned

    # Draw text pixel-by-pixel
    for y in range(img_height):
        for x in range(img_width):
            r, g, b, a = text_surface.get_at((x, y))  # Get RGBA values
            if a > 0:  # Only draw non-transparent pixels
                pyxel.pset(x_pos + x, y_pos + y, 7)  # 7 = White