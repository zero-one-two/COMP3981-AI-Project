import _thread
import random

import GUI
from AI.Evaluator import Evaluator
from GUI import movement
from Models import game_state
from Utility.constants import *

out_of_bounds = ['A0', 'A6', 'B0', 'B7', 'C0', 'C8', 'D0', 'D9',
                 'E0', 'E10', 'F1', 'F10', 'G2', 'G10', 'H3', 'H10', 'I4', 'I10',
                 '@0', '@1', '@2', '@3', '@4', '@5', '@6', 'J4', 'J5', 'J6', 'J7',
                 'J8', 'J9', 'J10']


def begin_turn(context: GUI, piece_id):
    execute_thread(context, piece_id)


def execute_thread(context: GUI, piece_id):
    _thread.start_new_thread(calculate, (context, piece_id))


def calculate(context: GUI, piece_id):
    board_state = context.board.to_string_state()
    turn = ('b', 'w')[piece_id == white_piece_id]
    best_move = Evaluator.minimax(board_state, turn)

    # Before executing, check that the game has not changed state
    if game_state.game_state['game']['state'] == 'started':

        # First move is random
        if game_state.game_state['game']['turn'] == 'black' and game_state.game_state['black']['moves_taken'] == 0:
            string_board = context.board.to_string_state()
            moves, resulting_boards = context.board.generate_all_boards(string_board, 'b')
            find_and_execute_move(moves[random.randint(0, len(moves) - 1)], context)
            game_state.update_turn(context)

        else:
            find_and_execute_move(best_move, context)
            game_state.update_turn(context)


def find_and_execute_move(best_move, context: GUI):
    """
    param: best_move: list[str]
    Function to find the type of move (Sumito, push, or move) and call the correct movement function.
    If the best move is to move a single piece, then it will come in
    best_move will come in list with each string being a joined value of the coordinate
    and the colour.
    Ex - ['C3b','C4w']
    """
    start_coordinates = [strip_coordinate(coordinate) for coordinate in best_move['start']]
    end_coordinates = [strip_coordinate(coordinate) for coordinate in best_move['end']]
    pushes = best_move['pushes']

    # Pushing and sumito
    if pushes > 0:
        enemy_end_coordinates = [strip_coordinate(coordinate) for coordinate in best_move['e_end']
                                 if strip_coordinate(coordinate) not in out_of_bounds]
        enemy_start_coordinates = [strip_coordinate(coordinate) for coordinate in best_move['e_start']]

        # Two marbles pushing
        if len(start_coordinates) == 2:

            # Sumito two to one
            if best_move['elim']:
                movement.sumito_two_to_one(context, start_coordinates, end_coordinates)
                game_state.add_to_move_history(context, start_coordinates, end_coordinates)

            # TODO: Test this (Functioning going right)
            # Push two to one
            else:
                # IE D5D6 - D6D7w
                # vector = best_move['move'].value
                # target_coordinate = get_next_coordinate(end_coordinates[1], vector)
                #
                # movement.push_two_to_one(context, start_coordinates[0], start_coordinates[1],
                #                          end_coordinates[0], end_coordinates[1], target_coordinate)
                movement.push_two_to_one(context, start_coordinates, end_coordinates,
                                         enemy_start_coordinates, enemy_end_coordinates)
                game_state.add_to_move_history(context, start_coordinates, end_coordinates)

        # 3-1 Push    (C3C4C5 -> C4C5C6)
        # 3-2 Sumito  (F6F5F4 -> F5F4F3) - Push F2
        # 3-1 Sumito  (F4E3D2 -> E3D2C1) - Push C1
        # 3-2 Sumito  (E5F6G7 -> F6G7H8) - Push I9

        # Three marbles pushing
        if len(start_coordinates) == 3:
            if best_move['elim']:
                vector = best_move['move'].value

                # TODO: Test (DL Works)
                # Sumito 3-1
                if pushes == 1:
                    # movement.sumito_three_to_one(context, start_coordinates[0], end_coordinates[2])
                    movement.sumito_three_to_one(context, start_coordinates, end_coordinates)
                    game_state.add_to_move_history(context, start_coordinates, end_coordinates)

                # TODO: Test this (DL Works)
                # Sumito 3-2
                else:

                    # (D3D4D5) -> (D2D3D4) Pushed off d1

                    movement.sumito_three_to_two(context, start_coordinates, end_coordinates, enemy_start_coordinates,
                                                 enemy_end_coordinates)
                    game_state.add_to_move_history(context, start_coordinates, end_coordinates)

            else:
                vector_tuple = best_move['move'].value

                # TODO: Test this (Right works)
                # Push 3-1
                if pushes == 1:
                    movement.push_three_to_one(context, start_coordinates, end_coordinates, enemy_end_coordinates,
                                               enemy_start_coordinates)
                    game_state.add_to_move_history(context, start_coordinates, end_coordinates)

                # TODO: Test this (Right works)
                # Push 3-2
                else:
                    # Ex - (G6G7G8 -> G5G6G7) Pushed (G5G4 -> G4G3)
                    movement.push_three_to_two(context, start_coordinates, end_coordinates, enemy_start_coordinates,
                                               enemy_end_coordinates)
                    game_state.add_to_move_history(context, start_coordinates, end_coordinates)

    # If not pushing, move to designated coordinates
    else:
        # Move one stone
        # Start/end coordinates come in strings instead of list in this situation
        if len(start_coordinates) == 1:

            # TODO: Double check end coordinates will length of 1
            movement.move_1_piece(context, start_coordinates[0], end_coordinates[0])
            game_state.add_to_move_history(context, start_coordinates, end_coordinates)

        # Move two stones
        elif len(start_coordinates) == 2:
            movement.move_2_pieces(context, start_coordinates[0], start_coordinates[1], end_coordinates[0],
                                   end_coordinates[1])
            game_state.add_to_move_history(context, start_coordinates, end_coordinates)

        # Move three stones
        elif len(start_coordinates) == 3:
            movement.move_3_pieces(context, start_coordinates[0], start_coordinates[1], start_coordinates[2],
                                   end_coordinates[0], end_coordinates[1], end_coordinates[2])
            game_state.add_to_move_history(context, start_coordinates, end_coordinates)


def strip_coordinate(move_string):
    return move_string[:-1]
