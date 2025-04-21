# Pyxel Dodge Ball Game

## Description
This project is a dodgeball-style game developed using the Pyxel library. It was created as a learning exercise while exploring game development with Pyxel and Pygame. Players must dodge incoming balls and utilize skills to survive as long as possible.

## Game Modes
- **Single Player:** Control one character and dodge balls to stay alive.
- **Multiplayer:** Two players can play on the same computer using separate controls.
- **Bot Mode:** A human player competes alongside or against a bot.
- **Challenge Mode:** A harder version of the game with random maps, more enemies, and reduced skill cooldown.

## Controls & Features
-**Single player**:
- **Arrow Keys:** Move your character.
- **Skills:**
  - `A`: Accelerate
  - `S`: Invincibility
  - `D`: Regeneration

-**Multiplayer**:
- **Arrow Keys:** Move your character (Player 1).
- **Skills (Player 1):**
  - `Keypad 7`: Accelerate
  - `Keypad 8`: Invincibility
  - `Keypad 9`: Regeneration
- **WASD:** Player 2 movement.
- **Skills (Player 2):**
  - `C`: Accelerate
  - `V`: Invincibility
  - `B`: Regeneration

-**Pause:** `P`

-**Return to map select:** `TAB`

-**Exit the game:** Press `ESC` or use the Quit button in the Main Menu

## Technologies Used
- **Python Version:** 3.12.6
- **Libraries:**
  - `pyxel`: Retro game engine
  - `pygame`: For certain interface interactions and utility handling

## Installation

1. **Clone the Repository**
   ```bash
   git clone <your-repo-link>
   cd <your-repo-name>
   ```

2. **Install Python**
   - Download and install Python from [python.org](https://www.python.org/downloads/).

3. **Install Dependencies**
   ```bash
   pip install pyxel pygame
   ```

## Running the Game
Run the game using the following command:
```bash
python main.py
```

## Screens and Guides
The game includes an in-game guide screen explaining:
- Movement controls and skill buttons
- Multiplayer key mapping
- Challenge mode mechanics
- Visual indicators (arrows, skill icons, etc...) for learning gameplay basics

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
