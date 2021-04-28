from pathlib import Path


class FileReader:
    """
    The file reader takes in an input file and generates a tuple (turn, marbles) listing the
    color of marbles to be moved on the current turn and a list of current marble positions.
    """
    @staticmethod
    def load_data(path):
        """
        Gets the data from a valid file path or raises an error if the file is not found.
        """
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError("File path was invalid.")
        with open(path, mode="r", encoding="utf-8") as file:
            data = file.read()
            return data

    @staticmethod
    def read_data(data):
        """
        Returns a tuple with the current marble to move and a list of all marble positions.
        """
        turn = data[0]
        positions = [x.strip() for x in data[2:].split(',')]
        return turn, positions

    @staticmethod
    def write_data(path, data):
        """
        Writes the data passed in to the specified file path from a source array. Used for board states.
        """
        file_path = Path(path)
        with open(file_path, mode="w", encoding="utf-8") as file:
            [file.write(str(line).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '') + '\n')
             for line in data]

    @staticmethod
    def write_moves(path, data):
        """
        Writes the data passed in to the specified file path from a source array. Used for moves.
        """
        file_path = Path(path)
        with open(file_path, mode="w", encoding="utf-8") as file:
            [file.write(str(line) + '\n') for line in data]
