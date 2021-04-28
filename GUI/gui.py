import textwrap
from threading import Thread

import thorpy
import random

from GUI import gui_controls
from GUI.board import Board
from Models import state_timer
from Utility.constants import *
from Utility.enum import Vector, vector_to_movement_enum
from Utility.enum import Turn
from operator import itemgetter
from GUI.gui_controls import *


class GUI:
    """
    The Game class is the driver of the Abalone game. It initiates
    the setup to open a window and run the game.
    """

    def __init__(self):
        """
        Initialize GUI with empty window and console, which are to be built after the GUI is initialized
        """
        self.alternate_turns = True
        self.toggle_players = True
        self.board = Board()
        self.window = None
        self.console = None
        self.selected_pieces = []
        self.player_turn = Turn.BLACK

    def run(self):
        """
        Builds the GUI and then runs the main loop, calling methods to build different pieces
        """
        # Build window, board, console
        self.build_window()
        self.board.build_board(self.window, 'default')
        self.build_console()
        self.draw_score_and_time()
        self.update_printer()
        self.update_move_printer()
        self.set_scoreboard()
        state_timer.start_state_timer(self)
        pygame.display.set_caption("Abalone")

        # self.play_music()
        thread1 = Thread(target=self.start_game_loop)
        thread1.start()
        thread1.run()

    @staticmethod
    def play_music():
        pygame.mixer.music.load('../COMP3981_project/Utility/monsters_inc.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

    def start_game_loop(self):
        clock = pygame.time.Clock()
        while True:

            for event in pygame.event.get():
                # GUI buttons react to event
                self.console.react(event)

                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    self.handle_click(pos)

            pygame.display.update()

    def dumb_stuff(self):
        """
        Draws two flashing rectangles. Probably best we get rid of this.
        """
        rect = pygame.Rect(975, 450, 320, 450)
        pygame.draw.rect(self.window, [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], rect)

        rect2 = pygame.Rect(1200, 0, 100, 450)
        pygame.draw.rect(self.window, [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], rect2)

    def handle_click(self, pos):
        state = game_state.game_state['game']['state']

        # Only deal with board clicks, ThorPy will react to GUI clicks in main loop
        if pos[0] < console_start_x:
            if state == 'stopped':
                self.update_printer("Can't play, game is stopped")
            elif state == 'paused':
                self.update_printer("Game is paused, unpause to continue")
            elif state == 'started':

                # Check if it is the AI's turn
                if game_state.game_state['black']['player'] == 'ai' and self.player_turn == Turn.BLACK:
                    self.update_printer("Cannot select pieces while the AI is making its move")
                elif game_state.game_state['white']['player'] == 'ai' and self.player_turn == Turn.WHITE:
                    self.update_printer("Cannot select pieces while the AI is making its move")

                # Good to go
                else:
                    for key, tile in self.board.board_dict.items():
                        if tile.get_rect() is not None and tile.get_rect().collidepoint(pos):
                            print(f"Tile Coords: ({tile.row}, {tile.column})")
                            self.clicked_tile(tile)

    def build_window(self):
        """
        Method to build the game window
        :return: Window
        """
        # Draw screen then game board
        window = pygame.display.set_mode((window_width, window_height))
        window.fill(blue)
        pygame.draw.rect(window, red, (0, 0, board_width, board_height))

        # Music
        # pygame.mixer.music.load('../COMP3981_project/Utility/yea.mp3')
        # pygame.mixer.music.set_volume(0.01)
        # pygame.mixer.music.play()
        self.window = window

    def build_console(self):
        """
        Builds the buttons and widgets to be displayed to the right of the board
        The process of adding elements is as follows:
            1. Create desired elements (button, text, etc.)
            2. Make a new thorPy Box and add the new elements to the box
            3. Set the size and position of the box
            4. Call blit() then update() at the bottom of this function so other
                elements are not overwritten
            5. Add the box to self.console at the bottom of this function.
        """
        starting_position_title = thorpy.make_text("Starting Position", 18, (0, 0, 0))
        starting_position_title.set_size((button_length, button_height))

        default_layout_radio = thorpy.Checker.make("Default", type_="radio")
        german_daisy_layout_radio = thorpy.Checker.make("German Daisy", type_="radio")
        belgian_daisy_layout_radio = thorpy.Checker.make("Belgian Daisy", type_="radio")

        # Make property of GUI to access when starting a game
        self.layout_radio_choices = [default_layout_radio, german_daisy_layout_radio, belgian_daisy_layout_radio]
        layout_radio_pool = thorpy.RadioPool(self.layout_radio_choices,
                                             first_value=self.layout_radio_choices[0],
                                             always_value=True)

        set_position_button = thorpy.make_button("Set Board", func=lambda: gui_controls.set_board_button(self))
        set_position_button.set_size((button_length, button_height))

        sep_line = thorpy.Line.make(size=225, type_="horizontal")

        """ CONTROLS BOX """

        start_button = thorpy.make_button("Start", func=lambda: gui_controls.start_game_button(self))
        start_button.set_size((button_length, button_height))

        stop_button = thorpy.make_button("Stop", func=lambda: gui_controls.stop_game_button(self))
        stop_button.set_size((button_length, button_height))

        pause_button = thorpy.make_button("Pause", func=lambda: gui_controls.pause_game_button(self))
        pause_button.set_size((button_length, button_height))

        resume_button = thorpy.make_button("Resume", func=lambda: gui_controls.resume_game_button(self))
        resume_button.set_size((button_length, button_height))

        reset_button = thorpy.make_button("Reset", func=lambda: gui_controls.reset_game_button(self))
        reset_button.set_size((button_length, button_height))

        undo_button = thorpy.make_button("Undo", func=lambda: gui_controls.undo_move_button(self))
        undo_button.set_size((button_length, button_height))

        controls_box = thorpy.Box.make(elements=[
            starting_position_title, default_layout_radio, german_daisy_layout_radio, belgian_daisy_layout_radio,
            set_position_button, sep_line, start_button, stop_button, pause_button, resume_button, reset_button,
            undo_button
        ])
        controls_box.set_size((225, 450))

        """ PLAYER SETTINGS """
        black_settings_title = thorpy.make_text("Black", 22, (0, 0, 0))
        black_settings_title.set_size((button_length, button_height))

        black_move_limit = thorpy.Inserter("Move Limit:", value="")
        black_move_limit.set_size((button_length/2, button_height/2))

        black_move_time_limit = thorpy.Inserter(name="Move Time Limit", value="")
        black_move_time_limit.set_size((button_length/2, button_height/2))

        black_total_time_limit = thorpy.Inserter(name="Total Time Limit", value="")
        black_total_time_limit.set_size((button_length/2, button_height/2))

        # Black human or AI radio group
        self.black_human_radio = thorpy.Checker.make("Human", type_="radio")
        black_ai_radio = thorpy.Checker.make("AI", type_="radio")
        black_radio_choices = [self.black_human_radio, black_ai_radio]
        black_radio_group = thorpy.RadioPool(black_radio_choices,
                                             first_value=black_radio_choices[0],
                                             always_value=True)

        # White human or AI radio group
        self.white_human_radio = thorpy.Checker.make("Human", type_="radio")
        white_ai_radio = thorpy.Checker.make("AI", type_="radio")
        white_radio_choices = [self.white_human_radio, white_ai_radio]
        white_radio_group = thorpy.RadioPool(white_radio_choices,
                                             first_value=white_radio_choices[0],
                                             always_value=True)

        white_settings_title = thorpy.make_text("White", 22, (0, 0, 0))
        white_settings_title.set_size((button_length, button_height))

        white_move_limit = thorpy.Inserter(name="Move Limit", value="")
        white_move_limit.set_size((button_length/2, button_height/2))

        white_move_time_limit = thorpy.Inserter("Move Time Limit", value="")
        white_move_time_limit.set_size((button_length/2, button_height/2))

        white_total_time_limit = thorpy.Inserter(name="Total Time Limit", value="")
        white_total_time_limit.set_size((button_length/2, button_height/2))

        # Put this in a list for sanitization later, must stay in this order
        self.settings_inputs = [black_move_limit, black_move_time_limit, white_move_limit, white_move_time_limit,
                                black_total_time_limit, white_total_time_limit]

        settings_box = thorpy.Box.make(elements=[
            black_settings_title, self.black_human_radio, black_ai_radio, black_move_limit, black_move_time_limit,
            black_total_time_limit, white_settings_title, self.white_human_radio, white_ai_radio, white_move_limit,
            white_move_time_limit, white_total_time_limit
        ])
        settings_box.set_size((225, 450))

        """ MOVEMENT CONTROLS """
        # Row 1
        up_left = thorpy.make_button("UP-L", func=self.test_func_move, params={"vector": Vector.UpLeft})
        up_left.set_size((50, 50))

        up_right = thorpy.make_button("UP-R", func=self.test_func_move, params={"vector": Vector.UpRight})
        up_right.set_size((50, 50))

        up_box = thorpy.Box([up_left, up_right])
        thorpy.store(up_box, mode="h")
        up_box.fit_children()

        # Row 2
        left = thorpy.make_button("<", func=self.test_func_move, params={"vector": Vector.Left})
        left.set_size((50, 50))

        center = thorpy.make_button("Clr", func=self.clear_selected_pieces)
        center.set_size((50, 50))
        center.set_topleft((2000, 1000))

        right = thorpy.make_button(">", func=self.test_func_move, params={"vector": Vector.Right})
        right.set_size((50, 50))

        horiz_box = thorpy.Box([left, center, right])
        thorpy.store(horiz_box, mode="h")
        horiz_box.fit_children()

        # Row 3
        down_left = thorpy.make_button("DN-L", func=self.test_func_move, params={"vector": Vector.DownLeft})
        down_left.set_size((50, 50))

        down_right = thorpy.make_button("DN-R", func=self.test_func_move, params={"vector": Vector.DownRight})
        down_right.set_size((50, 50))
        down_right.stick_to(up_left, target_side="right", self_side="left")

        down_box = thorpy.Box([down_left, down_right])
        thorpy.store(down_box, mode="h")
        down_box.fit_children()

        move_box = thorpy.Box.make(elements=[up_box, horiz_box, down_box])
        move_box.set_size((225, 450))

        # MISC #
        sheesh = thorpy.make_button("Sheesh", func=lambda: gui_controls.sheesh(self))
        sheesh.set_size((100, 50))

        stop = thorpy.make_button("Stop playing", func=lambda: gui_controls.stop_music(self))
        stop.set_size((100, 50))

        sheesh_box = thorpy.Box.make(elements=[sheesh, stop])

        # Set the position of each box, then place
        controls_box.set_topleft((console_start_x, console_start_y))
        controls_box.blit()
        controls_box.update()

        settings_box.set_topleft((console_start_x + 225, 0))
        settings_box.blit()
        settings_box.update()

        move_box.set_topleft((console_start_x, 450))
        move_box.blit()
        move_box.update()

        sheesh_box.set_topleft((1200, 0))
        sheesh_box.blit()
        sheesh_box.update()

        self.console = thorpy.Menu([controls_box, settings_box, move_box, sheesh_box])
        for element in self.console.get_population():
            element.surface = self.window

    def update_printer(self, message=None):
        # Print a string
        pygame.draw.rect(self.window, black, (
            printer_start_x, printer_start_y,
            printer_width, printer_height/2
        ))
        if message is not None:
            pos_x = (printer_start_x + 1 * 1 / 8)
            pos_y = (printer_start_y + 1 * 1 / 32)
            position = pos_x, pos_y
            font_text = pygame.font.SysFont('Ariel', 22)
            wrapper = textwrap.TextWrapper(width=28)
            word_list = wrapper.wrap(text=str(message))

            label = []
            for line in word_list:
                label.append(font_text.render(line, True, white))

            for line in range(len(label)):
                self.window.blit(label[line], (position[0], position[1] + (line * 5) + (15 * line)))
        pygame.display.update()

    def update_move_printer(self, message=None):
        pygame.draw.rect(self.window, red, (
            printer_start_x, printer_start_y + printer_height/2,
            printer_width, printer_height
        ))
        if message is not None:
            pos_x = (printer_start_x + 1 * 1 / 8)
            pos_y = ((printer_start_y + printer_height/2) + 1 * 1 / 32)
            position = pos_x, pos_y
            font_text = pygame.font.SysFont('Ariel', 22)
            wrapper = textwrap.TextWrapper(width=28)
            word_list = wrapper.wrap(text=str(message))

            label = []
            for line in word_list:
                label.append(font_text.render(line, True, white))

            for line in range(len(label)):
                self.window.blit(label[line], (position[0], position[1] + (line * 5) + (15 * line)))
        pygame.display.update()

    def clicked_tile(self, tile):
        # Deals with an event where a tile was clicked

        # Add/remove selected piece to selected pieces
        print(f"Clicked {tile.board_coordinate}, occupied by {tile.piece}")
        if tile not in self.selected_pieces:
            self.selected_pieces.append(tile)
            print(f"Added {tile.board_coordinate}")
            self.update_printer(f"Added {tile.board_coordinate}, selected coordinates: "
                                f"{[tile.board_coordinate for tile in self.selected_pieces]}")

        else:
            self.selected_pieces.remove(tile)
            print(f"Removed {tile.board_coordinate}")
            self.update_printer(f"Removed {tile.board_coordinate}, selected coordinates: "
                                f"{[tile.board_coordinate for tile in self.selected_pieces]}")

        print([tile.board_coordinate for tile in self.selected_pieces])

    @staticmethod
    def sort_selected_pieces(vector: Vector, selected_pieces):
        if vector == Vector.UpLeft:
            vector_rep = (1, 0)
            return sorted(selected_pieces, key=itemgetter('row', 'column'), reverse=True)
        elif vector == Vector.UpRight:
            vector_rep = (1, 1)
            return sorted(selected_pieces, key=itemgetter('row', 'column'), reverse=True)
        elif vector == Vector.Left:
            vector_rep = (0, -1)
            return sorted(selected_pieces, key=itemgetter('column'))
        elif vector == Vector.Right:
            vector_rep = (0, 1)
            return sorted(selected_pieces, key=itemgetter('column'), reverse=True)
        elif vector == Vector.DownLeft:
            vector_rep = (-1, -1)
            return sorted(selected_pieces, key=itemgetter('row', 'column'))
        elif vector == Vector.DownRight:
            vector_rep = (-1, 0)
            return sorted(selected_pieces, key=itemgetter('row', 'column'))

    def test_func_move(self, **kwargs):
        # Check state first to see that game is in progress
        state = game_state.game_state['game']['state']
        if state == 'stopped':
            self.update_printer(message="Game is stopped")
            return
        elif state == 'paused':
            self.update_printer(message="Game is paused")
            return

        print("Move: " + str(kwargs['vector']))
        vector_rep = kwargs['vector']
        try:
            vector = None
            selected_pieces_sorted = None

            vector = vector_to_movement_enum(vector_rep).value
            selected_pieces_sorted = self.sort_selected_pieces(vector_rep, self.selected_pieces)

            if len(selected_pieces_sorted) == 0:
                print("No pieces to move")
                return

            if self.is_valid_selection() and self.is_valid_move(vector, selected_pieces_sorted):
                target_coord = self.find_target_coord(vector, selected_pieces_sorted)

                # Swaps all tiles according to movement vector
                for tile in selected_pieces_sorted:
                    print(f"Moving vector {vector}")
                    self.board.swap_tiles((tile.row, tile.column), (tile.row + vector[0], tile.column + vector[1]))

                # self.board.update_board(self.window)

                self.update_move_printer(f"Moving from {[tile.board_coordinate for tile in self.selected_pieces]} to "
                                         f"")

                if self.toggle_players:
                    self.end_turn()

                return True
            else:
                print("Invalid Move. Clearing selected pieces")
                self.update_printer("Invalid Move. Clearing selected pieces")
                return False

        finally:
            self.selected_pieces.clear()

    def is_valid_selection(self):
        print("Evaluating for valid selection")
        if len(self.selected_pieces) > 3:
            return False
        # prev_tile = None
        selected_pieces_sorted_col = sorted(self.selected_pieces, key=itemgetter('column'))
        for tile in selected_pieces_sorted_col:
            print(tile)
            # Determine consistent piece selection
            if tile.piece != self.player_turn.value:
                print("Wrong color")
                return False

        if not self.is_continuous_row_selection() and not self.is_continuous_diagonal_selection():
            print("Non continuous selection")
            return False
        print("Valid Selection")
        return True

    def is_continuous_row_selection(self):
        prev_tile = None
        selected_pieces_sorted_col = sorted(self.selected_pieces, key=itemgetter('column'))

        # Determine continuous row selection
        for tile in selected_pieces_sorted_col:
            if prev_tile is not None:
                if prev_tile.row != tile.row or prev_tile.column != tile.column - 1:
                    print(f"{prev_tile.column}, {tile.column}")
                    print("Inconsistent row selection")
                    return False
                else:
                    prev_tile = tile
            else:
                prev_tile = tile
        return True

    def is_continuous_diagonal_selection(self):
        # print("Starting Diagonal selection consistency Test.")
        prev_tile = None
        selected_pieces_sorted_row = sorted(self.selected_pieces, key=itemgetter('row'))
        horizontal_vector = None  # Keeps track on either up-right or up-left consistency

        # Determine Continuous diagonal selection
        for tile in selected_pieces_sorted_row:

            # Determine continuous row selection
            if prev_tile is not None:
                if horizontal_vector is None:
                    # Assign horizontal vector based on first and second evaluation.
                    if prev_tile.column + 1 == tile.column:
                        horizontal_vector = 1
                        # print("Looking for up-right diagonal")
                    else:
                        horizontal_vector = 0
                        # print("Looking for up-left diagonal")
                if prev_tile.row + 1 == tile.row:  # Row consistency (increasing)
                    # print(f"Evaluating tile: {prev_tile.column}, {tile.column}")
                    if horizontal_vector is not None:
                        if prev_tile.column + horizontal_vector != tile.column:
                            # print(f"Inconsistent column selection: c1:{prev_tile.column} c2:{tile.column}")
                            return False
                    else:
                        print("Horizontal_vector wasn't assigned. Something went wrong")
                else:
                    # print("Inconsistent row selection")
                    return False
                prev_tile = tile
            else:
                # After first evaluation, assign some variables
                prev_tile = tile
        return True

    def is_valid_move(self, vector: tuple, selected_pieces_sorted: list):
        print("Evaluating if move is valid")
        try:
            target_coord = self.find_target_coord(vector, selected_pieces_sorted)
            print("Target Coord:", end="")
            print(target_coord)
        except KeyError:
            print("Can't move out of bounds.")
            return False

        # Friendly collisions
        print("------Starting Friendly Piece Collision-----")
        if self.determine_piece_collision(vector, selected_pieces_sorted, self.player_turn):
            print("Cannot push your own piece.")
            return False

        if self.player_turn == Turn.BLACK:
            opponent_piece = Turn.WHITE
        else:
            opponent_piece = Turn.BLACK

        # Opponent piece collisions
        # do_stuff = True
        print("------Starting Opponent Piece Collision-----")
        if self.determine_piece_collision(vector, selected_pieces_sorted, opponent_piece):
            print("Collision with opponent piece. Do stuff")
            print("\nDetermining Push")
            if self.is_linear_movement(vector, selected_pieces_sorted):
                print(f"Target Coord: {target_coord}")
                opponent_push_strength = self.find_opposing_push_strength(target_coord, vector)
                print(f"Opp push strength: "
                      f"{opponent_push_strength}")
                if (len(self.selected_pieces) > opponent_push_strength) and (opponent_push_strength != 0):
                    print("SUMITO!!!!!")
                    self.sumito(vector, target_coord)
                    return True
                else:
                    print("Failed Push!")
                    return False
            else:
                print("Collision with non-linear movement. Invalid Move")
                print("Result Vector:")
                print(vector)
                print("Coord")
                for tile in selected_pieces_sorted:
                    print(tile.board_coordinate)
                return False
        return True

    def end_turn(self):
        game_state.update_turn(self)

    def is_linear_movement(self, vector: tuple, selected_pieces_sorted: list):
        print("Linear move test")
        if len(selected_pieces_sorted) == 1:
            return True
        if self.change_coordinate_by_vector(vector, selected_pieces_sorted[1])\
                == selected_pieces_sorted[0].board_coordinate:
            return True
        else:
            return False

    def sumito(self, vector, target_coord):
        current_tile = self.board.board_dict[target_coord]
        temp_prev = None
        # temp_curr = None
        try:
            while current_tile.piece is not None:
                temp_curr = current_tile.piece
                print(current_tile)
                self.board.board_dict[current_tile.board_coordinate].piece = temp_prev
                temp_prev = temp_curr
                current_tile = self.board.board_dict[self.change_coordinate_by_vector(vector, current_tile)]

            current_tile.piece = temp_prev
            return
        except KeyError:
            return

    def determine_piece_collision(self, vector: tuple, selected_pieces_sorted: list, collision_piece_id):
        for tile in selected_pieces_sorted:
            evaluated_next_coord = self.change_coordinate_by_vector(vector, tile)
            evaluated_next_tile = self.board.board_dict[evaluated_next_coord]
            print(f"Current:{tile.board_coordinate}-----Evaluated:{evaluated_next_coord}")
            if evaluated_next_tile.piece == collision_piece_id.value \
                    and evaluated_next_tile not in selected_pieces_sorted:
                print(f"Collision with {collision_piece_id.name}")
                return True
        return False

    @staticmethod
    def change_coordinate_by_vector(vector: tuple, tile):
        new_coord = f"{chr(ord(tile.board_coordinate[0]) + vector[0])}{int(tile.board_coordinate[1]) + vector[1]}"
        return new_coord

    def find_target_coord(self, vector, selected_pieces_sorted):
        coord = self.change_coordinate_by_vector(vector, selected_pieces_sorted[0])
        print("Target coord: ", end="")
        print(coord)
        return self.board.board_dict[coord].board_coordinate

    def find_opposing_push_strength(self, contact_tile, vector):

        push_strength = 0
        try:
            current_tile = self.board.board_dict[contact_tile]
            while True:
                print(f"Current Eval Coord: " + current_tile.board_coordinate + "----Piece: " + str(current_tile.piece))
                if current_tile.piece is None:
                    print("Out by None")
                    return push_strength
                else:
                    next_coord = self.change_coordinate_by_vector(vector, current_tile)
                    print(f"Next coord: {next_coord}")
                    push_strength += 1
                    current_tile = self.board.board_dict[next_coord]
                    print("Incrementing push strength")
                    print(f"Eval Coord: " + current_tile.board_coordinate + "----Piece: " + str(current_tile.piece))
        except KeyError:
            return push_strength

    def toggle_player_move(self):
        if self.player_turn == Turn.WHITE:
            self.player_turn = Turn.BLACK
        else:
            self.player_turn = Turn.WHITE

    def draw_score_and_time(self):
        """
        Builds the boxes for black and white score, time taken, and moves taken.
        Should only be called on startup and resetting the board
        """
        """ BLACK """
        black_score_title = thorpy.make_text("Black", 24, (0, 0, 0))
        black_score_title.set_topleft((50, 640))
        black_score_title.blit()
        black_score_title.update()

        font_text_time_label = pygame.font.SysFont('Ariel', 30)
        black_total_time_taken = font_text_time_label.render("Total Time:", True, black)
        self.window.blit(black_total_time_taken, (25, 675))

        black_turn_time_taken = font_text_time_label.render("Turn Time:", True, black)
        self.window.blit(black_turn_time_taken, (25, 705))

        black_score = font_text_time_label.render("Score:", True, black)
        self.window.blit(black_score, (25, 735))

        black_moves_taken = font_text_time_label.render("Moves Taken:", True, black)
        self.window.blit(black_moves_taken, (25, 765))

        """ WHITE """
        white_score_title = thorpy.make_text("White:", 24, (0, 0, 0))
        white_score_title.set_topleft((550, 640))
        white_score_title.blit()

        white_total_time_taken = font_text_time_label.render("Total Time:", True, black)
        self.window.blit(white_total_time_taken, (525, 675))

        white_turn_time_taken = font_text_time_label.render("Turn Time:", True, black)
        self.window.blit(white_turn_time_taken, (525, 705))

        white_score = font_text_time_label.render("Score:", True, black)
        self.window.blit(white_score, (525, 735))

        white_moves_taken = font_text_time_label.render("Moves Taken:", True, black)
        self.window.blit(white_moves_taken, (525, 765))

        current_turn = font_text_time_label.render("Current Turn:", True, black)
        self.window.blit(current_turn, (590, 25))

        pygame.display.update()

    def set_scoreboard(self):
        # For setting or resetting the score, time, etc.
        self.draw_score_and_time()
        self.update_total_time(Turn.BLACK, 0.0)
        self.update_total_time(Turn.WHITE, 0.0)
        self.update_turn_time(Turn.BLACK, 0.0)
        self.update_turn_time(Turn.WHITE, 0.0)
        self.update_score(Turn.BLACK, "0")
        self.update_score(Turn.WHITE, "0")
        self.update_moves_taken(Turn.BLACK, "0")
        self.update_moves_taken(Turn.WHITE, "0")

    def update_total_time(self, piece_enum, time):
        # Update the aggregate timers

        # Format the time first
        time = "{:.1f}".format(time)
        font_text_time_label = pygame.font.SysFont('Ariel', 30)

        if piece_enum == Turn.WHITE:
            # Draw a box to cover the last value
            pygame.draw.rect(self.window, red, (670, 675, 75, 20))
            time_taken = font_text_time_label.render(str(time), True, black)
            self.window.blit(time_taken, white_total_time_location)

        elif piece_enum == Turn.BLACK:
            # Draw a box to cover the last value
            pygame.draw.rect(self.window, red, (180, 675, 75, 20))
            time_taken = font_text_time_label.render(str(time), True, black)
            self.window.blit(time_taken, black_total_time_location)
        pygame.display.update()

    def update_turn_time(self, piece_enum, time):
        font_text_time_label = pygame.font.SysFont('Ariel', 30)
        time = "{:.1f}".format(time)

        if piece_enum == Turn.WHITE:
            pygame.draw.rect(self.window, red, (670, 705, 75, 20))
            time_taken = font_text_time_label.render(str(time), True, black)
            self.window.blit(time_taken, white_turn_time_taken_location)

        elif piece_enum == Turn.BLACK:
            pygame.draw.rect(self.window, red, (180, 705, 75, 20))
            time_taken = font_text_time_label.render(str(time), True, black)
            self.window.blit(time_taken, black_turn_time_location)
        pygame.display.update()

    def update_score(self, piece_enum, score):
        font_text_time_label = pygame.font.SysFont('Ariel', 30)

        if piece_enum == Turn.WHITE:
            # Draw a box to cover the last value
            pygame.draw.rect(self.window, red, (670, 735, 75, 20))
            time_taken = font_text_time_label.render(str(score), True, black)
            self.window.blit(time_taken, white_score_location)

        elif piece_enum == Turn.BLACK:
            # Draw a box to cover the last value
            pygame.draw.rect(self.window, red, (180, 735, 75, 20))
            time_taken = font_text_time_label.render(str(score), True, black)
            self.window.blit(time_taken, black_score_location)
        pygame.display.update()

    def update_moves_taken(self, piece_enum, moves_taken):
        font_text_time_label = pygame.font.SysFont('Ariel', 30)

        if piece_enum == Turn.WHITE:
            pygame.draw.rect(self.window, red, (670, 765, 75, 20))
            time_taken = font_text_time_label.render(str(moves_taken), True, black)
            self.window.blit(time_taken, white_moves_taken_location)

        elif piece_enum == Turn.BLACK:
            pygame.draw.rect(self.window, red, (180, 765, 75, 20))
            time_taken = font_text_time_label.render(str(moves_taken), True, black)
            self.window.blit(time_taken, black_moves_taken_location)
        pygame.display.update()

    def update_turn_label(self, piece_enum):
        pygame.draw.rect(self.window, red, (610, 55, 80, 25))
        font_text_time_lable = pygame.font.SysFont('Ariel', 30)
        turn_label = font_text_time_lable.render(piece_enum.name, True, black)
        self.window.blit(turn_label, turn_label_location)
        pygame.display.update()

    def clear_selected_pieces(self):
        self.selected_pieces.clear()
        self.update_printer("Cleared piece selection")
