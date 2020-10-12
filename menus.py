import pygame
import config as conf
import log_cool_runs as lcr


class Menu:
    """ A super class for Menus

    Important attributes:
    --------------------

    self.game:
        The game the menu is attached to.

    self.run_display:
        Boolean value for displaying the menu.

    self.cursor_offset_*:
        The offset for positioning the cursor properly.

    """
    def __init__(self, game):
        """ Initialize the Menu object """
        self.game = game
        self.mid_w, self.mid_h = self.game.screen_w / 2, self.game.screen_h / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.cursor_offset_x = conf.DEFAULT_CURSOR_X_OFFSET
        self.cursor_offset_y = 2
        self.background = conf.LEAF_GREEN
        self.default_text_size = 35
        self.default_text_gap = 40
        self.default_cursor_size = 25
        self.colors = [conf.WHITE, conf.BLACK, conf.PINK, conf.PURPLE, conf.DARK_PURPLE,
                       conf.DARKER_PURPLE, conf.BROWN, conf.BLUE, conf.DARK_BLUE, conf.RED, conf.YELLOW,
                       conf.GRAY, conf.GREEN, conf.LEAF_GREEN, conf.TREE_TOP_GREEN, conf.ORANGE, conf.MUSTARD]
        self.color_names = ["WHITE", "BLACK", "PINK", "PURPLE", "DARK_PURPLE", "DARKER_PURPLE", "BROWN", "BLUE",
                            "DARK_BLUE", "RED", "YELLOW", "GRAY", "GREEN", "LEAF_GREEN", "TREE_TOP_GREEN", "ORANGE",
                            "MUSTARD"]

    def draw_cursor(self):
        self.game.draw_text('*', self.default_cursor_size, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        """ Attache the menu on top of the game screen and reset inputs """
        self.game.screen.blit(self.game.top_view, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    """
    A Main Menu class, works like a state machine

    Important additional attributes:
    -------------------------------

    self.state:
        The current state the menu is in.

    self.*_x or self.*_Y:
        The x or y position for the * label.

    """
    def __init__(self, game):
        """ Initialize the MainMenu object """
        Menu.__init__(self, game)
        self.run_cursor_offset = -130
        self.cursor_offset_x = self.run_cursor_offset
        self.state = "Run Random"
        self.bacteria_size = 50
        self.bacteria_image = pygame.image.load('assets/virus_red.png')
        self.bacteria_image = pygame.transform.scale(self.bacteria_image, (self.bacteria_size, self.bacteria_size))
        self.reverse_image = pygame.image.load('assets/reverse.png')
        self.reverse_image = pygame.transform.scale(self.reverse_image, (self.bacteria_size, self.bacteria_size))
        self.curr_image = self.bacteria_image
        self. bacteria_x, self.bacteria_y = round(self.mid_w * 1.8), 100
        self.run_random_x, self.run_random_y = self.mid_w - 150, self.mid_h + self.default_text_gap
        self.run_select_x, self.run_select_y = self.mid_w + 150, self.mid_h + self.default_text_gap
        self.load_x, self.load_y = self.mid_w, self.mid_h + self.default_text_gap * 2
        self.setup_x, self.setup_y = self.mid_w, self.mid_h + self.default_text_gap * 3
        self.info_x, self.info_y = self.mid_w, self.mid_h + self.default_text_gap * 4
        self.quit_x, self.quit_y = self.mid_w, self.mid_h + self.default_text_gap * 5
        self.cursor_rect.midtop = (self.run_random_x + self.cursor_offset_x, self.run_random_y + self.cursor_offset_y)

    def display_menu(self):
        """ Display the menu on the game screen"""
        self.run_display = True
        while self.run_display:
            # collect input
            mouse_pos = self.game.check_events()
            self.move_cursor()
            self.check_input()
            # display change
            self.update_bacteria_mode(mouse_pos)
            self.game.top_view.fill(self.background)
            self.game.top_view.blit(self.curr_image, (self.bacteria_x, self.bacteria_y))
            self.game.draw_text('The Game Of Life', + self.default_text_gap + 10,  self.mid_w, self.mid_h - 100)
            self.game.draw_text("Run Random", + self.default_text_gap, self.run_random_x, self.run_random_y)
            self.game.draw_text("Run Select", + self.default_text_gap, self.run_select_x, self.run_select_y)
            self.game.draw_text("Load", + self.default_text_gap, self.load_x, self.load_y)
            self.game.draw_text("Setup", + self.default_text_gap, self.setup_x, self.setup_y)
            self.game.draw_text("Info", + self.default_text_gap, self.info_x, self.info_y)
            self.game.draw_text("Quit", + self.default_text_gap, self.quit_x, self.quit_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Run Random' or self.state == 'Run Select':
                self.cursor_offset_x = conf.DEFAULT_CURSOR_X_OFFSET
                self.cursor_rect.midtop = (self.load_x + self.cursor_offset_x, self.load_y + self.cursor_offset_y)
                self.state = 'Load'
            elif self.state == 'Load':
                self.cursor_rect.midtop = (self.setup_x + self.cursor_offset_x, self.setup_y + self.cursor_offset_y)
                self.state = 'Setup'
            elif self.state == 'Setup':
                self.cursor_rect.midtop = (self.info_x + self.cursor_offset_x, self.info_y + self.cursor_offset_y)
                self.state = 'Info'
            elif self.state == 'Info':
                self.cursor_rect.midtop = (self.quit_x + self.cursor_offset_x, self.quit_y + self.cursor_offset_y)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_offset_x = self.run_cursor_offset
                self.cursor_rect.midtop = (self.run_random_x + self.cursor_offset_x, self.run_random_y + self.cursor_offset_y)
                self.state = 'Run Random'
        elif self.game.UP_KEY:
            if self.state == 'Run Random' or self.state == 'Run Select':
                self.cursor_offset_x = conf.DEFAULT_CURSOR_X_OFFSET
                self.cursor_rect.midtop = (self.quit_x + self.cursor_offset_x, self.quit_y + self.cursor_offset_y)
                self.state = 'Quit'
            elif self.state == 'Load':
                self.cursor_offset_x = self.run_cursor_offset
                self.cursor_rect.midtop = (self.run_select_x + self.cursor_offset_x, self.run_select_y + self.cursor_offset_y)
                self.state = 'Run Select'
            elif self.state == 'Setup':
                self.cursor_rect.midtop = (self.load_x + self.cursor_offset_x, self.load_y + self.cursor_offset_y)
                self.state = 'Load'
            elif self.state == 'Info':
                self.cursor_rect.midtop = (self.setup_x + self.cursor_offset_x, self.setup_y + self.cursor_offset_y)
                self.state = 'Setup'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.info_x + self.cursor_offset_x, self.info_y + self.cursor_offset_y)
                self.state = 'Info'
        elif self.game.RIGHT_KEY or self.game.LEFT_KEY:
            if self.state == 'Run Random':
                self.cursor_rect.midtop = (self.run_select_x + self.cursor_offset_x, self.run_select_y + self.cursor_offset_y)
                self.state = 'Run Select'
            elif self.state == 'Run Select':
                self.cursor_rect.midtop = (self.run_random_x + self.cursor_offset_x, self.run_random_y + self.cursor_offset_y)
                self.state = 'Run Random'

    def check_input(self):
        """ Update state and game.curr_menu according to input """
        if self.game.ENTER_KEY:
            if self.state == 'Run Random':
                self.game.run_mode = 'Run'
                self.game.playing = True
            elif self.state == 'Run Select':
                self.game.run_mode = 'Select'
                self.game.playing = True
            elif self.state == 'Load':
                self.game.curr_menu = self.game.load_menu
            elif self.state == 'Setup':
                self.game.curr_menu = self.game.setup_menu
            elif self.state == 'Info':
                self.game.curr_menu = self.game.info_menu
            elif self.state == 'Quit':
                self.game.curr_menu = self.game.quit_menu
            self.run_display = False

    def update_bacteria_mode(self, mouse_pos):
        """ Go in and out of bacteria mode and display image accordingly """
        if mouse_pos is not None:
            if (self.bacteria_x <= mouse_pos[0] <= self.bacteria_x + self.bacteria_size) and \
                    (self.bacteria_y <= mouse_pos[1] <= self.bacteria_y + self.bacteria_size):
                if self.game.bacteria_mode:
                    self.game.bacteria_mode = False
                    self.curr_image = self.bacteria_image
                else:
                    self.game.bacteria_mode = True
                    self.curr_image = self.reverse_image


class LoadMenu(Menu):
    """
    A Load Menu class, works like a state machine

    Important additional attributes:
    -------------------------------

    self.input_window:
        A surface for the interactive text input box.

    self.no_such_name:
        Boolean value for whether the given name input exists.

    """
    def __init__(self, game):
        """ Initialize the LoadMenu object """
        Menu.__init__(self, game)
        self.name_x, self.name_y = self.mid_w, self.mid_h + 20
        self.lable_offset_y = 10
        self.no_such_name = False
        self.input_window = pygame.Surface((600, 38))
        self.input_window.fill(self.background)  # -- should never be seen ---

    def display_menu(self):
        """ Display the menu on the game screen"""
        self.run_display = True
        while self.run_display:
            # basic menu display
            self.game.top_view.fill(self.background)
            self.game.draw_text('Load & Run by name', self.default_text_size + 10, self.game.screen_w / 2, self.game.screen_h / 2 - 50)
            if self.no_such_name:
                self.game.draw_text('Try a different name:', self.default_text_size, self.name_x, self.name_y + self.lable_offset_y)
            else:
                self.game.draw_text('Name:', self.default_text_size, self.name_x, self.name_y + self.lable_offset_y)
            self.blit_screen()
            # interactive text input box, while loop inside
            name = self.game.input_box(200, 200, self.input_window, self.default_text_size, -200, 150, 300)
            # handle text
            self.handle_name_input(name)

    def handle_name_input(self, name):
        """ process the name that was entered in the input box"""
        # if player hit escape
        if name is None:
            self.run_display = False
            self.game.curr_menu = self.game.main_menu
            return

        run_arr = lcr.get_run_arr_by_name(name)
        # if name is empty or there is no match for name
        if run_arr[0] == -1:
            self.no_such_name = True
            return
        else:
            cell_size = run_arr.pop(0)
            self.game.cell_grid.new_grid(cell_size)
        # load coordinates
        for tup in run_arr:
            self.game.cell_grid.grid[tup[0]][tup[1]].live()

        # now play and setup for after the run
        self.run_display = False
        self.game.curr_menu = self.game.main_menu
        self.game.playing = True
        self.game.loaded = True
        return


class SetupMenu(Menu):
    """
    A Setup Menu class, works like a state machine

    Important additional attributes:
    -------------------------------

    self.state (override):
        The states are entries in a 3x2 matrix, each can be active/inactive.

    self.changing_settings:
        This is an intermediate state.
        - When it is [3, 3], the current self.state is inactive.
        User arrows input will change between inactive states.
        - Otherwise, self.state is active.
        User arrows input will affect the settings of the current state.

    self.*_list:
        A list of strings for the different options for * label.

    self.*_index:
        The current index (mode) in  self.*_list.

    """
    def __init__(self, game):
        """ Initialize the Setup Menu object """
        Menu.__init__(self, game)
        self.state = [0, 0]
        self.cursor_offset_x = -175
        self.box_x, self.box_y = self.mid_w - 220, self.mid_h - 20
        self.input_box_x, self.input_box_y = self.mid_w - 220, self.mid_h + 25
        self.box_offset_x = 520
        self.box_offset_y = 120
        self.cursor_rect.midtop = (self.box_x + self.cursor_offset_x, self.box_y)
        self.changing_settings = [3, 3]
        self.speed_list = ['very slow', 'slow', 'medium', 'fast']
        self.cell_size_list = ['small', 'medium', 'large']
        self.alive_color_index = self.colors.index(self.game.alive_cell_color)
        self.dead_color_index = self.colors.index(self.game.dead_cell_color)
        self.area_edge_size = self.game.start_area_edge
        self.life_chance = self.game.life_chance_for_random_start
        self.cell_size_index = self.game.cell_size // 10 - 1
        self.speed_index = conf.SPEED_INDEX
        self.cell_size_text_color, self.speed_index_text_color, self.alive_color_index_text_color,\
            self.dead_color_index_text_color, self.area_edge_size_text_color, self.life_chance_text_color = \
            game.text_color, game.text_color, game.text_color, game.text_color, game.text_color, game.text_color

    def display_menu(self):
        """ Display the menu on the game screen """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input_and_change_state()
            # display text
            self.game.top_view.fill(self.background)
            self.game.draw_text('Setup', self.default_text_size + 10, self.mid_w, self.mid_h - 150)
            self.game.draw_text('Living cell color: ', self.default_text_size, self.box_x, self.box_y, self.alive_color_index_text_color)
            self.game.draw_text("Dead cell color:", self.default_text_size, self.box_x + self.box_offset_x, self.box_y, self.dead_color_index_text_color)
            self.game.draw_text("Speed:", self.default_text_size, self.box_x, self.box_y + self.box_offset_y, self.speed_index_text_color)
            self.game.draw_text("Area size:", self.default_text_size, self.box_x + self.box_offset_x, self.box_y + self.box_offset_y, self.area_edge_size_text_color)
            self.game.draw_text("Spawn chance:", self.default_text_size, self.box_x, self.box_y + self.box_offset_y * 2, self.life_chance_text_color)
            self.game.draw_text("Cell size:", self.default_text_size, self.box_x + self.box_offset_x, self.box_y + self.box_offset_y * 2, self.cell_size_text_color)
            self.game.draw_text("{}".format(self.color_names[self.alive_color_index]), self.default_text_size, self.input_box_x, self.input_box_y)
            self.game.draw_text("{}".format(self.color_names[self.dead_color_index]), self.default_text_size, self.input_box_x + self.box_offset_x, self.input_box_y)
            self.game.draw_text("{}".format(self.speed_list[self.speed_index]), self.default_text_size, self.input_box_x, self.input_box_y + self.box_offset_y)
            self.game.draw_text("{}".format(self.area_edge_size ** 2), self.default_text_size, self.input_box_x + self.box_offset_x, self.input_box_y + self.box_offset_y)
            self.game.draw_text("{}".format(self.life_chance), self.default_text_size, self.input_box_x, self.input_box_y + self.box_offset_y * 2)
            self.game.draw_text("{}".format(self.cell_size_list[self.cell_size_index]), self.default_text_size, self.input_box_x + self.box_offset_x, self.input_box_y + self.box_offset_y * 2)
            self.draw_cursor()
            self.blit_screen()

        # update game parameters
        if self.speed_index == 0:
            self.game.round_time = 0.8
        if self.speed_index == 1:
            self.game.round_time = 0.3
        if self.speed_index == 2:
            self.game.round_time = 0.05
        if self.speed_index == 3:
            self.game.round_time = 0.01
        self.game.cell_grid.new_grid((self.cell_size_index + 1) * 10)
        self.game.alive_cell_color = self.colors[self.alive_color_index]
        self.game.dead_cell_color = self.colors[self.dead_color_index]
        self.game.update_grid_color()
        self.game.start_area_edge = self.area_edge_size
        self.game.life_chance_for_random_start = self.life_chance

    def check_input_and_change_state(self):
        # self.changing_settings != [3, 3] therefor input changes settings.
        if self.changing_settings == [0, 0]:
            if self.game.ENTER_KEY:
                self.changing_settings = [3, 3]
                self.alive_color_index_text_color = self.game.text_color
            elif self.game.UP_KEY:
                self.alive_color_index += 1
                self.alive_color_index %= len(self.colors)
            elif self.game.DOWN_KEY:
                self.alive_color_index -= 1
                self.alive_color_index %= len(self.colors)
        elif self.changing_settings == [1, 0]:
            if self.game.ENTER_KEY:
                self.changing_settings = [3, 3]
                self.dead_color_index_text_color = self.game.text_color
            elif self.game.UP_KEY:
                self.dead_color_index += 1
                self.dead_color_index %= len(self.colors)
            elif self.game.DOWN_KEY:
                self.dead_color_index -= 1
                self.dead_color_index %= len(self.colors)
        elif self.changing_settings == [0, 1]:
            if self.game.ENTER_KEY:
                self.changing_settings = [3, 3]
                self.speed_index_text_color = self.game.text_color
            elif self.game.UP_KEY and self.speed_index < 3:
                self.speed_index += 1
            elif self.game.DOWN_KEY and self.speed_index > 0:
                self.speed_index -= 1
        elif self.changing_settings == [1, 1]:
            if self.game.ENTER_KEY:
                self.changing_settings = [3, 3]
                self.area_edge_size_text_color = self.game.text_color
            elif self.game.UP_KEY and self.area_edge_size < (self.game.screen_h / self.game.cell_size) - 5:
                self.area_edge_size += 1
            elif self.game.DOWN_KEY and self.area_edge_size > 3:
                self.area_edge_size -= 1
        elif self.changing_settings == [0, 2]:
            if self.game.ENTER_KEY:
                self.changing_settings = [3, 3]
                self.life_chance_text_color = self.game.text_color
            elif self.game.UP_KEY and self.life_chance < 1:
                self.life_chance += 0.05
            elif self.game.DOWN_KEY and self.life_chance > 0.1:
                self.life_chance -= 0.05
            self.life_chance = round(self.life_chance, 2)
        elif self.changing_settings == [1, 2]:
            if self.game.ENTER_KEY:
                self.changing_settings = [3, 3]
                self.cell_size_text_color = self.game.text_color
            elif self.game.UP_KEY and self.cell_size_index < 2:
                self.cell_size_index += 1
                self.game.cell_size = (self.cell_size_index + 1) * 10
                self.game.num_of_rows = self.game.screen_h // self.game.cell_size
                self.area_edge_size = min(self.game.num_of_rows - 5, self.area_edge_size)
            elif self.game.DOWN_KEY and self.cell_size_index > 0:
                self.cell_size_index -= 1
                self.game.cell_size = (self.cell_size_index + 1) * 10
                self.game.num_of_rows = self.game.screen_h // self.game.cell_size
                self.area_edge_size = min(self.game.num_of_rows - 5, self.area_edge_size)

        # self.changing_settings == [3, 3] therefor input changes inactive states.
        else:
            got_input = False
            if self.game.ESCAPE_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            elif self.game.UP_KEY:
                self.state[0] += 0
                self.state[1] += -1
                got_input = True
            elif self.game.DOWN_KEY:
                self.state[0] += 0
                self.state[1] += 1
                got_input = True
            elif self.game.RIGHT_KEY:
                self.state[0] += 1
                self.state[1] += 0
                got_input = True
            elif self.game.LEFT_KEY:
                self.state[0] += -1
                self.state[1] += 0
                got_input = True
            elif self.game.ENTER_KEY:
                self.changing_settings = self.state
                if self.changing_settings == [0, 0]:
                    self.alive_color_index_text_color = self.game.selected_text_color
                elif self.changing_settings == [1, 0]:
                    self.dead_color_index_text_color = self.game.selected_text_color
                elif self.changing_settings == [0, 1]:
                    self.speed_index_text_color = self.game.selected_text_color
                elif self.changing_settings == [1, 1]:
                    self.area_edge_size_text_color = self.game.selected_text_color
                elif self.changing_settings == [0, 2]:
                    self.life_chance_text_color = self.game.selected_text_color
                elif self.changing_settings == [1, 2]:
                    self.cell_size_text_color = self.game.selected_text_color

            if got_input:
                self.state[0] = self.state[0] % 2
                self.state[1] = self.state[1] % 3
                self.cursor_rect.midtop = (self.box_x + self.cursor_offset_x + self.box_offset_x * self.state[0],
                                           self.box_y + self.box_offset_y * self.state[1])


class InfoMenu(Menu):
    """
    An Info Menu class, just a screen.
    """
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.top_view.fill(self.background)
            with open('assets/info.txt', 'r') as info_file:
                for i, line in enumerate(info_file.readlines()):
                    self.game.draw_text(line[:-1], self.default_text_size + 5, self.game.screen_w / 2, self.game.screen_h / 2 - 350 + 40*i)

            self.blit_screen()

    def check_input(self):
        if self.game.ESCAPE_KEY or self.game.ENTER_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False


class QuitMenu(Menu):
    """
    A Quit Menu class, works like a state machine
    """
    def __init__(self, game):
        """ Initialize the Quit Menu object """
        Menu.__init__(self, game)
        self.exit = False
        self.state = 'NO'
        self.no_x, self.no_y = self.mid_w, self.mid_h + 20
        self.yes_x, self.yes_y = self.mid_w, self.mid_h + 80
        self.cursor_offset_x = -35
        self.cursor_offset_y = 4
        self.lable_offset_y = 10
        self.cursor_rect.midtop = (self.no_x + self.cursor_offset_x, self.no_y + self.lable_offset_y +
                                   self.cursor_offset_y)

    def display_menu(self):
        """
        Display the menu on the game screen.
        If returns -1, the game will quit.
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            if self.exit:
                return -1
            if self.game.ESCAPE_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.top_view.fill(self.background)
            self.game.draw_text('ARE YOU SURE?', self.default_text_size + 10, self.game.screen_w / 2, self.game.screen_h / 2 - 50)
            self.game.draw_text('NO', self.default_text_size, self.no_x, self.no_y + self.lable_offset_y)
            self.game.draw_text('YES', self.default_text_size, self.yes_x, self.yes_y + self.lable_offset_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.state == 'NO':
            if self.game.ENTER_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            if self.game.UP_KEY or self.game.DOWN_KEY:
                self.state = 'YES'
                self.cursor_rect.midtop = (self.yes_x + self.cursor_offset_x, self.yes_y + self.lable_offset_y +
                                           self.cursor_offset_y)
        elif self.state == 'YES':
            if self.game.ENTER_KEY:
                self.exit = True
            elif self.game.UP_KEY or self.game.DOWN_KEY:
                self.state = 'NO'
                self.cursor_rect.midtop = (self.no_x + self.cursor_offset_x, self.no_y + self.lable_offset_y +
                                           self.cursor_offset_y)
