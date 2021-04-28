import GUI
from operator import itemgetter


def is_valid(context: GUI, vector):
    if is_valid_selection(context) and is_valid_move(context, vector):
        print("Valid")
    else:
        print("Invalid")


def is_valid_selection(context: GUI):
    # Determine if the selected pieces are valid
    if len(context.selected_pieces) > 3 or len(context.selected_pieces) == 0:
        return False

    selected_pieces_sorted_col = sorted(context.selected_pieces, key=itemgetter('column'))
    for tile in selected_pieces_sorted_col:
        print(tile)
        # Determine consistent piece selection
        if tile.piece != context.player_turn.value:
            print("Wrong color")
            return False

    if not is_continuous_row_selection(context) and not is_continuous_diagonal_selection(context):
        print("Non continuous selection")
        return False

    print("Valid Selection")
    return True


def is_continuous_row_selection(context: GUI):
    prev_tile = None
    selected_pieces_sorted_col = sorted(context.selected_pieces, key=itemgetter('column'))

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


def is_continuous_diagonal_selection(context: GUI):
    # print("Starting Diagonal selection consistency Test.")
    prev_tile = None
    selected_pieces_sorted_row = sorted(context.selected_pieces, key=itemgetter('row'))
    horizontal_vector = None  # Keeps track on either up-right or up-left consistency

    # Determine Continuous diagonal selection
    for tile in selected_pieces_sorted_row:

        # Determine continuous row selection
        if prev_tile is not None:
            if horizontal_vector is None:
                # Assign horizontal vector based on first and second evaluation.
                if prev_tile.column + 1 == tile.column:
                    horizontal_vector = 1
                else:
                    horizontal_vector = 0
            if prev_tile.row + 1 == tile.row:  # Row consistency (increasing)
                if horizontal_vector is not None:
                    if prev_tile.column + horizontal_vector != tile.column:
                        # print(f"Inconsistent column selection: c1:{prev_tile.column} c2:{tile.column}")
                        return False
                else:
                    print("Horizontal_vector wasn't assigned. Something went wrong")
            else:
                return False
            prev_tile = tile
        else:
            # After first evaluation, assign some variables
            prev_tile = tile
    return True


def is_valid_move(context: GUI, vector: tuple):
    pass
