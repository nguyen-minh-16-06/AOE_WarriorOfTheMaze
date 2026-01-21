import numpy as np

# ===== SCREEN SETTINGS =====
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
TILE_WIDTH = 64
TILE_HEIGHT = 32

# ===== SPEED SETTINGS =====
MOVE_SPEED = 2
ANIMATION_SPEED = 0.0

# ===== MAZE LAYOUT =====
MAZE_LAYOUT = np.array([
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 0]
])

# ===== ASSET PATHS =====
ASSET_CONFIG = {
    'floor': 'assets/resources/grass',
    'wall': 'assets/resources/natures',
    'goal': 'assets/units/knight/blue',
    'start': 'assets/resources/buildings',
    'agent': 'assets/units/knight/red'
}