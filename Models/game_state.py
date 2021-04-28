import copy
import pygame
import GUI
from AI import ai_main
from GUI import gui_updater
from Utility.constants import *
from Utility.enum import *

game_state = {
    'game': {
        'state': 'stopped',  # paused, stopped, started
        'turn': 'black'  # black, white
    },
    'config': {
        'starting_layout': '',  # default, german daisy, belgian daisy
        'time_elapsed': 0,
    },
    'black': {
        'player': '',  # human, ai
        'move_limit': 0,
        'time_limit': 0,
        'total_time_limit': 0,
        'score': 0,
        'moves_taken': 0,
        'move_time': 0,
        'total_time': 0
    },
    'white': {
        'player': '',  # human, ai
        'move_limit': 0,
        'time_limit': 0,
        'total_time_limit': 0,
        'score': 0,
        'moves_taken': 0,
        'move_time': 0,
        'total_time': 0
    }
}

# Add to the histories in the from-to format:
#   [a, b, c][x, y, z]
move_history_black = [[], []]
move_history_white = [[], []]
board_history = []
state_history = []


def start_game(context: GUI):
    # Can only start from a stopped position with valid text from inputs
    if game_state['game']['state'] != 'stopped' or not validate_text_input(context):
        return False
    else:
        reset_game(context)
        context.update_printer("Starting game, black to move!")
        set_game_config(context)
        # context.start_timer()


def stop_game(context: GUI):
    # Stop the game

    if game_state['game']['state'] == 'stopped':
        return False
    else:
        game_state['game']['state'] = 'stopped'


def pause_game(context: GUI):
    # Can only pause if game has started
    if game_state['game']['state'] != 'started':
        return False
    else:
        # Set state and reset move timer
        game_state['game']['state'] = 'paused'

        # Reset the move time for AI, search will need to be done again
        if game_state['game']['turn'] == 'black' and game_state['black']['player'] == 'ai':
            game_state['black']['total_time'] -= game_state['black']['move_time']
            game_state['black']['move_time'] = 0

        elif game_state['game']['turn'] == 'white' and game_state['white']['player'] == 'ai':
            game_state['white']['total_time'] -= game_state['white']['move_time']
            game_state['white']['move_time'] = 0

        gui_updater.update_gui(context)


def resume_game(context: GUI):
    # Resuming the game will change the state to 'started'

    if game_state['game']['state'] != 'paused' or game_state['game']['state'] == 'stopped':
        return False
    else:

        game_state['game']['state'] = 'started'
        if game_state['game']['turn'] == 'black' and game_state['black']['player'] == 'ai':
            context.update_printer("Black to move! AI is thinking...")
            ai_main.begin_turn(context, black_piece_id)

        elif game_state['game']['turn'] == 'white' and game_state['white']['player'] == 'ai':
            context.update_printer("White to move! AI is thinking...")
            ai_main.begin_turn(context, white_piece_id)


def reset_game(context: GUI):
    # Reset game state
    game_state['game']['state'] = 'stopped'
    game_state['game']['turn'] = 'black'
    game_state['config']['starting_layout'] = ''
    game_state['config']['time_elapsed'] = 0
    game_state['black']['player'] = ''
    game_state['black']['move_limit'] = 0
    game_state['black']['time_limit'] = 0
    game_state['black']['score'] = 0
    game_state['black']['moves_taken'] = 0
    game_state['black']['move_time'] = 0
    game_state['black']['total_time'] = 0
    game_state['white']['player'] = ''
    game_state['white']['move_limit'] = 0
    game_state['white']['time_limit'] = 0
    game_state['white']['score'] = 0
    game_state['white']['moves_taken'] = 0
    game_state['white']['move_time'] = 0
    game_state['white']['total_time'] = 0

    # Reset GUI and board
    context.selected_pieces.clear()
    set_board_config(context)
    context.set_scoreboard()

    # Clear histories
    move_history_black = [[], []]
    move_history_white = [[], []]
    board_history = []
    gui_updater.update_gui(context)


def undo_move(context: GUI):
    global game_state

    # Can't undo move if game not paused - didn't want to do move timer calculations when we can just reset
    if game_state['game']['state'] == 'paused':
        # Have to pop the board twice because we save the current one right on turn change
        board_history.pop()
        last_board = board_history.pop()
        last_state = state_history.pop()

        # Set to paused so player can gather their thoughts and feelings
        last_state['game']['state'] = 'paused'

        # Subtract the last move time from the total, and then reset the move time
        if last_state['game']['turn'] == 'black':
            last_state['black']['total_time'] -= last_state['black']['move_time']
            # last_state['white']['total_time'] -= game_state['white']['move_time']
        else:
            last_state['white']['total_time'] -= last_state['white']['move_time']
            # last_state['black']['total_time'] -= game_state['black']['move_time']
        last_state['black']['move_time'] = 0.0
        last_state['white']['move_time'] = 0.0

        # Finalize by assigning the previous state, board, and updating gui
        game_state = copy.deepcopy(last_state)
        context.board = copy.deepcopy(last_board)

        context.toggle_player_move()
        gui_updater.update_gui(context)
        context.board.update_board(context.window)

    else:
        return False


def update_turn(context: GUI):
    print(game_state)
    # Check for wins/no time left
    check_goal_state(context)

    save_history(context)
    context.board.update_board(context.window)

    # Calculate the current score after movement, reset the move timers
    context.board.update_scores()
    game_state['black']['move_time'] = 0.0
    game_state['white']['move_time'] = 0.0

    # If black just went
    if game_state['game']['turn'] == 'black':
        game_state['game']['turn'] = 'white'
        context.toggle_player_move()
        update_moves_taken(Turn.BLACK)
        gui_updater.update_gui(context)

        if game_state['white']['player'] == 'ai':
            context.update_printer("White to move! AI is thinking...")
            ai_main.begin_turn(context, white_piece_id)

    # If white just went
    elif game_state['game']['turn'] == 'white':
        game_state['game']['turn'] = 'black'
        context.toggle_player_move()
        update_moves_taken(Turn.WHITE)
        gui_updater.update_gui(context)

        if game_state['black']['player'] == 'ai':
            context.update_printer("Black to move! AI is thinking...")
            gui_updater.update_gui(context)
            ai_main.begin_turn(context, black_piece_id)


def update_moves_taken(piece_enum):
    # Method which will be called after a move is finalized in game_board
    if piece_enum == Turn.WHITE:
        game_state['white']['moves_taken'] += 1
    if piece_enum == Turn.BLACK:
        game_state['black']['moves_taken'] += 1


def check_goal_state(context: GUI):
    # Check for goal states before finalizing a turn
    #    Point win (6 points)
    if game_state['white']['score'] == 6:
        game_state['game']['state'] = 'stopped'
        context.update_printer("White has won by score")
        play_music()

    elif game_state['black']['score'] == 6:
        game_state['game']['state'] = 'stopped'
        context.update_printer("Black has won by score")
        play_music()

    # No moves left on current player
    elif game_state['white']['moves_taken'] == game_state['white']['move_limit']:
        game_state['game']['state'] = 'stopped'
        context.update_printer("Black has won by move limit")
        play_music()

    elif game_state['black']['moves_taken'] == game_state['black']['move_limit']:
        game_state['game']['state'] = 'stopped'
        context.update_printer("White has won by move limit")
        play_music()

    # #    No time left on a player
    # elif game_state['white']['total_time'] >= game_state['white']['time_limit']:
    #     game_state['game']['state'] = 'stopped'
    #     context.update_printer("Black has won by time")
    #     print("MonkaS")
    #     # play_music()
    #
    # elif game_state['black']['total_time'] >= game_state['black']['time_limit']:
    #     game_state['game']['state'] = 'stopped'
    #     context.update_printer("White has won by time")
    #     print("MonkaS")
    #     # play_music()
    #
    # # Gone over the total time limiit
    # elif game_state['black']['total_time'] >= game_state['black']['total_time_limit']:
    #     game_state['game']['state'] = 'stopped'
    #     context.update_printer("White has won by time")
    #     print("MonkaS")
    #     # play_music()
    #
    # elif game_state['white']['total_time'] >= game_state['white']['total_time_limit']:
    #     game_state['game']['state'] = 'stopped'
    #     context.update_printer("Black has won by time")
    #     print("MonkaS")
    #     # play_music()


def play_music():
    pygame.mixer.music.load('../COMP3981_project/Utility/yea.mp3')
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()


def validate_text_input(context: GUI):
    for text_input in context.settings_inputs:
        if not text_input.get_value().isdigit():
            return False
    return True


def set_board_config(context: GUI):
    # Set the board config based on the radio button that has been selected

    for layout in context.layout_radio_choices:
        if not layout.get_value():
            continue
        if layout.get_text() == "Default":
            context.board.build_board(context.window, 'default')
            game_state['config']['starting_layout'] = 'default'

        elif layout.get_text() == "German Daisy":
            context.board.build_board(context.window, 'german_daisy')
            game_state['config']['starting_layout'] = 'german daisy'

        elif layout.get_text() == "Belgian Daisy":
            context.board.build_board(context.window, 'belgian_daisy')
            game_state['config']['starting_layout'] = 'belgian daisy'


def set_game_config(context: GUI):
    # Set the game configs from the GUI

    # Starting layout
    set_board_config(context)

    # Settings for black
    if context.black_human_radio.get_value():
        game_state['black']['player'] = 'human'
    else:
        game_state['black']['player'] = 'ai'
    game_state['black']['move_limit'] = int(context.settings_inputs[0].get_value())
    game_state['black']['time_limit'] = int(context.settings_inputs[1].get_value())
    # game_state['black']['total_time_limit'] = int(context.settings_inputs[4].get_value())
    game_state['black']['total_time_limit'] = 999999999999999999999999999

    # Settings for White
    if context.white_human_radio.get_value():
        game_state['white']['player'] = 'human'
    else:
        game_state['white']['player'] = 'ai'
    game_state['white']['move_limit'] = int(context.settings_inputs[2].get_value())
    game_state['white']['time_limit'] = int(context.settings_inputs[3].get_value())
    # game_state['white']['total_time_limit'] = int(context.settings_inputs[5].get_value())
    game_state['white']['total_time_limit'] = 999999999999999999999999999

    # Set the turn state
    if game_state['black']['player'] == 'human':
        context.update_printer("Black to move!")
        game_state['game']['turn'] = 'black'
        game_state['game']['state'] = 'started'
        save_history(context)
        gui_updater.update_gui(context)

    elif game_state['black']['player'] == 'ai':
        game_state['game']['turn'] = 'black'
        game_state['game']['state'] = 'started'
        gui_updater.update_gui(context)

        context.update_printer("AI is thinking...")
        save_history(context)
        ai_main.begin_turn(context, black_piece_id)

    else:
        save_history(context)


def save_history(context: GUI):
    # Save the current board and game_state
    temp_board = copy.deepcopy(context.board)
    temp_state = copy.deepcopy(game_state)

    board_history.append(temp_board)
    state_history.append(temp_state)


def add_to_move_history(context: GUI, old_coordinates: list, new_coordinates: list):
    """
    Coordinates should come in a String list. Example:
    old_coordinates = ['I5', 'H4']
    new_coordinates = ['G3', 'H4']
    """
    if game_state['game']['turn'] == 'black':
        move_history_black[0].append(old_coordinates)
        move_history_black[1].append(new_coordinates)
        context.update_move_printer(f"Black moved from {old_coordinates} to {new_coordinates}")

    else:
        move_history_white[0].append(old_coordinates)
        move_history_white[1].append(new_coordinates)
        context.update_move_printer(f"White moved from {old_coordinates} to {new_coordinates}")
