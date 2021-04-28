class Tile:
    """
    Class to represent a tile to be displayed on the board.
    """

    def __init__(self, row, column, board_coordinate, piece):
        """
        Constructor for the tile. Holds a row and column (Ex. 8, 4),
        board coordinate for representation (Ex. "I5"), and a piece. A piece
        is defined in Utility/constants.py:
            white_piece_id = 1
            black_piece_id = 2
            Unoccupied = None
        :param row: int, x coordinate on the board
        :param column: int, y coordinate on the board
        """
        self.row = row
        self.column = column
        self.board_coordinate = board_coordinate
        self.piece = piece
        self.rect = None

    def get_coord(self):
        """
        Gets the tile board coordinate.
        """
        return self.board_coordinate

    def get_piece(self):
        """
        Gets the tile piece data
        """
        return self.piece

    def set_piece(self, piece):
        """
        Sets the tile board piece.
        """
        self.piece = piece

    @staticmethod
    def generate_tile(marble):
        """
        Generates a Tile object based on the marble string passed in.
        "C5b" is converted to a tile possessing the proper characteristics.
        """
        letter = marble[0]
        position = int(marble[1]) - 1
        if marble[2] == 'b':
            color = 2
        else:
            color = 1
        num_letter = ord(letter) - 65
        return Tile(num_letter, position, letter + marble[1], color)

    def set_rect(self, rect):
        """
        Setter for rect.
        When a tile is set by the board, it is given an image Rect object which
        is used to detect mouse clicks.
        :param rect:
        :return:
        """
        self.rect = rect

    def get_rect(self):
        return self.rect

    def __getitem__(self, item):
        if item == 'row':
            return self.row
        elif item == 'column':
            return self.column
        elif item == 'board_coordinate':
            return self.board_coordinate
        else:
            raise KeyError("Invalid item selection")

    def __str__(self):
        return "{0}, {1}, {2}, {3}".format(self.row, self.column, self.board_coordinate, self.piece)
