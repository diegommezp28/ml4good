# Snake Game

A classic Snake game implementation using Python and Pygame.

## Requirements

- Python 3.8 or higher
- uv (Python package manager)

## Installation

1. Make sure you have Python 3.8 or higher installed
2. Install uv if you haven't already:
   ```bash
   pip install uv
   ```
3. Install the game dependencies:
   ```bash
   uv pip install -e .
   ```

## How to Play

Run the game:
```bash
python snake_game.py
```

### Controls
- Use the arrow keys to control the snake's direction
- Eat the red food to grow longer and increase your score
- Avoid hitting yourself
- The snake can pass through walls and appear on the opposite side

### Game Features
- Score tracking
- Smooth controls
- Wrapping around screen edges
- Game over screen 