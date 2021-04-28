import copy

import pygame
from enum import Enum

import thorpy

from GUI.tile import Tile
from Models import game_state
from Utility.constants import *
from GUI.file_reader import FileReader
from Utility.enum import *

# Empty board for testing purposes, can take this and copy/paste it into a board setup
# to force ai to take certain movements
empty_board = [
            Tile(8, 4, "I5", None), Tile(8, 5, "I6", None), Tile(8, 6, "I7", None),
            Tile(8, 7, "I8", None), Tile(8, 8, "I9", None),
            Tile(7, 3, "H4", None), Tile(7, 4, "H5", None), Tile(7, 5, "H6", None),
            Tile(7, 6, "H7", None), Tile(7, 7, "H8", None), Tile(7, 8, "H9", None),
            Tile(6, 2, "G3", None), Tile(6, 3, "G4", None), Tile(6, 4, "G5", None),
            Tile(6, 5, "G6", None), Tile(6, 6, "G7", None), Tile(6, 7, "G8", None),
            Tile(6, 8, "G9", None),
            Tile(5, 1, "F2", None), Tile(5, 2, "F3", None), Tile(5, 3, "F4", None), Tile(5, 4, "F5", None),
            Tile(5, 5, "F6", None), Tile(5, 6, "F7", None), Tile(5, 7, "F8", None), Tile(5, 8, "F9", None),
            Tile(4, 0, "E1", None), Tile(4, 1, "E2", None), Tile(4, 2, "E3", None), Tile(4, 3, "E4", None),
            Tile(4, 4, "E5", None), Tile(4, 5, "E6", None), Tile(4, 6, "E7", None), Tile(4, 7, "E8", None),
            Tile(4, 8, "E9", None),
            Tile(3, 0, "D1", None), Tile(3, 1, "D2", None), Tile(3, 2, "D3", None), Tile(3, 3, "D4", None),
            Tile(3, 4, "D5", None), Tile(3, 5, "D6", None), Tile(3, 6, "D7", None), Tile(3, 7, "D8", None),
            Tile(2, 0, "C1", None), Tile(2, 1, "C2", None), Tile(2, 2, "C3", None),
            Tile(2, 3, "C4", None), Tile(2, 4, "C5", None), Tile(2, 5, "C6", None),
            Tile(2, 6, "C7", None),
            Tile(1, 0, "B1", None), Tile(1, 1, "B2", None), Tile(1, 2, "B3", None),
            Tile(1, 3, "B4", None), Tile(1, 4, "B5", None), Tile(1, 5, "B6", None),
            Tile(0, 0, "A1", None), Tile(0, 1, "A2", None), Tile(0, 2, "A3", None),
            Tile(0, 3, "A4", None), Tile(0, 4, "A5", None),
        ]


class Board:
    """
    Class which represents the board in the game window.
    """

    def __init__(self):
        # NOTE: the board [] is used for the GUI, and the board_dict is for state_space_gen
        self.board = []
        self.board_dict = {}
        self.forbidden_spots = ['A0', 'A6', 'B0', 'B7', 'C0', 'C8', 'D0', 'D9',
                                'E0', 'E10', 'F1', 'F10', 'G2', 'G10', 'H3', 'H10', 'I4', 'I10',
                                '@0', '@1', '@2', '@3', '@4', '@5', '@6', 'J4', 'J5', 'J6', 'J7',
                                'J8', 'J9', 'J10']
        self.movements = [Movement.Left, Movement.Right, Movement.UpLeft, Movement.UpRight,
                          Movement.DownLeft, Movement.DownRight]
        pass

    def set_board(self, board, board_dict):
        # Function to set board easier when undoing a move
        self.board = board
        self.board_dict = board_dict

    def build_board(self, window, layout):
        # Build the board from scratch
        self.board = []
        self.board_dict = {}

        if layout == 'default':
            self.set_default_tiles()
        elif layout == 'german_daisy':
            self.set_german_daisy_tiles()
        elif layout == 'belgian_daisy':
            self.set_belgian_daisy_tiles()
        self.convert_to_dict()  # Converts board from list to dict rep.
        self.update_board(window)
        pygame.display.update()

    def set_default_tiles(self):
        """
        Set the board for a Standard start.
        """
        self.board = [
            Tile(8, 4, "I5", white_piece_id), Tile(8, 5, "I6", white_piece_id), Tile(8, 6, "I7", white_piece_id),
            Tile(8, 7, "I8", white_piece_id), Tile(8, 8, "I9", white_piece_id),
            Tile(7, 3, "H4", white_piece_id), Tile(7, 4, "H5", white_piece_id), Tile(7, 5, "H6", white_piece_id),
            Tile(7, 6, "H7", white_piece_id), Tile(7, 7, "H8", white_piece_id), Tile(7, 8, "H9", white_piece_id),
            Tile(6, 2, "G3", None), Tile(6, 3, "G4", None), Tile(6, 4, "G5", white_piece_id),
            Tile(6, 5, "G6", white_piece_id), Tile(6, 6, "G7", white_piece_id), Tile(6, 7, "G8", None),
            Tile(6, 8, "G9", None),
            Tile(5, 1, "F2", None), Tile(5, 2, "F3", None), Tile(5, 3, "F4", None), Tile(5, 4, "F5", None),
            Tile(5, 5, "F6", None), Tile(5, 6, "F7", None), Tile(5, 7, "F8", None), Tile(5, 8, "F9", None),
            Tile(4, 0, "E1", None), Tile(4, 1, "E2", None), Tile(4, 2, "E3", None), Tile(4, 3, "E4", None),
            Tile(4, 4, "E5", None), Tile(4, 5, "E6", None), Tile(4, 6, "E7", None), Tile(4, 7, "E8", None),
            Tile(4, 8, "E9", None),
            Tile(3, 0, "D1", None), Tile(3, 1, "D2", None), Tile(3, 2, "D3", None), Tile(3, 3, "D4", None),
            Tile(3, 4, "D5", None), Tile(3, 5, "D6", None), Tile(3, 6, "D7", None), Tile(3, 7, "D8", None),
            Tile(2, 0, "C1", None), Tile(2, 1, "C2", None), Tile(2, 2, "C3", black_piece_id),
            Tile(2, 3, "C4", black_piece_id), Tile(2, 4, "C5", black_piece_id), Tile(2, 5, "C6", None),
            Tile(2, 6, "C7", None),
            Tile(1, 0, "B1", black_piece_id), Tile(1, 1, "B2", black_piece_id), Tile(1, 2, "B3", black_piece_id),
            Tile(1, 3, "B4", black_piece_id), Tile(1, 4, "B5", black_piece_id), Tile(1, 5, "B6", black_piece_id),
            Tile(0, 0, "A1", black_piece_id), Tile(0, 1, "A2", black_piece_id), Tile(0, 2, "A3", black_piece_id),
            Tile(0, 3, "A4", black_piece_id), Tile(0, 4, "A5", black_piece_id),
        ]

        # self.board = [
        #     Tile(8, 4, "I5", None), Tile(8, 5, "I6", None), Tile(8, 6, "I7", None),
        #     Tile(8, 7, "I8", None), Tile(8, 8, "I9", None),
        #     Tile(7, 3, "H4", None), Tile(7, 4, "H5", None), Tile(7, 5, "H6", None),
        #     Tile(7, 6, "H7", None), Tile(7, 7, "H8", None), Tile(7, 8, "H9", None),
        #     Tile(6, 2, "G3", None), Tile(6, 3, "G4", None), Tile(6, 4, "G5", None),
        #     Tile(6, 5, "G6", None), Tile(6, 6, "G7", None), Tile(6, 7, "G8", None),
        #     Tile(6, 8, "G9", None),
        #     Tile(5, 1, "F2", None), Tile(5, 2, "F3", None), Tile(5, 3, "F4", None), Tile(5, 4, "F5", None),
        #     Tile(5, 5, "F6", None), Tile(5, 6, "F7", None), Tile(5, 7, "F8", None), Tile(5, 8, "F9", None),
        #     Tile(4, 0, "E1", None), Tile(4, 1, "E2", None), Tile(4, 2, "E3", None), Tile(4, 3, "E4", None),
        #     Tile(4, 4, "E5", None), Tile(4, 5, "E6", None), Tile(4, 6, "E7", None), Tile(4, 7, "E8", None),
        #     Tile(4, 8, "E9", None),
        #     Tile(3, 0, "D1", None), Tile(3, 1, "D2", None), Tile(3, 2, "D3", None), Tile(3, 3, "D4", None),
        #     Tile(3, 4, "D5", None), Tile(3, 5, "D6", None), Tile(3, 6, "D7", None), Tile(3, 7, "D8", None),
        #     Tile(2, 0, "C1", None), Tile(2, 1, "C2", None), Tile(2, 2, "C3", white_piece_id),
        #     Tile(2, 3, "C4", black_piece_id), Tile(2, 4, "C5", black_piece_id), Tile(2, 5, "C6", None),
        #     Tile(2, 6, "C7", None),
        #     Tile(1, 0, "B1", None), Tile(1, 1, "B2", None), Tile(1, 2, "B3", None),
        #     Tile(1, 3, "B4", None), Tile(1, 4, "B5", None), Tile(1, 5, "B6", None),
        #     Tile(0, 0, "A1", None), Tile(0, 1, "A2", None), Tile(0, 2, "A3", None),
        #     Tile(0, 3, "A4", None), Tile(0, 4, "A5", None),
        # ]
        self.convert_to_dict()

    def set_belgian_daisy_tiles(self):
        """
        Set the board for a German Daisy start.
        """
        self.board = [
            Tile(8, 4, "I5", white_piece_id), Tile(8, 5, "I6", white_piece_id), Tile(8, 6, "I7", None),
            Tile(8, 7, "I8", black_piece_id), Tile(8, 8, "I9", black_piece_id),
            Tile(7, 3, "H4", white_piece_id), Tile(7, 4, "H5", white_piece_id), Tile(7, 5, "H6", white_piece_id),
            Tile(7, 6, "H7", black_piece_id), Tile(7, 7, "H8", black_piece_id), Tile(7, 8, "H9", black_piece_id),
            Tile(6, 2, "G3", None), Tile(6, 3, "G4", white_piece_id), Tile(6, 4, "G5", white_piece_id),
            Tile(6, 5, "G6", None), Tile(6, 6, "G7", black_piece_id), Tile(6, 7, "G8", black_piece_id),
            Tile(6, 8, "G9", None),
            Tile(5, 1, "F2", None), Tile(5, 2, "F3", None), Tile(5, 3, "F4", None), Tile(5, 4, "F5", None),
            Tile(5, 5, "F6", None), Tile(5, 6, "F7", None), Tile(5, 7, "F8", None), Tile(5, 8, "F9", None),
            Tile(4, 0, "E1", None), Tile(4, 1, "E2", None), Tile(4, 2, "E3", None), Tile(4, 3, "E4", None),
            Tile(4, 4, "E5", None), Tile(4, 5, "E6", None), Tile(4, 6, "E7", None), Tile(4, 7, "E8", None),
            Tile(4, 8, "E9", None),
            Tile(3, 0, "D1", None), Tile(3, 1, "D2", None), Tile(3, 2, "D3", None), Tile(3, 3, "D4", None),
            Tile(3, 4, "D5", None), Tile(3, 5, "D6", None), Tile(3, 6, "D7", None), Tile(3, 7, "D8", None),
            Tile(2, 0, "C1", None), Tile(2, 1, "C2", black_piece_id), Tile(2, 2, "C3", black_piece_id),
            Tile(2, 3, "C4", None), Tile(2, 4, "C5", white_piece_id), Tile(2, 5, "C6", white_piece_id),
            Tile(2, 6, "C7", None),
            Tile(1, 0, "B1", black_piece_id), Tile(1, 1, "B2", black_piece_id), Tile(1, 2, "B3", black_piece_id),
            Tile(1, 3, "B4", white_piece_id), Tile(1, 4, "B5", white_piece_id), Tile(1, 5, "B6", white_piece_id),
            Tile(0, 0, "A1", black_piece_id), Tile(0, 1, "A2", black_piece_id), Tile(0, 2, "A3", None),
            Tile(0, 3, "A4", white_piece_id), Tile(0, 4, "A5", white_piece_id),
        ]
        self.convert_to_dict()

    def set_german_daisy_tiles(self):
        """
        Set the board for a Belgian Daisy start.
        """
        self.board = [
            Tile(8, 4, "I5", None), Tile(8, 5, "I6", None), Tile(8, 6, "I7", None), Tile(8, 7, "I8", None),
            Tile(8, 8, "I9", None),
            Tile(7, 3, "H4", white_piece_id), Tile(7, 4, "H5", white_piece_id), Tile(7, 5, "H6", None),
            Tile(7, 6, "H7", None), Tile(7, 7, "H8", black_piece_id), Tile(7, 8, "H9", black_piece_id),
            Tile(6, 2, "G3", white_piece_id), Tile(6, 3, "G4", white_piece_id), Tile(6, 4, "G5", white_piece_id),
            Tile(6, 5, "G6", None), Tile(6, 6, "G7", black_piece_id), Tile(6, 7, "G8", black_piece_id),
            Tile(6, 8, "G9", black_piece_id),
            Tile(5, 1, "F2", None), Tile(5, 2, "F3", white_piece_id), Tile(5, 3, "F4", white_piece_id),
            Tile(5, 4, "F5", None), Tile(5, 5, "F6", None), Tile(5, 6, "F7", black_piece_id),
            Tile(5, 7, "F8", black_piece_id), Tile(5, 8, "F9", None),
            Tile(4, 0, "E1", None), Tile(4, 1, "E2", None), Tile(4, 2, "E3", None), Tile(4, 3, "E4", None),
            Tile(4, 4, "E5", None), Tile(4, 5, "E6", None), Tile(4, 6, "E7", None), Tile(4, 7, "E8", None),
            Tile(4, 8, "E9", None),
            Tile(3, 0, "D1", None), Tile(3, 1, "D2", black_piece_id), Tile(3, 2, "D3", black_piece_id),
            Tile(3, 3, "D4", None), Tile(3, 4, "D5", None), Tile(3, 5, "D6", white_piece_id),
            Tile(3, 6, "D7", white_piece_id), Tile(3, 7, "D8", None),
            Tile(2, 0, "C1", black_piece_id), Tile(2, 1, "C2", black_piece_id), Tile(2, 2, "C3", black_piece_id),
            Tile(2, 3, "C4", None), Tile(2, 4, "C5", white_piece_id), Tile(2, 5, "C6", white_piece_id),
            Tile(2, 6, "C7", white_piece_id),
            Tile(1, 0, "B1", black_piece_id), Tile(1, 1, "B2", black_piece_id), Tile(1, 2, "B3", None),
            Tile(1, 3, "B4", None), Tile(1, 4, "B5", white_piece_id), Tile(1, 5, "B6", white_piece_id),
            Tile(0, 0, "A1", None), Tile(0, 1, "A2", None), Tile(0, 2, "A3", None), Tile(0, 3, "A4", None),
            Tile(0, 4, "A5", None),
        ]
        self.convert_to_dict()

    def generate_board(self, marbles):
        """
        Function read_data in file reader provides positions to generate board. These positions are
        turned into tiles and placed within the hashtable representing the board. The remainder of
        the board is filled with empty tiles and the game board is updated.
        """
        board_out = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': []}
        rows = ['A15', 'B16', 'C17', 'D18', 'E19', 'F29', 'G39', 'H49', 'I59']
        for marble in marbles:
            tile = Tile.generate_tile(marble)
            board_out[marble[0]].append(tile)
        for row in rows:
            curr_row = board_out[row[0]]
            tiles_occupied = [x.get_coord() for x in curr_row]
            row_int = ord(row[0]) - 65
            start = int(row[1]) - 1
            end = int(row[2])
            for x in range(start, end):
                tile_id = row[0] + str(x + 1)
                if tile_id not in tiles_occupied:
                    curr_row.append(Tile(row_int, x, tile_id, None))
        self.board = board_out

    def generate_single_moves(self, black_marbles: list, white_marbles: list, turn: chr):
        """
        Checks all possible directions for a single marble to move then ensures
        that the generated location is not occupied or out of bounds. The resulting array
        consists of multiple board configurations, one for each move found possible.
        """
        forbidden = self.forbidden_spots
        result = []
        moves = []
        movements = self.movements
        if turn == 'b':
            marbles = black_marbles
        else:
            marbles = white_marbles
        for marble in marbles:
            letter, num = self.convert_to_nums(marble)
            left = self.convert_to_string(letter, num - 1)
            right = self.convert_to_string(letter, num + 1)
            upL = self.convert_to_string(letter + 1, num)
            upR = self.convert_to_string(letter + 1, num + 1)
            downL = self.convert_to_string(letter - 1, num - 1)
            downR = self.convert_to_string(letter - 1, num)
            test_spots = [left, right, upL, upR, downL, downR]
            for spot in test_spots:
                # Deep copy needed for each turn to generate output for board file.
                if turn == 'b':
                    array_copy = copy.deepcopy(black_marbles)
                else:
                    array_copy = copy.deepcopy(white_marbles)
                if spot not in white_marbles and spot not in black_marbles and spot not in forbidden:
                    index = array_copy.index(marble)
                    array_copy.remove(marble)
                    array_copy.insert(index, spot)
                    # Merges lists in black-white order for output
                    if turn == 'b':
                        array_copy.sort()
                        array_copy = [x + 'b' for x in array_copy]
                        white_marbles_out = [x + 'w' for x in white_marbles]
                        final_output = array_copy + white_marbles_out

                        move_index = test_spots.index(spot)
                        move = {"start": [marble + 'b'],
                                "end": [spot + 'b'],
                                "move": movements[move_index],
                                "elim": False, "pushes": 0}
                        moves.append(move)
                    else:
                        array_copy.sort()
                        array_copy = [x + 'w' for x in array_copy]
                        black_marbles_out = [x + 'b' for x in black_marbles]
                        final_output = black_marbles_out + array_copy

                        move_index = test_spots.index(spot)
                        move = {"start": [marble + 'w'],
                                "end": [spot + 'w'],
                                "move": movements[move_index],
                                "elim": False, "pushes": 0}
                        moves.append(move)
                    result.append(final_output)
        return result, moves

    def generate_double_sets(self, black_marbles: list, white_marbles: list, turn: chr):
        """
        Create pairs for marbles that can move together to assist in generating moves
        for 2 marbles. Each marble pair is stored as a tuple and the result is a list
        of tuples.
        """
        result = []
        if turn == 'b':
            marbles = black_marbles
        else:
            marbles = white_marbles
        for marble in marbles:
            letter, num = self.convert_to_nums(marble)
            right = self.convert_to_string(letter, num + 1)
            upL = self.convert_to_string(letter + 1, num)
            upR = self.convert_to_string(letter + 1, num + 1)
            pair_locations = [right, upL, upR]
            for second_marble in pair_locations:
                if second_marble in marbles:
                    result.append((marble, second_marble))
        return result

    @staticmethod
    def strip_active_marbles(marbles: list, active_marbles: tuple):
        """
        Helper function for generating moves. Returns a list of marbles with
        the marbles currently being tested removed from the list.
        """
        result = copy.deepcopy(marbles)
        for marble in active_marbles:
            result.remove(marble)
        return result

    @staticmethod
    def replace_marbles(marbles: list, old_positions: list, new_positions: list):
        """
        Helper function for generating moves. Replaces the previous configuration of marbles
        with the new updated positions following a successful move.
        """
        final_marbles = copy.deepcopy(marbles)
        for x in range(len(old_positions)):
            index = final_marbles.index(old_positions[x])
            final_marbles.remove(old_positions[x])
            final_marbles.insert(index, new_positions[x])
        return final_marbles

    @staticmethod
    def replace_marble(marbles: list, old_position: str, new_position: str):
        """
        Helper function for generating moves. Replaces a single old position with the new updated
        position.
        """
        final_marbles = copy.deepcopy(marbles)
        index = final_marbles.index(old_position)
        final_marbles.remove(old_position)
        final_marbles.insert(index, new_position)
        return final_marbles

    @staticmethod
    def remove_marble(marbles: list, removed_marble: str):
        """
        Handles a marble falling out of the board and removes it from the list of marbles.
        Returns the updated list.
        """
        final_marbles = copy.deepcopy(marbles)
        final_marbles.remove(removed_marble)
        return final_marbles

    def generate_double_moves_without_collision(self, black_marbles: list, white_marbles: list,
                                                turn: chr, marble_pairs: list):
        """
        Generates all moves for a pair of marbles that do not collide with any other marble
        on the field, be it black or white.
        """
        result = []
        forbidden = self.forbidden_spots
        marbles = black_marbles + white_marbles
        moves = []
        movements = self.movements
        for marble_tuple in marble_pairs:
            current_marbles = self.strip_active_marbles(marbles, marble_tuple)
            one_letter, one_num = self.convert_to_nums(marble_tuple[0])
            two_letter, two_num = self.convert_to_nums(marble_tuple[1])

            one_left = self.convert_to_string(one_letter, one_num - 1)
            one_right = self.convert_to_string(one_letter, one_num + 1)
            if one_left not in current_marbles and one_left not in forbidden:
                two_left = self.convert_to_string(two_letter, two_num - 1)
                if two_left not in current_marbles and two_left not in forbidden:
                    old_positions = [x for x in marble_tuple]
                    new_positions = [one_left, two_left]
                    if turn == 'b':
                        final_black_marbles = self.replace_marbles(black_marbles, old_positions, new_positions)
                        final_black_marbles.sort()
                        final_black_marbles = [x + 'b' for x in final_black_marbles]
                        white_marbles_out = [x + 'w' for x in white_marbles]
                        final_output = final_black_marbles + white_marbles_out

                        move = {"start": [x + 'b' for x in old_positions],
                                "end": [x + 'b' for x in new_positions],
                                "move": Movement.Left,
                                "elim": False, "pushes": 0}
                    else:
                        final_white_marbles = self.replace_marbles(white_marbles, old_positions, new_positions)
                        final_white_marbles.sort()
                        final_white_marbles = [x + 'w' for x in final_white_marbles]
                        black_marbles_out = [x + 'b' for x in black_marbles]
                        final_output = black_marbles_out + final_white_marbles

                        move = {"start": [x + 'w' for x in old_positions],
                                "end": [x + 'w' for x in new_positions],
                                "move": Movement.Left,
                                "elim": False, "pushes": 0}
                    moves.append(move)
                    result.append(final_output)
            if one_right not in current_marbles and one_right not in forbidden:
                two_right = self.convert_to_string(two_letter, two_num + 1)
                if two_right not in current_marbles and two_right not in forbidden:
                    old_positions = [x for x in marble_tuple]
                    new_positions = [one_right, two_right]
                    if turn == 'b':
                        final_black_marbles = self.replace_marbles(black_marbles, old_positions, new_positions)
                        final_black_marbles.sort()
                        final_black_marbles = [x + 'b' for x in final_black_marbles]
                        white_marbles_out = [x + 'w' for x in white_marbles]
                        final_output = final_black_marbles + white_marbles_out

                        move = {"start": [x + 'b' for x in old_positions],
                                "end": [x + 'b' for x in new_positions],
                                "move": Movement.Right,
                                "elim": False, "pushes": 0}
                    else:
                        final_white_marbles = self.replace_marbles(white_marbles, old_positions, new_positions)
                        final_white_marbles.sort()
                        final_white_marbles = [x + 'w' for x in final_white_marbles]
                        black_marbles_out = [x + 'b' for x in black_marbles]
                        final_output = black_marbles_out + final_white_marbles

                        move = {"start": [x + 'w' for x in old_positions],
                                "end": [x + 'w' for x in new_positions],
                                "move": Movement.Right,
                                "elim": False, "pushes": 0}
                    moves.append(move)
                    result.append(final_output)

            one_upL = self.convert_to_string(one_letter + 1, one_num)
            one_upR = self.convert_to_string(one_letter + 1, one_num + 1)
            one_downL = self.convert_to_string(one_letter - 1, one_num - 1)
            one_downR = self.convert_to_string(one_letter - 1, one_num)
            two_upL = self.convert_to_string(two_letter + 1, two_num)
            two_upR = self.convert_to_string(two_letter + 1, two_num + 1)
            two_downL = self.convert_to_string(two_letter - 1, two_num - 1)
            two_downR = self.convert_to_string(two_letter - 1, two_num)
            one_spots = [one_upL, one_upR, one_downL, one_downR]
            two_spots = [two_upL, two_upR, two_downL, two_downR]
            for spot in one_spots:
                if spot not in current_marbles and spot not in forbidden:
                    index = one_spots.index(spot)
                    second_spot = two_spots[index]
                    if second_spot not in current_marbles and second_spot not in forbidden:
                        old_positions = [x for x in marble_tuple]
                        new_positions = [spot, second_spot]
                        if turn == 'b':
                            final_black_marbles = self.replace_marbles(black_marbles, old_positions, new_positions)
                            final_black_marbles.sort()
                            final_black_marbles = [x + 'b' for x in final_black_marbles]
                            white_marbles_out = [x + 'w' for x in white_marbles]
                            final_output = final_black_marbles + white_marbles_out

                            move = {"start": [x + 'b' for x in old_positions],
                                    "end": [x + 'b' for x in new_positions],
                                    "move": movements[index + 2],
                                    "elim": False, "pushes": 0}
                        else:
                            final_white_marbles = self.replace_marbles(white_marbles, old_positions, new_positions)
                            final_white_marbles.sort()
                            final_white_marbles = [x + 'w' for x in final_white_marbles]
                            black_marbles_out = [x + 'b' for x in black_marbles]
                            final_output = black_marbles_out + final_white_marbles

                            move = {"start": [x + 'w' for x in old_positions],
                                    "end": [x + 'w' for x in new_positions],
                                    "move": movements[index + 2],
                                    "elim": False, "pushes": 0}
                        moves.append(move)
                        result.append(final_output)
        return result, moves

    def double_marble_collisions(self, forbidden: list, black_marbles: list, white_marbles: list, turn: chr,
                                 marble_spot_one_move: list,
                                 marble_spot_two_move: list, marble_tuple: tuple, enemy_marbles: list,
                                 current_marbles: list, result: list, movement: Enum, moves: list):
        """
        Checks if a given set of 2 marbles can make a push move on the board and stores all resulting board
        configurations from each possible push.
        """
        for marble_move_one in marble_spot_one_move:
            # One enemy marble next to column of 2 player marbles.
            if marble_move_one in enemy_marbles and marble_move_one not in forbidden:
                index = marble_spot_one_move.index(marble_move_one)
                marble_move_two = marble_spot_two_move[index]
                if marble_move_two in current_marbles:
                    # Two consecutive enemy marbles or a friendly marble found blocking push, skip and continue
                    continue
                # One enemy marble at the edge of the board to be pushed off
                elif marble_move_two in forbidden:
                    if turn == 'b':
                        final_enemy_marbles = self.remove_marble(white_marbles, marble_move_one)
                        final_player_marbles = self.replace_marbles(black_marbles, [x for x in marble_tuple],
                                                                    marble_spot_one_move)
                        final_enemy_marbles.sort()
                        final_player_marbles.sort()
                        final_player_marbles = [x + 'b' for x in final_player_marbles]
                        final_enemy_marbles = [x + 'w' for x in final_enemy_marbles]
                        result.append(final_player_marbles + final_enemy_marbles)

                        move = {"start": [x + 'b' for x in marble_tuple],
                                "end": [x + 'b' for x in marble_spot_one_move],
                                "e_start": [marble_move_one],
                                "e_end": [marble_move_two],
                                "move": movement,
                                "elim": True, "pushes": 1}
                        moves.append(move)
                    else:
                        final_enemy_marbles = self.remove_marble(black_marbles, marble_move_one)
                        final_player_marbles = self.replace_marbles(white_marbles, [x for x in marble_tuple],
                                                                    marble_spot_one_move)
                        final_enemy_marbles.sort()
                        final_player_marbles.sort()
                        final_player_marbles = [x + 'w' for x in final_player_marbles]
                        final_enemy_marbles = [x + 'b' for x in final_enemy_marbles]
                        result.append(final_enemy_marbles + final_player_marbles)

                        move = {"start": [x + 'w' for x in marble_tuple],
                                "end": [x + 'w' for x in marble_spot_one_move],
                                "e_start": [marble_move_one],
                                "e_end": [marble_move_two],
                                "move": movement,
                                "elim": True, "pushes": 1}
                        moves.append(move)
                # Empty spot after enemy marble
                else:
                    if turn == 'b':
                        final_enemy_marbles = self.replace_marble(white_marbles, marble_move_one, marble_move_two)
                        final_player_marbles = self.replace_marbles(black_marbles, [x for x in marble_tuple],
                                                                    marble_spot_one_move)
                        final_enemy_marbles.sort()
                        final_player_marbles.sort()
                        final_player_marbles = [x + 'b' for x in final_player_marbles]
                        final_enemy_marbles = [x + 'w' for x in final_enemy_marbles]
                        result.append(final_player_marbles + final_enemy_marbles)

                        move = {"start": [x + 'b' for x in marble_tuple],
                                "end": [x + 'b' for x in marble_spot_one_move],
                                "e_start": [marble_move_one + 'w'],
                                "e_end": [marble_move_two + 'w'],
                                "move": movement,
                                "elim": False, "pushes": 1}
                        moves.append(move)
                    else:
                        final_enemy_marbles = self.replace_marble(black_marbles, marble_move_one, marble_move_two)
                        final_player_marbles = self.replace_marbles(white_marbles, [x for x in marble_tuple],
                                                                    marble_spot_one_move)
                        final_enemy_marbles.sort()
                        final_player_marbles.sort()
                        final_player_marbles = [x + 'w' for x in final_player_marbles]
                        final_enemy_marbles = [x + 'b' for x in final_enemy_marbles]
                        result.append(final_enemy_marbles + final_player_marbles)

                        move = {"start": [x + 'w' for x in marble_tuple],
                                "end": [x + 'w' for x in marble_spot_one_move],
                                "e_start": [marble_move_one + 'b'],
                                "e_end": [marble_move_two + 'b'],
                                "move": movement,
                                "elim": False, "pushes": 1}
                        moves.append(move)

    def generate_double_moves_with_collision(self, black_marbles: list, white_marbles: list,
                                             turn: chr, marble_pairs: list):
        """
        Generates all possible board configurations from moving two marbles and pushing an
        opponents marble.
        """
        result = []
        moves = []
        marbles = black_marbles + white_marbles
        forbidden = self.forbidden_spots
        if turn == 'b':
            enemy_marbles = white_marbles
        else:
            enemy_marbles = black_marbles
        for marble_tuple in marble_pairs:
            current_marbles = self.strip_active_marbles(marbles, marble_tuple)
            one_letter, one_num = self.convert_to_nums(marble_tuple[0])
            two_letter, two_num = self.convert_to_nums(marble_tuple[1])
            # Marbles in-line horizontally
            if one_letter == two_letter:
                marble_spots_one_left = [self.convert_to_string(one_letter, one_num - 1),
                                         self.convert_to_string(two_letter, two_num - 1)]
                marble_spots_two_left = [self.convert_to_string(one_letter, one_num - 2),
                                         self.convert_to_string(two_letter, two_num - 2)]
                marble_spots_one_right = [self.convert_to_string(one_letter, one_num + 1),
                                          self.convert_to_string(two_letter, two_num + 1)]
                marble_spots_two_right = [self.convert_to_string(one_letter, one_num + 2),
                                          self.convert_to_string(two_letter, two_num + 2)]
                # Pushing marble left case
                self.double_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_one_left,
                                              marble_spots_two_left, marble_tuple, enemy_marbles, current_marbles,
                                              result, Movement.Left, moves)
                self.double_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_one_right,
                                              marble_spots_two_right, marble_tuple, enemy_marbles, current_marbles,
                                              result, Movement.Right, moves)
            # Marbles in-line diagonally with left slant
            elif one_num == two_num:
                marble_spots_upL_one = [self.convert_to_string(one_letter + 1, one_num),
                                        self.convert_to_string(two_letter + 1, two_num)]
                marble_spots_upL_two = [self.convert_to_string(one_letter + 2, one_num),
                                        self.convert_to_string(two_letter + 2, two_num)]
                marble_spots_downR_one = [self.convert_to_string(one_letter - 1, one_num),
                                          self.convert_to_string(two_letter - 1, two_num)]
                marble_spots_downR_two = [self.convert_to_string(one_letter - 2, one_num),
                                          self.convert_to_string(two_letter - 2, two_num)]
                self.double_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_upL_one,
                                              marble_spots_upL_two, marble_tuple, enemy_marbles, current_marbles,
                                              result, Movement.UpLeft, moves)
                self.double_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_downR_one,
                                              marble_spots_downR_two, marble_tuple, enemy_marbles, current_marbles,
                                              result, Movement.DownRight, moves)
            # Marbles in-line diagonally with right slant
            else:
                marble_spots_upR_one = [self.convert_to_string(one_letter + 1, one_num + 1),
                                        self.convert_to_string(two_letter + 1, two_num + 1)]
                marble_spots_upR_two = [self.convert_to_string(one_letter + 2, one_num + 2),
                                        self.convert_to_string(two_letter + 2, two_num + 2)]
                marble_spots_downL_one = [self.convert_to_string(one_letter - 1, one_num - 1),
                                          self.convert_to_string(two_letter - 1, two_num - 1)]
                marble_spots_downL_two = [self.convert_to_string(one_letter - 2, one_num - 2),
                                          self.convert_to_string(two_letter - 2, two_num - 2)]
                self.double_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_upR_one,
                                              marble_spots_upR_two, marble_tuple, enemy_marbles, current_marbles,
                                              result, Movement.UpRight, moves)
                self.double_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_downL_one,
                                              marble_spots_downL_two, marble_tuple, enemy_marbles, current_marbles,
                                              result, Movement.DownLeft, moves)
        return result, moves

    def generate_triple_sets(self, black_marbles: list, white_marbles: list, turn: chr):
        """
        Create triplets for marbles that can move together to assist in generating moves
        for 3 marbles. Each marble triplet is stored as a tuple and the result is a list
        of tuples.
        """
        result = []
        if turn == 'b':
            marbles = black_marbles
        else:
            marbles = white_marbles
        for marble in marbles:
            letter, num = self.convert_to_nums(marble)
            right = self.convert_to_string(letter, num + 1)
            upL = self.convert_to_string(letter + 1, num)
            upR = self.convert_to_string(letter + 1, num + 1)
            potential_pair_one_spot = [right, upL, upR]
            right_2 = self.convert_to_string(letter, num + 2)
            upL_2 = self.convert_to_string(letter + 2, num)
            upR_2 = self.convert_to_string(letter + 2, num + 2)
            potential_pair_two_spots = [right_2, upL_2, upR_2]
            for second_marble in potential_pair_one_spot:
                if second_marble in marbles:
                    index = potential_pair_one_spot.index(second_marble)
                    third_marble = potential_pair_two_spots[index]
                    if third_marble in marbles:
                        result.append((marble, second_marble, third_marble))
        return result

    def generate_triple_moves_without_collision(self, black_marbles: list, white_marbles: list,
                                                turn: chr, marble_pairs: list):
        """
        Generates all moves for a triplet of marbles that do not collide with any other marble
        on the field, be it black or white.
        """
        result = []
        moves = []
        movements = self.movements
        forbidden = self.forbidden_spots
        marbles = black_marbles + white_marbles
        for marble_tuple in marble_pairs:
            current_marbles = self.strip_active_marbles(marbles, marble_tuple)
            one_letter, one_num = self.convert_to_nums(marble_tuple[0])
            two_letter, two_num = self.convert_to_nums(marble_tuple[1])
            three_letter, three_num = self.convert_to_nums(marble_tuple[2])

            one_left = self.convert_to_string(one_letter, one_num - 1)
            one_right = self.convert_to_string(one_letter, one_num + 1)
            if one_left not in current_marbles and one_left not in forbidden:
                two_left = self.convert_to_string(two_letter, two_num - 1)
                if two_left not in current_marbles and two_left not in forbidden:
                    three_left = self.convert_to_string(three_letter, three_num - 1)
                    if three_left not in current_marbles and three_left not in forbidden:
                        old_positions = [x for x in marble_tuple]
                        new_positions = [one_left, two_left, three_left]
                        if turn == 'b':
                            final_black_marbles = self.replace_marbles(black_marbles, old_positions, new_positions)
                            final_black_marbles.sort()
                            final_black_marbles = [x + 'b' for x in final_black_marbles]
                            white_marbles_out = [x + 'w' for x in white_marbles]
                            final_output = final_black_marbles + white_marbles_out

                            move = {"start": [x + 'b' for x in old_positions],
                                    "end": [x + 'b' for x in new_positions],
                                    "move": Movement.Left,
                                    "elim": False, "pushes": 0}
                        else:
                            final_white_marbles = self.replace_marbles(white_marbles, old_positions, new_positions)
                            final_white_marbles.sort()
                            final_white_marbles = [x + 'w' for x in final_white_marbles]
                            black_marbles_out = [x + 'b' for x in black_marbles]
                            final_output = black_marbles_out + final_white_marbles

                            move = {"start": [x + 'w' for x in old_positions],
                                    "end": [x + 'w' for x in new_positions],
                                    "move": Movement.Left,
                                    "elim": False, "pushes": 0}
                        moves.append(move)
                        result.append(final_output)
            if one_right not in current_marbles and one_right not in forbidden:
                two_right = self.convert_to_string(two_letter, two_num + 1)
                if two_right not in current_marbles and two_right not in forbidden:
                    three_right = self.convert_to_string(three_letter, three_num + 1)
                    if three_right not in current_marbles and three_right not in forbidden:
                        old_positions = [x for x in marble_tuple]
                        new_positions = [one_right, two_right, three_right]
                        if turn == 'b':
                            final_black_marbles = self.replace_marbles(black_marbles, old_positions, new_positions)
                            final_black_marbles.sort()
                            final_black_marbles = [x + 'b' for x in final_black_marbles]
                            white_marbles_out = [x + 'w' for x in white_marbles]
                            final_output = final_black_marbles + white_marbles_out

                            move = {"start": [x + 'b' for x in old_positions],
                                    "end": [x + 'b' for x in new_positions],
                                    "move": Movement.Right,
                                    "elim": False, "pushes": 0}
                        else:
                            final_white_marbles = self.replace_marbles(white_marbles, old_positions, new_positions)
                            final_white_marbles.sort()
                            final_white_marbles = [x + 'w' for x in final_white_marbles]
                            black_marbles_out = [x + 'b' for x in black_marbles]
                            final_output = black_marbles_out + final_white_marbles

                            move = {"start": [x + 'w' for x in old_positions],
                                    "end": [x + 'w' for x in new_positions],
                                    "move": Movement.Right,
                                    "elim": False, "pushes": 0}
                        moves.append(move)
                        result.append(final_output)

            one_upL = self.convert_to_string(one_letter + 1, one_num)
            one_upR = self.convert_to_string(one_letter + 1, one_num + 1)
            one_downL = self.convert_to_string(one_letter - 1, one_num - 1)
            one_downR = self.convert_to_string(one_letter - 1, one_num)
            two_upL = self.convert_to_string(two_letter + 1, two_num)
            two_upR = self.convert_to_string(two_letter + 1, two_num + 1)
            two_downL = self.convert_to_string(two_letter - 1, two_num - 1)
            two_downR = self.convert_to_string(two_letter - 1, two_num)
            three_upL = self.convert_to_string(three_letter + 1, three_num)
            three_upR = self.convert_to_string(three_letter + 1, three_num + 1)
            three_downL = self.convert_to_string(three_letter - 1, three_num - 1)
            three_downR = self.convert_to_string(three_letter - 1, three_num)
            one_spots = [one_upL, one_upR, one_downL, one_downR]
            two_spots = [two_upL, two_upR, two_downL, two_downR]
            three_spots = [three_upL, three_upR, three_downL, three_downR]
            for spot in one_spots:
                if spot not in current_marbles and spot not in forbidden:
                    index = one_spots.index(spot)
                    second_spot = two_spots[index]
                    if second_spot not in current_marbles and second_spot not in forbidden:
                        third_spot = three_spots[index]
                        if third_spot not in current_marbles and third_spot not in forbidden:
                            old_positions = [x for x in marble_tuple]
                            new_positions = [spot, second_spot, third_spot]
                            if turn == 'b':
                                final_black_marbles = self.replace_marbles(black_marbles, old_positions,
                                                                           new_positions)
                                final_black_marbles.sort()
                                final_black_marbles = [x + 'b' for x in final_black_marbles]
                                white_marbles_out = [x + 'w' for x in white_marbles]
                                final_output = final_black_marbles + white_marbles_out

                                move = {"start": [x + 'b' for x in old_positions],
                                        "end": [x + 'b' for x in new_positions],
                                        "move": movements[index + 2],
                                        "elim": False, "pushes": 0}
                            else:
                                final_white_marbles = self.replace_marbles(white_marbles, old_positions,
                                                                           new_positions)
                                final_white_marbles.sort()
                                final_white_marbles = [x + 'w' for x in final_white_marbles]
                                black_marbles_out = [x + 'b' for x in black_marbles]
                                final_output = black_marbles_out + final_white_marbles

                                move = {"start": [x + 'w' for x in old_positions],
                                        "end": [x + 'w' for x in new_positions],
                                        "move": movements[index + 2],
                                        "elim": False, "pushes": 0}
                            moves.append(move)
                            result.append(final_output)
        return result, moves

    def triple_marble_collisions(self, forbidden: list, black_marbles: list, white_marbles: list, turn: chr,
                                 marble_spot_one_move: list, marble_spot_two_move: list,
                                 marble_spot_three_move: list, marble_tuple: tuple,
                                 enemy_marbles: list, current_marbles: list, result: list, movement: Enum, moves: list):
        """
        Checks if a given set of 3 marbles can make a push move on the board and stores all resulting board
        configurations from each possible push.
        """
        for marble_move_one in marble_spot_one_move:
            # One enemy marble next to column of 3 player marbles.
            if marble_move_one in enemy_marbles and marble_move_one not in forbidden:
                index = marble_spot_one_move.index(marble_move_one)
                marble_move_two = marble_spot_two_move[index]
                # Two enemy marbles in-line side by side
                if marble_move_two in enemy_marbles:
                    marble_move_three = marble_spot_three_move[index]
                    # Third spot is occupied by enemy or friendly marble, push cannot occur.
                    if marble_move_three in current_marbles:
                        continue
                    # Third spot off board, pushing 2 marbles and 1 falls out
                    elif marble_move_three in forbidden:
                        if turn == 'b':
                            temp_enemy_marbles = self.remove_marble(white_marbles, marble_move_two)
                            final_enemy_marbles = self.replace_marble(temp_enemy_marbles, marble_move_one,
                                                                      marble_move_two)
                            final_player_marbles = self.replace_marbles(black_marbles, [x for x in marble_tuple],
                                                                        marble_spot_one_move)
                            final_enemy_marbles.sort()
                            final_player_marbles.sort()
                            final_player_marbles = [x + 'b' for x in final_player_marbles]
                            final_enemy_marbles = [x + 'w' for x in final_enemy_marbles]
                            result.append(final_player_marbles + final_enemy_marbles)

                            move = {"start": [x + 'b' for x in marble_tuple],
                                    "end": [x + 'b' for x in marble_spot_one_move],
                                    "e_start": [marble_move_one + 'w', marble_move_two + 'w'],
                                    "e_end": [marble_move_two + 'w', marble_move_three + 'w'],
                                    "move": movement,
                                    "elim": True, "pushes": 2}
                            moves.append(move)
                        else:
                            temp_enemy_marbles = self.remove_marble(black_marbles, marble_move_two)
                            final_enemy_marbles = self.replace_marble(temp_enemy_marbles, marble_move_one,
                                                                      marble_move_two)
                            final_player_marbles = self.replace_marbles(white_marbles, [x for x in marble_tuple],
                                                                        marble_spot_one_move)
                            final_enemy_marbles.sort()
                            final_player_marbles.sort()
                            final_player_marbles = [x + 'w' for x in final_player_marbles]
                            final_enemy_marbles = [x + 'b' for x in final_enemy_marbles]
                            result.append(final_enemy_marbles + final_player_marbles)

                            move = {"start": [x + 'w' for x in marble_tuple],
                                    "end": [x + 'w' for x in marble_spot_one_move],
                                    "e_start": [marble_move_one + 'b', marble_move_two + 'b'],
                                    "e_end": [marble_move_two + 'b', marble_move_three + 'b'],
                                    "move": movement,
                                    "elim": True, "pushes": 2}
                            moves.append(move)
                    # Third spot empty, pushing 2 marbles
                    else:
                        if turn == 'b':
                            final_enemy_marbles = self.replace_marbles(white_marbles,
                                                                       [marble_move_one, marble_move_two],
                                                                       [marble_move_two, marble_move_three])
                            final_player_marbles = self.replace_marbles(black_marbles, [x for x in marble_tuple],
                                                                        marble_spot_one_move)
                            final_enemy_marbles.sort()
                            final_player_marbles.sort()
                            final_player_marbles = [x + 'b' for x in final_player_marbles]
                            final_enemy_marbles = [x + 'w' for x in final_enemy_marbles]
                            result.append(final_player_marbles + final_enemy_marbles)

                            move = {"start": [x + 'b' for x in marble_tuple],
                                    "end": [x + 'b' for x in marble_spot_one_move],
                                    "e_start": [marble_move_one + 'w', marble_move_two + 'w'],
                                    "e_end": [marble_move_two + 'w', marble_move_three + 'w'],
                                    "move": movement,
                                    "elim": False, "pushes": 2}
                            moves.append(move)
                        else:
                            final_enemy_marbles = self.replace_marbles(black_marbles,
                                                                       [marble_move_one, marble_move_two],
                                                                       [marble_move_two, marble_move_three])
                            final_player_marbles = self.replace_marbles(white_marbles, [x for x in marble_tuple],
                                                                        marble_spot_one_move)
                            final_enemy_marbles.sort()
                            final_player_marbles.sort()
                            final_player_marbles = [x + 'w' for x in final_player_marbles]
                            final_enemy_marbles = [x + 'b' for x in final_enemy_marbles]
                            result.append(final_enemy_marbles + final_player_marbles)

                            move = {"start": [x + 'w' for x in marble_tuple],
                                    "end": [x + 'w' for x in marble_spot_one_move],
                                    "e_start": [marble_move_one + 'b', marble_move_two + 'b'],
                                    "e_end": [marble_move_two + 'b', marble_move_three + 'b'],
                                    "move": movement,
                                    "elim": False, "pushes": 2}
                            moves.append(move)
                # One enemy marble at the edge of the board to be pushed off
                elif marble_move_two in forbidden:
                    if turn == 'b':
                        final_enemy_marbles = self.remove_marble(white_marbles, marble_move_one)
                        final_player_marbles = self.replace_marbles(black_marbles, [x for x in marble_tuple],
                                                                    marble_spot_one_move)
                        final_enemy_marbles.sort()
                        final_player_marbles.sort()
                        final_player_marbles = [x + 'b' for x in final_player_marbles]
                        final_enemy_marbles = [x + 'w' for x in final_enemy_marbles]
                        result.append(final_player_marbles + final_enemy_marbles)

                        move = {"start": [x + 'b' for x in marble_tuple],
                                "end": [x + 'b' for x in marble_spot_one_move],
                                "e_start": [marble_move_one + 'w'],
                                "e_end": [marble_move_two + 'w'],
                                "move": movement,
                                "elim": True, "pushes": 1}
                        moves.append(move)
                    else:
                        final_enemy_marbles = self.remove_marble(black_marbles, marble_move_one)
                        final_player_marbles = self.replace_marbles(white_marbles, [x for x in marble_tuple],
                                                                    marble_spot_one_move)
                        final_enemy_marbles.sort()
                        final_player_marbles.sort()
                        final_player_marbles = [x + 'w' for x in final_player_marbles]
                        final_enemy_marbles = [x + 'b' for x in final_enemy_marbles]
                        result.append(final_enemy_marbles + final_player_marbles)

                        move = {"start": [x + 'w' for x in marble_tuple],
                                "end": [x + 'w' for x in marble_spot_one_move],
                                "e_start": [marble_move_one + 'b'],
                                "e_end": [marble_move_two + 'b'],
                                "move": movement,
                                "elim": True, "pushes": 1}
                        moves.append(move)
                # Friendly marble on the opposite side of the enemy marble blocking the push by 3 marbles.
                elif marble_move_two not in enemy_marbles and marble_move_two not \
                        in forbidden and marble_move_two in current_marbles:
                    continue
                # Empty spot after enemy marble
                else:
                    if turn == 'b':
                        final_enemy_marbles = self.replace_marble(white_marbles, marble_move_one, marble_move_two)
                        final_player_marbles = self.replace_marbles(black_marbles, [x for x in marble_tuple],
                                                                    marble_spot_one_move)
                        final_enemy_marbles.sort()
                        final_player_marbles.sort()
                        final_player_marbles = [x + 'b' for x in final_player_marbles]
                        final_enemy_marbles = [x + 'w' for x in final_enemy_marbles]
                        result.append(final_player_marbles + final_enemy_marbles)

                        move = {"start": [x + 'b' for x in marble_tuple],
                                "end": [x + 'b' for x in marble_spot_one_move],
                                "e_start": [marble_move_one + 'w'],
                                "e_end": [marble_move_two + 'w'],
                                "move": movement,
                                "elim": False, "pushes": 1}
                        moves.append(move)
                    else:
                        final_enemy_marbles = self.replace_marble(black_marbles, marble_move_one, marble_move_two)
                        final_player_marbles = self.replace_marbles(white_marbles, [x for x in marble_tuple],
                                                                    marble_spot_one_move)
                        final_enemy_marbles.sort()
                        final_player_marbles.sort()
                        final_player_marbles = [x + 'w' for x in final_player_marbles]
                        final_enemy_marbles = [x + 'b' for x in final_enemy_marbles]
                        result.append(final_enemy_marbles + final_player_marbles)

                        move = {"start": [x + 'w' for x in marble_tuple],
                                "end": [x + 'w' for x in marble_spot_one_move],
                                "e_start": [marble_move_one + 'b'],
                                "e_end": [marble_move_two + 'b'],
                                "move": movement,
                                "elim": False, "pushes": 1}
                        moves.append(move)

    def generate_triple_moves_with_collision(self, black_marbles: list, white_marbles: list,
                                             turn: chr, marble_pairs: list):
        """
        Generates all possible board configurations from moving three marbles and pushing
        opponents marble(s).
        """
        result = []
        moves = []
        marbles = black_marbles + white_marbles
        forbidden = self.forbidden_spots
        if turn == 'b':
            enemy_marbles = white_marbles
        else:
            enemy_marbles = black_marbles
        for marble_tuple in marble_pairs:
            current_marbles = self.strip_active_marbles(marbles, marble_tuple)
            one_letter, one_num = self.convert_to_nums(marble_tuple[0])
            two_letter, two_num = self.convert_to_nums(marble_tuple[1])
            three_letter, three_num = self.convert_to_nums(marble_tuple[2])
            # Marbles in-line horizontally
            if one_letter == two_letter:
                marble_spots_one_left = [self.convert_to_string(one_letter, one_num - 1),
                                         self.convert_to_string(two_letter, two_num - 1),
                                         self.convert_to_string(three_letter, three_num - 1)]
                marble_spots_two_left = [self.convert_to_string(one_letter, one_num - 2),
                                         self.convert_to_string(two_letter, two_num - 2),
                                         self.convert_to_string(three_letter, three_num - 2)]
                marble_spots_three_left = [self.convert_to_string(one_letter, one_num - 3),
                                           self.convert_to_string(two_letter, two_num - 3),
                                           self.convert_to_string(three_letter, three_num - 3)]
                marble_spots_one_right = [self.convert_to_string(one_letter, one_num + 1),
                                          self.convert_to_string(two_letter, two_num + 1),
                                          self.convert_to_string(three_letter, three_num + 1)]
                marble_spots_two_right = [self.convert_to_string(one_letter, one_num + 2),
                                          self.convert_to_string(two_letter, two_num + 2),
                                          self.convert_to_string(three_letter, three_num + 2)]
                marble_spots_three_right = [self.convert_to_string(one_letter, one_num + 3),
                                            self.convert_to_string(two_letter, two_num + 3),
                                            self.convert_to_string(three_letter, three_num + 3)]
                # Pushing marble left case
                self.triple_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_one_left,
                                              marble_spots_two_left, marble_spots_three_left, marble_tuple,
                                              enemy_marbles, current_marbles, result, Movement.Left, moves)
                # Pushing marble right case
                self.triple_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_one_right,
                                              marble_spots_two_right, marble_spots_three_right, marble_tuple,
                                              enemy_marbles, current_marbles, result, Movement.Right, moves)
            # Marbles in-line diagonally with left slant
            elif one_num == two_num:
                marble_spots_upL_one = [self.convert_to_string(one_letter + 1, one_num),
                                        self.convert_to_string(two_letter + 1, two_num),
                                        self.convert_to_string(three_letter + 1, three_num)]
                marble_spots_upL_two = [self.convert_to_string(one_letter + 2, one_num),
                                        self.convert_to_string(two_letter + 2, two_num),
                                        self.convert_to_string(three_letter + 2, three_num)]
                marble_spots_upL_three = [self.convert_to_string(one_letter + 3, one_num),
                                          self.convert_to_string(two_letter + 3, two_num),
                                          self.convert_to_string(three_letter + 3, three_num)]
                marble_spots_downR_one = [self.convert_to_string(one_letter - 1, one_num),
                                          self.convert_to_string(two_letter - 1, two_num),
                                          self.convert_to_string(three_letter - 1, three_num)]
                marble_spots_downR_two = [self.convert_to_string(one_letter - 2, one_num),
                                          self.convert_to_string(two_letter - 2, two_num),
                                          self.convert_to_string(three_letter - 2, three_num)]
                marble_spots_downR_three = [self.convert_to_string(one_letter - 3, one_num),
                                            self.convert_to_string(two_letter - 3, two_num),
                                            self.convert_to_string(three_letter - 3, three_num)]
                self.triple_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_upL_one,
                                              marble_spots_upL_two, marble_spots_upL_three, marble_tuple,
                                              enemy_marbles, current_marbles, result, Movement.UpLeft, moves)
                self.triple_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_downR_one,
                                              marble_spots_downR_two, marble_spots_downR_three, marble_tuple,
                                              enemy_marbles, current_marbles, result, Movement.DownRight, moves)

            # Marbles in-line diagonally with right slant
            else:
                marble_spots_upR_one = [self.convert_to_string(one_letter + 1, one_num + 1),
                                        self.convert_to_string(two_letter + 1, two_num + 1),
                                        self.convert_to_string(three_letter + 1, three_num + 1)]
                marble_spots_upR_two = [self.convert_to_string(one_letter + 2, one_num + 2),
                                        self.convert_to_string(two_letter + 2, two_num + 2),
                                        self.convert_to_string(three_letter + 2, three_num + 2)]
                marble_spots_upR_three = [self.convert_to_string(one_letter + 3, one_num + 3),
                                          self.convert_to_string(two_letter + 3, two_num + 3),
                                          self.convert_to_string(three_letter + 3, three_num + 3)]
                marble_spots_downL_one = [self.convert_to_string(one_letter - 1, one_num - 1),
                                          self.convert_to_string(two_letter - 1, two_num - 1),
                                          self.convert_to_string(three_letter - 1, three_num - 1)]
                marble_spots_downL_two = [self.convert_to_string(one_letter - 2, one_num - 2),
                                          self.convert_to_string(two_letter - 2, two_num - 2),
                                          self.convert_to_string(three_letter - 2, three_num - 2)]
                marble_spots_downL_three = [self.convert_to_string(one_letter - 3, one_num - 3),
                                            self.convert_to_string(two_letter - 3, two_num - 3),
                                            self.convert_to_string(three_letter - 3, three_num - 3)]
                self.triple_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_upR_one,
                                              marble_spots_upR_two, marble_spots_upR_three, marble_tuple,
                                              enemy_marbles, current_marbles, result, Movement.UpRight, moves)
                self.triple_marble_collisions(forbidden, black_marbles, white_marbles, turn, marble_spots_downL_one,
                                              marble_spots_downL_two, marble_spots_downL_three, marble_tuple,
                                              enemy_marbles, current_marbles, result, Movement.DownLeft, moves)
        return result, moves

    def generate_all_boards(self, *args):
        """
        Accepts input in 2 forms:
        - File name only: will determine turn and board state from the file.
        - board, turn: will skip file reading as the board is already known.
        The method will then generate all possible boards and return a list of moves, result boards
        """
        if len(args) == 1:
            turn, current_board = FileReader.read_data(FileReader.load_data(args[0]))
            black_marbles, white_marbles = self.read_marbles(current_board)
        else:
            black_marbles, white_marbles = self.read_marbles(args[0])
            turn = args[1]
        double_marble_sets = self.generate_double_sets(black_marbles, white_marbles, turn)
        triple_marble_sets = self.generate_triple_sets(black_marbles, white_marbles, turn)

        all_single_boards, all_single_moves = self.generate_single_moves(black_marbles, white_marbles, turn)
        double_boards_no_push, double_boards_no_push_moves = self.\
            generate_double_moves_without_collision(black_marbles, white_marbles, turn, double_marble_sets)
        double_boards_push, double_boards_push_moves = self.\
            generate_double_moves_with_collision(black_marbles, white_marbles, turn, double_marble_sets)
        triple_boards_no_push, triple_boards_no_push_moves = self.\
            generate_triple_moves_without_collision(black_marbles, white_marbles, turn, triple_marble_sets)
        triple_boards_push, triple_boards_push_moves = self.\
            generate_triple_moves_with_collision(black_marbles, white_marbles, turn, triple_marble_sets)

        output = []
        for result_board in all_single_boards:
            output.append(result_board)
        for result_board in double_boards_no_push:
            output.append(result_board)
        for result_board in double_boards_push:
            output.append(result_board)
        for result_board in triple_boards_no_push:
            output.append(result_board)
        for result_board in triple_boards_push:
            output.append(result_board)
        if len(args) == 1:
            file_name_out = args[0].split('.')[0] + ".board"
            FileReader.write_data(file_name_out, output)

        all_moves = []
        for move in all_single_moves:
            all_moves.append(move)
        for move in double_boards_no_push_moves:
            all_moves.append(move)
        for move in double_boards_push_moves:
            all_moves.append(move)
        for move in triple_boards_no_push_moves:
            all_moves.append(move)
        for move in triple_boards_push_moves:
            all_moves.append(move)
        if len(args) == 1:
            move_file_out = args[0].split('.')[0] + ".move"
            FileReader.write_moves(move_file_out, all_moves)

        return all_moves, output

    @staticmethod
    def read_marbles(board_state: list):
        """
        Takes the position output of the read data method in File Reader module and returns
        lists of marbles of both players separately.
        """
        black_marbles = []
        white_marbles = []
        for marble in board_state:
            if marble[2] == 'b':
                black_marbles.append(marble[0:2])
            else:
                white_marbles.append(marble[0:2])
        return black_marbles, white_marbles

    @staticmethod
    def convert_to_nums(marble_string):
        """
        Coverts a marble string representation from "A1" to 65, 1 for use in
        generating moves.
        """
        letter = ord(marble_string[0])
        num = int(marble_string[1])
        return letter, num

    @staticmethod
    def convert_to_string(letter, num):
        """
        Coverts a numeric representation of the letter and number for a tile position
        to a string. 65, 1 --> "A1"
        """
        return chr(letter) + str(num)

    def compute_one_move(self, marble, move: Movement):
        """
        Moves a marble in the direction specified by the move.
        :param marble: Tile
        :param move: Enum
        :return: marble after shift.
        """
        letter, num = self.convert_to_nums(marble)
        l_change, n_change = move.value
        letter += l_change
        num += n_change
        result = self.convert_to_string(letter, num)
        return result

    def update_board(self, window):
        """
        Updates the current board, going through the tiles and redrawing the
        images.
        NOTE: As of March 08, this should be fine to leave for the remainder of the
        project (barring geometry changes). Moves and tile changes should be handled
        outside of this method.
        """
        unoccupied = pygame.image.load('Images/unoccupied.png')
        black_stone_image = pygame.image.load('Images/resize_black.png')
        white_stone_image = pygame.image.load('Images/resize_white.png')

        # Iterate through columns, drawing a circle and adding the center point as a tuple to each Tile.
        # beginning has 25 X diff, end of row has a 40 X diff
        # tile_counter = 0
        board_seq = ['I5', 'I6', 'I7', 'I8', 'I9', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'G3', 'G4', 'G5', 'G6', 'G7',
                     'G8', 'G9', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6',
                     'E7', 'E8', 'E9', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'C1', 'C2', 'C3', 'C4', 'C5',
                     'C6', 'C7', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'A1', 'A2', 'A3', 'A4', 'A5']
        board_seq_iter = iter(board_seq)

        font_text = pygame.font.SysFont('Ariel', 22)
        current_y = board_start_y + piece_radius
        for col in [5, 6, 7, 8, 9, 8, 7, 6, 5]:

            current_x = ((10 - col) * piece_radius) + piece_distance + board_start_x

            for row in range(0, col):
                coord = next(board_seq_iter)
                if self.board_dict[coord].piece is None:
                    rect = window.blit(unoccupied, (current_x, current_y))
                    self.board_dict[coord].set_rect(rect)
                elif self.board_dict[coord].piece == white_piece_id:
                    rect = window.blit(white_stone_image, (current_x, current_y))
                    self.board_dict[coord].set_rect(rect)
                elif self.board_dict[coord].piece == black_piece_id:
                    rect = window.blit(black_stone_image, (current_x, current_y))
                    self.board_dict[coord].set_rect(rect)

                # TODO: style this or something
                position = (current_x + (piece_radius/2), current_y + (piece_radius/2))
                coord_title = thorpy.make_text(self.board_dict[coord].get_coord(), 12, black)
                coord_title.set_topleft(position)
                coord_title.blit()
                coord_title.update()

                current_x += (piece_radius * 2) + piece_distance
            current_y += (piece_radius * 2) + piece_distance
        pygame.display.update()

    def swap_tiles(self, coord_a: tuple, coord_b: tuple):
        """
        Swaps the pieces of two tiles.
        :param coord_a: int
        :param coord_b: int
        """
        tile_a_coord_id = f"{chr(ord('A') + coord_a[0])}{coord_a[1] + 1}"
        tile_a = self.board_dict[tile_a_coord_id]

        tile_b_coord_id = f"{chr(ord('A') + coord_b[0])}{coord_b[1] + 1}"
        tile_b = self.board_dict[tile_b_coord_id]

        print(f"Swapping {tile_a.board_coordinate} and {tile_b.board_coordinate}")
        temp = tile_b.piece
        tile_b.piece = tile_a.piece
        tile_a.piece = temp

    def convert_to_dict(self):
        board_dict = {}
        for tile in self.board:
            board_dict[tile.board_coordinate] = tile
        self.board_dict = board_dict

    def update_scores(self):
        white_score = 0
        black_score = 0

        for tile in self.board:
            if tile.piece == white_piece_id:
                white_score += 1
            if tile.piece == black_piece_id:
                black_score += 1

        game_state.game_state['white']['score'] = 14 - black_score
        game_state.game_state['black']['score'] = 14 - white_score

    def to_string_state(self):
        # Get board in string state
        board_state = []
        for key in self.board_dict:
            if self.board_dict[key].get_piece() == white_piece_id:
                board_state.append(self.board_dict[key].board_coordinate + 'w')
            elif self.board_dict[key].get_piece() == black_piece_id:
                board_state.append(self.board_dict[key].board_coordinate + 'b')
        return board_state


"""
In order to test input files, add the input file to the GUI folder. You can now enter the name
of the input file where "Test1.input" is written as a string. The program will automatically load and
then generate all possible board configurations for the specified input file. Board and move files will be found
in the GUI folder. 
Note: Run the board.py file directly, using main.py will not provide access to the state generator.
Note: The move file representation for each line is [[Old position], [New position], Movement_Performed]
"""
if __name__ == '__main__':
    board = Board()
    board.generate_all_boards("Test4.input")
