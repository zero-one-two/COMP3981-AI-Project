"""
Constants to be used throughout the program.
"""

# Colors
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
black = [0, 0, 0]
white = [255, 255, 255]

# Dimensions
window_width = 1300
window_height = 900

piece_radius = 25
piece_distance = 15

board_width = window_width - 550
board_height = window_height
board_start_x = 20
board_start_y = 30

# Console columns are 225 in length each
# Console starts where board ends
console_width = window_width - board_width
console_height = window_height
console_start_x = board_width
console_start_y = 0
button_length = 180
button_height = 40

printer_start_x = 975
printer_start_y = 450
printer_width = 225
printer_height = 450

# Dynamic text locations on the board using their top left location
black_total_time_location = (180, 675)
black_turn_time_location = (180, 705)
black_score_location = (180, 735)
black_moves_taken_location = (180, 765)

white_total_time_location = (670, 675)
white_turn_time_taken_location = (670, 705)
white_score_location = (670, 735)
white_moves_taken_location = (670, 765)

turn_label_location = (610, 55)

# Misc
num_rows = 9
max_row = 9
white_piece_id = 1
black_piece_id = 2
score_box_size = 150
