import _thread
import pygame
from GUI import gui_updater
import GUI
from Models import game_state


def run_timer(context: GUI):
    while True:
        pygame.time.delay(200)

        if game_state.game_state['game']['state'] == 'started':
            if game_state.game_state['game']['turn'] == 'black':
                game_state.game_state['black']['move_time'] += 0.2
                game_state.game_state['black']['total_time'] += 0.2

            elif game_state.game_state['game']['turn'] == 'white':
                game_state.game_state['white']['move_time'] += 0.2
                game_state.game_state['white']['total_time'] += 0.2

            gui_updater.update_gui_turn_time(context)
            gui_updater.update_gui_total_time(context)


def start_state_timer(context: GUI):
    _thread.start_new_thread(run_timer, (context, ))
