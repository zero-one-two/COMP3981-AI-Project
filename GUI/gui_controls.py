import pygame

import GUI
from Models import game_state

"""
This is a collection of callback functions that are used in the GUI. This file functions mostly as a
callback bridge between the GUI buttons and the files that contain functions to carry out the 
desired action.
"""


def start_game_button(context: GUI):
    # game_state.start_game() will only return false if invalid inputs or game state
    if not game_state.start_game(context):
        context.update_printer("State or inputs invalid")
    else:
        context.update_printer(message="Starting game, black to move!")
        game_state.game_state['game']['state'] = 'started'


def stop_game_button(context: GUI):
    if not game_state.stop_game(context):
        context.update_printer("Game is already stopped")
    else:
        context.update_printer("Stopping game")


def pause_game_button(context: GUI):
    if not game_state.pause_game(context):
        context.update_printer("Can't pause game")
    else:
        context.update_printer("Pausing game")


def resume_game_button(context: GUI):
    if not game_state.resume_game(context):
        context.update_printer("Can't resume game")
    else:
        context.update_printer("Resuming game")


def reset_game_button(context: GUI):
    if not game_state.reset_game(context):
        context.update_printer("Can't reset game")
    else:
        context.update_printer("Resetting game")


def undo_move_button(context: GUI):
    if not game_state.undo_move(context):
        context.update_printer("Can't undo move")
    else:
        context.update_printer("Undoing move and pausing game")


def set_board_button(context: GUI):
    game_state.set_board_config(context)


def sheesh(context: GUI, repeat=1):
    # pygame.mixer.music.load('../COMP3981_project/Utility/sheesh.mp3')
    pygame.mixer.music.set_volume(0.5)
    # pygame.mixer.music.play(repeat)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('../COMP3981_project/Utility/sheesh.mp3'))


def stop_music():
    # TODO: Fill in, low priority tho
    pass
    # pygame.mixer.music.stop()
    # pygame.mixer.Channel.stop()
