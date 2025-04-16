import pyxel
from config import FPS
from models.player import Player
class SkillItem:
    """Stores image coordinates for skill icons in the sprite sheet."""
    INVINCIBLE = (6, 0)
    ACCELERATE = (8, 0)
    HEALING = (0,2)

class Skill:
    def __init__(self, name, key, image, cooldown, duration, effect, reverse_effect = None, tick_interval = None):
        self.name = name
        self.key = key
        self.image = image  # (x, y) position in spritesheet
        self.cooldown = cooldown * FPS
        self.duration = duration * FPS
        self.effect = effect
        self.reverse_effect = reverse_effect

        self.current_cooldown = 0
        self.current_active_time = 0
        self.tick_interval = tick_interval * FPS if tick_interval is not None else None

    def activate(self, player):
        #activate if allowed
        if self.current_cooldown <= 0:
            print(f"{self.name} activated!")
            
            self.current_cooldown = self.cooldown
            self.current_active_time = self.duration
        else:
            print(f"{self.name} is on cooldown.")

    def update(self, player):
        #handle logic
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
        if self.current_active_time > 0:
            if self.current_active_time == self.duration:
                self.effect(player)
            if self.tick_interval is not None:
                if self.current_active_time % self.tick_interval == 0:
                    self.effect(player)
            if self.current_active_time == 1:
                if self.reverse_effect != None:
                    self.reverse_effect(player)
            self.current_active_time -= 1

class Skills:
    def __init__(self, player : Player):
        self.player = player
        self.skills = {
            "accelerate": Skill("Accelerate", self.player.key_list[4], SkillItem.ACCELERATE, 10, 5, self.accelerate_effect, self.revert_accelerate),
            "invincible": Skill("Invincible", self.player.key_list[5], SkillItem.INVINCIBLE, 14, 3, self.invincible_effect, self.revert_invincible),
            "healing" : Skill ("Healing", self.player.key_list[6], SkillItem.HEALING, 20, 10, self.healing_effect, None, 2)
        }

    def activate_skill(self, key):
        #check keys and activate
        for skill in self.skills.values():
            if skill.key == key:
                skill.activate(self.player)

    def update(self):
        for skill in self.skills.values():
            skill.update(self.player)

    # Skill Effects
    def accelerate_effect(self, player):
        #speed change
        print("Speed X 2")
        self.player.DX *= 2
        
    def revert_accelerate(self, player):
        #reset speed when end duration
        self.player.DX /= 2
        print("Speed returned to normal.")
        
    def invincible_effect(self, player):
        self.player.invincible = True
        print("Invincibility effect applied!") 
        
    def revert_invincible(self, player):
        self.player.invincible = False
        print("End of invincibility")
        pass
    
    def healing_effect(self, player):   
        if self.player.health_bar < self.player.max_health:
            self.player.health_bar += 1
