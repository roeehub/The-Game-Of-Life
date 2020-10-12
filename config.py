
""" Configuration file for constants and start conditions"""

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (220, 15, 243)
PURPLE = (190, 0, 190)
DARK_PURPLE = (65, 0, 65)
DARKER_PURPLE = (45, 0, 45)
BROWN = (138, 126, 46)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 102)
RED = (255, 0, 0)
YELLOW = (222, 225, 0)
GRAY = (66, 66, 66)
GREEN = (0, 255, 0)
LEAF_GREEN = (0, 160, 0)
TREE_TOP_GREEN = (0, 100, 0)
ORANGE = (255, 128, 0)
MUSTARD = (204, 204, 0)
TEXTCOLOR = (255, 255, 255)

# display
DEFAULT_FONT = 'assets/Classic Robot Bold.otf'

# game
CELL_EDGE_SIZE = 10
START_AREA_EDGE = 35
DEFAULT_CURSOR_X_OFFSET = -80
SPEED_INDEX = 3
CHANCE = 0.9
ROUND_TIME = 0.05
LOOP = False
DEBUG = False


def log(s):
    """ Basic logging function to console for debugging """
    if DEBUG:
        print(s)




