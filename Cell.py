import pygame
import random
from config import *


class Cell:
    """
    A Cell class. A cell is a single square on the board.

    Important attributes:
    --------------------

    self.surface:
        The pygame.Surface the cell is attached to.

    self.alive_next_round:
        Every round effects the liveliness of every cell, this is
        a boolean value of that liveliness (dead/alive).

    """
    def __init__(self, surface, init_live_color=WHITE, init_dead_color=PINK):
        """ Initialize the Cell object """
        self.alive = False
        self.alive_color = init_live_color
        self.dead_color = init_dead_color
        self.color = self.dead_color
        self.surface = surface
        self.alive_next_round = False

    def live(self):
        self.alive = True
        self.color = self.alive_color

    def die(self):
        self.alive = False
        self.color = self.dead_color


class CellGrid:
    """
    A Cell Grid class. This is the actual board of the game.

    Important attributes:
    --------------------

    self.game:
        The game the cell grid is attached to.


    Important methods:
    --------------------

    new_grid(self, ...):
        After the cell size is changed (via Setup menu), a new grid
        needs to be built.

    draw_grid(self, ...):
        Draw cells according to their next round liveliness.

    update_grid(self):
        Apply the rules of Conway's game of life to the grid.

    """
    def __init__(self, game):
        self.game = game
        # create a matrix of new Cell objects
        self.grid = [[Cell(self.game.screen, game.alive_cell_color, game.dead_cell_color)
                      for _ in range(game.num_of_cols + 2)]
                     for __ in range(game.num_of_rows + 2)]

    def new_grid(self, new_cell_size):
        """ Build a new cell grid """
        self.game.cell_size = new_cell_size
        self.game.num_of_cols = self.game.screen_w // self.game.cell_size
        self.game.num_of_rows = self.game.screen_h // self.game.cell_size
        new_grid = [[Cell(self.game.screen, self.game.alive_cell_color, self.game.dead_cell_color)
                     for _ in range(self.game.num_of_cols + 2)]
                    for __ in range(self.game.num_of_rows + 2)]
        self.grid = new_grid

    def draw_grid(self, cell_edge_size):
        """
        Draw the cells of the grid to their surface (the screen).
        The cell is drawn according to it's next round liveliness.
        """
        left = 0
        top = 0
        for row in range(1, self.game.num_of_rows + 1):
            for col in range(1, self.game.num_of_cols + 1):
                cell = self.grid[row][col]
                if cell.alive_next_round:
                    cell.color = cell.alive_color
                    cell.alive = True
                    cell.alive_next_round = False
                else:
                    cell.color = cell.dead_color
                    cell.alive = False

                square = pygame.Rect(left, top, cell_edge_size, cell_edge_size)
                pygame.draw.rect(cell.surface, cell.color, square)
                left += cell_edge_size

            left = 0
            top += cell_edge_size

    def update_grid(self):
        """
        Apply the rules of Conway's game of life to the grid.
        This updates the alive_next_round attribute of the cells.

        important variables:
        - over_population_limit: on/off bacteria mode.
        - adj_list: for the current cell, a list of it's adjacent cells.

        """
        if self.game.bacteria_mode:
            over_population_limit = 4
        else:
            over_population_limit = 3
        for row in range(1, self.game.num_of_rows + 1):
            for col in range(1, self.game.num_of_cols + 1):
                curr_cell = self.grid[row][col]
                adj_list = [self.grid[row-1][col-1], self.grid[row-1][col], self.grid[row-1][col+1],
                            self.grid[row][col-1], self.grid[row][col+1], self.grid[row+1][col-1],
                            self.grid[row+1][col], self.grid[row+1][col+1]]

                # act upon adj_list
                adj_live_count = 0
                for cell in adj_list:
                    if cell.alive:
                        adj_live_count += 1

                if curr_cell.alive:
                    if adj_live_count < 2:
                        curr_cell.alive_next_round = False  # loneliness
                    elif adj_live_count > over_population_limit:
                        curr_cell.alive_next_round = False  # overpopulation
                    else:
                        curr_cell.alive_next_round = True  # same same
                else:
                    if adj_live_count == 3:
                        curr_cell.alive_next_round = True  # A cell is born
                    else:
                        curr_cell.alive_next_round = False  # same same

    def random_middle_start(self):
        """ Choose cells randomly inside a square in the middle of the board.
            Resurrect them.
        """
        start_area_left = (self.game.num_of_cols // 2) - (self.game.start_area_edge // 2)
        start_area_top = (self.game.num_of_rows // 2) - (self.game.start_area_edge // 2)
        curr_run = []
        right_bound = start_area_left + self.game.start_area_edge
        down_bound = start_area_top + self.game.start_area_edge
        for col in range(start_area_left, right_bound):
            for row in range(start_area_top, down_bound):
                if random.random() < self.game.life_chance_for_random_start:
                    curr_run.append((row, col))
        self.set_start_cells(curr_run)
        return curr_run

    def set_start_cells(self, coordinate_arr):
        """Resurrect cells in given coordinates """
        for coordinate in coordinate_arr:
            self.grid[coordinate[0]][coordinate[1]].live()



