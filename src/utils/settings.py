import pygame

# Game dimensions
GRID_SIZE = 20
CELL_SIZE = 50
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
CELL_PADDING = 4

# Game settings
FPS = 10
FOOD_SIZE_FACTOR = 0.4

# Colors
BACKGROUND = (15, 15, 15)  # Very dark grey, almost black
GRID_COLOR = (25, 25, 25)  # Slightly lighter than background for subtle grid lines
SNAKE_HEAD = (135, 206, 250)
SNAKE_BODY_BASE = (30, 144, 255)
SNAKE_OUTLINE = (10, 10, 10)  # Very dark outline, almost black but slightly lighter than background
FOOD_COLOR = (244, 67, 54)
FOOD_OUTLINE = (211, 47, 47)
PATH_COLOR = (120, 30, 140)
WHITE = (255, 255, 255)
SCORE_COLOR = (180, 124, 253)  # #B47CFD
GAME_OVER_COLOR = (224, 108, 117)
TITLE_COLOR = (152, 195, 121)
START_TEXT_COLOR = (255, 255, 255)

# Game settings
INITIAL_DIRECTION = (1, 0)
INITIAL_POSITION = (GRID_SIZE // 2, GRID_SIZE // 2)

# Snake color schemes (Pastel to Dark gradients)
SNAKE_COLOR_SCHEMES = {
    'blue': {
        'head': (173, 216, 230),  # Light pastel blue
        'body': (30, 144, 255)    # Darker blue
    },
    'purple': {
        'head': (197, 150, 221),  # Pastel version of SCORE_COLOR
        'body': (128, 0, 128)     # Dark purple
    },
    'green': {
        'head': (176, 224, 176),  # Pastel green
        'body': (34, 139, 34)     # Forest green
    },
    'pink': {
        'head': (255, 182, 193),  # Light pink
        'body': (219, 112, 147)   # Pale violet red
    },
    'orange': {
        'head': (255, 218, 185),  # Peach
        'body': (255, 140, 0)     # Dark orange
    },
    'cyan': {
        'head': (176, 224, 230),  # Powder blue
        'body': (0, 139, 139)     # Dark cyan
    }
}