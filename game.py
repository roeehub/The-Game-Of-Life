import pygame
import time
from threading import Timer
from config import *
import menus
import Cell
import log_cool_runs as lcr


class Game:
    """
    A class for a game object, contains all the parameters
    relevant to the game.

    Important attributes:
    --------------------
    self.top_view:
        The pygame.Surface object that is seen by the player.

    self.num_of_cols/rows:
        Number of columns/rows of the game board grid.

    self.start_area_edge:
        When playing a random run, the edge size of the square in the middle
        of the board in which the cells spawn randomly according to
        self.life_chance_for_random_start.

    self.*_KEY:
        A recording of a key press.

    self.*_menu
        A *Menu object.

    self.curr_run:
        A record of the starting coordinates of the current run.


    Important methods:
    ------------------
    check_events(self):
        Record key presses and return mouse position if clicked.

    draw_text(self, ...):
        Draw text on the given surface.

    input_box(self, ...):
        Creates a box for text input.

    game_loop(self):
        Runs the the game of life.

    reset_grid(self):
        Resets all cells to their dead state.

    """
    def __init__(self):
        """ Initialize the game object"""
        pygame.init()
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.SCALED, size=(1920, 1080))
        self.top_view = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.SCALED, size=(1920, 1080))
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()
        self.num_of_cols = self.screen_w // CELL_EDGE_SIZE
        self.num_of_rows = self.screen_h // CELL_EDGE_SIZE
        self.default_font = DEFAULT_FONT
        # setup params
        self.text_color = WHITE
        self.selected_text_color = BLUE
        self.round_time = ROUND_TIME
        self.start_area_edge = START_AREA_EDGE
        self.life_chance_for_random_start = CHANCE
        self.cell_size = CELL_EDGE_SIZE
        self.run_mode = 'Select'
        self.bacteria_mode = False
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESCAPE_KEY, self.LEFT_KEY, self.RIGHT_KEY = \
            False, False, False, False, False, False
        self.running, self.playing = False, False
        pygame.display.set_caption("The Game Of Life")
        icon = pygame.image.load('assets/virus_red.png')
        pygame.display.set_icon(icon)
        self.loop = LOOP
        self.screen.fill((44, 200, 88))  # ---- should never be seen ----
        self.alive_cell_color = YELLOW
        self.dead_cell_color = DARKER_PURPLE
        self.main_menu = menus.MainMenu(self)
        self.load_menu = menus.LoadMenu(self)
        self.setup_menu = menus.SetupMenu(self)
        self.info_menu = menus.InfoMenu(self)
        self.quit_menu = menus.QuitMenu(self)
        self.curr_menu = self.main_menu
        self.curr_run = []
        self.cell_grid = Cell.CellGrid(self)
        self.loaded = False

    def check_events(self):
        """ Record key presses and return mouse position if clicked """
        mouse_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESCAPE_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
        return mouse_pos

    def draw_text(self, text, size, x, y, color=WHITE, surface=None):
        """ Draw text on the given surface, Default is top_view """
        font = pygame.font.Font(self.default_font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        if surface is not None:
            surface.blit(text_surface, text_rect)
        else:
            self.top_view.blit(text_surface, text_rect)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESCAPE_KEY, self.RIGHT_KEY, self.LEFT_KEY = \
            False, False, False, False, False, False

    def input_box(self, width, height, surface, text_size=22, x_offset=100, y_offset=62, text_center_x=93, text_center_y=19):
        """ Creates a box for text input
        Features:
            - backspace to delete
            - enter to submit
            - tab to get name from cool_runs resource
            - displays in real time
        """
        text = ''
        tab_index = 2
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_BACKSPACE and len(text) > 0:
                        text = text[:-1]
                    elif event.key == pygame.K_TAB:
                        name = lcr.get_name_by_index(tab_index)
                        if name is None:
                            tab_index = 2
                            text = ''
                        else:
                            text = name
                            tab_index += 1
                    else:
                        text += event.unicode
            surface.fill(self.curr_menu.background)
            self.draw_text(text, text_size, text_center_x, text_center_y, WHITE, surface)
            self.top_view.blit(surface, ((self.screen_w - width) // 2 + x_offset, (self.screen_h - height) // 2 + y_offset))
            pygame.display.update()

    def allow_another_loop(self):
        """ Restricts time between cycles to obtain constant speed """
        self.loop = True

    def game_loop(self):
        """ Runs the the game of life
        While playing:
            - press p to pause
            - press s for popup save window
            - press escape to exit game
        """
        if not self.loaded:
            if self.run_mode == 'Select':
                self.cell_grid.draw_grid(self.cell_size)
                pygame.display.update()
                self.click_mode()
            else:
                self.curr_run = self.cell_grid.random_middle_start()

        # main loop
        running = True
        while running:
            timer = Timer(self.round_time, self.allow_another_loop)
            timer.start()
            self.cell_grid.update_grid()
            self.cell_grid.draw_grid(self.cell_size)
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_p:
                        running = self.pause()
                    elif event.key == pygame.K_s:
                        self.save_window_popup()

            # Busy-wait to account for self.round_time
            while not self.loop:
                pass
            self.loop = False
            pygame.display.update()

    def click_mode(self):
        """ The click-and-live feature, supports dragging the mouse """
        done = False
        mouse_down = False
        while not done or mouse_down:
            for event in pygame.event.get():
                if event.type in {pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP} or mouse_down:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_down = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        mouse_down = False
                    x, y = pygame.mouse.get_pos()
                    col = x // self.cell_size
                    row = y // self.cell_size
                    cell = self.cell_grid.grid[row][col]
                    cell.live()
                    self.curr_run.append((row, col))
                    left = col * self.cell_size
                    top = row * self.cell_size
                    square = pygame.Rect(left, top, self.cell_size, self.cell_size)
                    pygame.draw.rect(cell.surface, cell.color, square)
                    pygame.display.update()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        done = True

    @staticmethod
    def pause():
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_p:
                        pause = False
        return True

    def save_window_popup(self):
        """ Creates a popup save window """
        # windows setup
        (width, height) = (600, 400)
        save_window = pygame.Surface((width, height))
        save_window.fill(self.curr_menu.background)
        input_window = pygame.Surface((300, 38))
        # display
        input_window.fill(self.curr_menu.background)
        self.draw_text("Save Run?", self.main_menu.default_text_size + 10, width // 2, height // 6, WHITE, save_window)
        self.draw_text("Title:", self.main_menu.default_text_size, width // 4 - 10, height // 3 + 15, WHITE, save_window)
        self.draw_text("ENTER  TO  SAVE", self.main_menu.default_text_size + 1, width // 2, height // 2 + 25, WHITE, save_window)
        self.draw_text("ESCAPE TO CANCEL", self.main_menu.default_text_size, width // 2, 3 * height // 4 + 10, WHITE, save_window)
        self.top_view.blit(save_window, ((self.screen_w - width) // 2, (self.screen_h - height) // 2))
        self.top_view.blit(input_window, ((self.screen_w - width) // 2 + 200, (self.screen_h - height) // 2 + 124))
        pygame.display.update()
        # interactive input box
        name = self.input_box(width, height, input_window, self.main_menu.default_text_size, 200, 124, 150, 19)
        self.handle_name_input(name, save_window, width, height)

    def handle_name_input(self, name, save_window, width, height):
        """ Save the name given if it is legitimate """
        if not name or name is None:
            return
        save_window.fill(self.curr_menu.background)
        if lcr.check_name_exists(name):
            self.draw_text("Name already exists!", int(self.main_menu.default_text_size * 1.5), width // 2, height * (1 / 3), WHITE, save_window)
            self.draw_text("Not saved!", int(self.main_menu.default_text_size * 1.5), width // 2, height * (2 / 3), WHITE, save_window)
            self.top_view.blit(save_window, ((self.screen_w - width) // 2, (self.screen_h - height) // 2))
            pygame.display.update()
            time.sleep(1)
        else:
            self.draw_text("Saved!", self.main_menu.default_text_size * 2, width // 2, height // 2, WHITE, save_window)
            self.top_view.blit(save_window, ((self.screen_w - width) // 2, (self.screen_h - height) // 2))
            pygame.display.update()
            time.sleep(0.4)
            lcr.log_run(self.curr_run, name, self.cell_size)

    def update_grid_color(self):
        """ Update the color of dead and alive cells """
        for row in range(self.num_of_rows + 1):
            for col in range(self.num_of_cols + 1):
                self.cell_grid.grid[row][col].alive_color = self.alive_cell_color
                self.cell_grid.grid[row][col].dead_color = self.dead_cell_color

    def reset_grid(self):
        """ Resets all cells to their dead state """
        self.curr_run.clear()
        for row in range(self.num_of_rows):
            for col in range(self.num_of_cols):
                self.cell_grid.grid[row][col].die()

    def reset_game(self):
        self.reset_grid()
        self.loaded = False
        self.playing = False

    @staticmethod
    def quit():
        pygame.quit()
