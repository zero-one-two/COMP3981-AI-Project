import GUI

"""
A file to hold functions for game movement for AI
NOTE: Co ordinates should be in string format for easy board access ("I5")
NOTE: These moves do not include validation, which should be done prior to calling these functions
"""

out_of_bounds = ['A0', 'A6', 'B0', 'B7', 'C0', 'C8', 'D0', 'D9',
                 'E0', 'E10', 'F1', 'F10', 'G2', 'G10', 'H3', 'H10', 'I4', 'I10',
                 '@0', '@1', '@2', '@3', '@4', '@5', '@6', 'J4', 'J5', 'J6', 'J7',
                 'J8', 'J9', 'J10']


# TODO: Condense these, there's lots of repeated calls.

def move_1_piece(context: GUI, old_coordinate, new_coordinate):
    """
    Move a single piece, no pushes
    Coordinate will come in String of its location (Ex: 'I6')
    """

    old_tile = context.board.board_dict[old_coordinate]
    new_tile = context.board.board_dict[new_coordinate]

    new_tile.piece = old_tile.piece
    old_tile.piece = None

    context.update_move_printer(old_coordinate + " " + new_coordinate)


def move_2_pieces(context: GUI, old_coordinate_1, old_coordinate_2, new_coordinate_1, new_coordinate_2):
    # Coordinate will come in String of its location (Ex: 'I6')

    # The old coordinates should be sorted so that old_coordinate_2 is adjacent to new_coordinate1
    # Ex - Black moving (b2,c3) to (D4,C3)

    old_tile_1 = context.board.board_dict[old_coordinate_1]
    old_tile_2 = context.board.board_dict[old_coordinate_2]
    new_tile_1 = context.board.board_dict[new_coordinate_1]
    new_tile_2 = context.board.board_dict[new_coordinate_2]

    # Store the old pieces
    temp1 = old_tile_1.piece
    temp2 = old_tile_2.piece

    # Empty the old tiles
    old_tile_1.piece = None
    old_tile_2.piece = None

    # Place pieces into new coordinates
    new_tile_1.piece = temp1
    new_tile_2.piece = temp2


def move_3_pieces(context: GUI, old_coordinate_1, old_coordinate_2, old_coordinate_3,
                  new_coordinate_1, new_coordinate_2, new_coordinate_3):
    # Coordinate will come in String of its location (Ex: 'I6')

    old_tile_1 = context.board.board_dict[old_coordinate_1]
    old_tile_2 = context.board.board_dict[old_coordinate_2]
    old_tile_3 = context.board.board_dict[old_coordinate_3]
    new_tile_1 = context.board.board_dict[new_coordinate_1]
    new_tile_2 = context.board.board_dict[new_coordinate_2]
    new_tile_3 = context.board.board_dict[new_coordinate_3]

    # Store old pieces
    temp_1 = old_tile_1.piece
    temp_2 = old_tile_2.piece
    temp_3 = old_tile_3.piece

    # Empty the old tiles
    old_tile_1.piece = None
    old_tile_2.piece = None
    old_tile_3.piece = None

    # Place pieces in the new positions
    new_tile_1.piece = temp_1
    new_tile_2.piece = temp_2
    new_tile_3.piece = temp_3


def sumito_two_to_one(context: GUI, old_coordinates, new_coordinates):
    current_piece = context.board.board_dict[old_coordinates[0]].piece
    for coord in new_coordinates:
        context.board.board_dict[coord].piece = current_piece

    empty_coordinates = [coord for coord in old_coordinates if coord not in new_coordinates]
    for coord in empty_coordinates:
        context.board.board_dict[coord].piece = None


def sumito_three_to_one(context, old_coordinates, new_coordinates):
    """
    Only need to move the piece from the first starting coordinate to the last end coordinate
    """
    # 3-1 Sumito  (F4E3D2 -> E3D2C1) - Push C1 off
    current_piece = context.board.board_dict[old_coordinates[0]].piece
    empty_coordinates = [coord for coord in old_coordinates if coord not in new_coordinates]

    for coord in new_coordinates:
        context.board.board_dict[coord].piece = current_piece

    for coord in empty_coordinates:
        context.board.board_dict[coord].piece = None


def sumito_three_to_two(context: GUI, old_coordinates, new_coordinates, enemy_start_coordinates, enemy_end_coordinates):
    """
    Only need to remove the piece from the first starting coordinate and place it where the last target
    coordinate is going to be
    """
    current_piece = context.board.board_dict[old_coordinates[0]].piece
    enemy_piece = context.board.board_dict[enemy_start_coordinates[0]].piece
    empty_coordinates = [coord for coord in old_coordinates if coord not in new_coordinates]

    for coord in enemy_end_coordinates:
        context.board.board_dict[coord].piece = enemy_piece

    for coord in new_coordinates:
        context.board.board_dict[coord].piece = current_piece

    for coord in empty_coordinates:
        context.board.board_dict[coord].piece = None


def push_two_to_one(context, old_coordinates, new_coordinates, enemy_start_coordinates, enemy_end_coordinates):
    # IE D5D6 - D6D7w

    current_piece = context.board.board_dict[old_coordinates[0]].piece
    enemy_piece = context.board.board_dict[enemy_start_coordinates[0]].piece
    empty_coordinates = [coord for coord in old_coordinates if coord not in new_coordinates]

    for coord in enemy_end_coordinates:
        context.board.board_dict[coord].piece = enemy_piece

    for coord in new_coordinates:
        context.board.board_dict[coord].piece = current_piece

    for coord in empty_coordinates:
        context.board.board_dict[coord].piece = None


def push_three_to_one(context, old_coordinates, new_coordinates, enemy_end_coordinates, enemy_start_coordinates):
    current_piece = context.board.board_dict[old_coordinates[0]].piece
    enemy_piece = context.board.board_dict[enemy_start_coordinates[0]].piece
    empty_coordinates = [coord for coord in old_coordinates if coord not in new_coordinates]

    for coord in enemy_end_coordinates:
        context.board.board_dict[coord].piece = enemy_piece

    for coord in new_coordinates:
        context.board.board_dict[coord].piece = current_piece

    for coord in empty_coordinates:
        context.board.board_dict[coord].piece = None


def push_three_to_two(context, old_coordinates, new_coordinates, enemy_start_coordinates, enemy_end_coordinates):
    # Coordinate will come in String of its location (Ex: 'I6')
    # Ex (C1C2C3 -> C2C3C4) Push (C4C5 -> C5C6)
    current_piece = context.board.board_dict[old_coordinates[0]].piece
    enemy_piece = context.board.board_dict[enemy_start_coordinates[0]].piece
    empty_coordinates = [coord for coord in old_coordinates if coord not in new_coordinates]

    for coord in enemy_end_coordinates:
        context.board.board_dict[coord].piece = enemy_piece

    for coord in new_coordinates:
        context.board.board_dict[coord].piece = current_piece

    for coord in empty_coordinates:
        context.board.board_dict[coord].piece = None
