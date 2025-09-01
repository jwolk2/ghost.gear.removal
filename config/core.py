# Base screen + timing
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
FPS = 60
INACTIVITY_TIMEOUT = 180  # seconds

# Reference resolution for scaling
REF_WIDTH = 1920
REF_HEIGHT = 1200

# Helper for tiny clamping on small screens (optional)
def _at_least(x, min_val=1):
    return max(int(x), min_val)

# Global colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (196, 255, 77)
LIGHT_BLUE = (195, 216, 241)
DARK_BLUE = (50, 50, 200)
DARK_BLUE_HOVER = (70, 70, 240)
TRANSPARENT = (0, 0, 0, 0)

# Default fonts
DEFAULT_FONT = "assets/fonts/Menlo.ttc"
TITLE_FONT = "assets/fonts/Bungee-Regular.ttf"
HEADING_FONT = "assets/fonts/norwester.otf"

# Button sprites
RED_BUTTON = "assets/sprites/red_button.svg"
RED_BUTTON_HOVER = "assets/sprites/red_button_hover.svg"
GREEN_BUTTON = "assets/sprites/green_button.svg"
GREEN_BUTTON_HOVER = "assets/sprites/green_button_hover.svg"
BLUE_BUTTON = "assets/sprites/blue_button.svg"
BLUE_BUTTON_HOVER = "assets/sprites/blue_button_hover.svg"

# --- Default button properties (scaled) ---
# Original: 200x60, font 32, radius 8
DEFAULT_BUTTON_WIDTH = _at_least(SCREEN_WIDTH  * (200 / REF_WIDTH))
DEFAULT_BUTTON_HEIGHT = _at_least(SCREEN_HEIGHT * (60  / REF_HEIGHT))
DEFAULT_BUTTON_TEXT = "Button"
DEFAULT_BUTTON_FONT_SIZE = _at_least(SCREEN_HEIGHT * (32  / REF_HEIGHT))
DEFAULT_BUTTON_BG_COLOR = DARK_BLUE
DEFAULT_BUTTON_TEXT_COLOR = WHITE
DEFAULT_BUTTON_HOVER_COLOR = DARK_BLUE_HOVER
DEFAULT_BUTTON_BORDER_RADIUS = _at_least(SCREEN_WIDTH * (8 / REF_WIDTH))

# --- Default text properties (scaled) ---
# Original: 400x50, font 24
DEFAULT_TEXT_WIDTH = _at_least(SCREEN_WIDTH  * (400 / REF_WIDTH))
DEFAULT_TEXT_HEIGHT = _at_least(SCREEN_HEIGHT * (50  / REF_HEIGHT))
DEFAULT_TEXT = "Text"
DEFAULT_TEXT_FONT_SIZE = _at_least(SCREEN_HEIGHT * (24  / REF_HEIGHT))
DEFAULT_TEXT_COLOR = WHITE
DEFAULT_TEXT_BG_COLOR = TRANSPARENT

# --- Sound configuration
START_SCREEN_NARRATION = "assets/sounds/Screen One Audio Description.wav"
GAME_SCREEN_1_NARRATION = "assets/sounds/Screen 2 Audio Descriptions.wav"
GAME_SCREEN_2_NARRATION = "assets/sounds/Screen 3 Audio Descriptions.wav"
REPEAT_NARRATION = True
REPEAT_NARRATION_DELAY = 20  # seconds

# Mixer / playback
SOUND_PLAYER_VOLUME = 0.25
