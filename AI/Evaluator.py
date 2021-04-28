"""

"""
from GUI.board import Board
import numpy


class Evaluator:
    # Central positions that provides player most board control.
    prime_positions = ['D3', 'D4', 'D5', 'D6', 'E3', 'E4', 'E5', 'E6', 'E7',
                       'F4', 'F5', 'F6', 'F7']
    # One step in from edge of board, provides knock off potential but has risk.
    good_positions = ['B2', 'B3', 'B4', 'B5', 'C2', 'C3', 'C4', 'C5', 'C6',
                      'D2', 'D7', 'E2', 'E8', 'F3', 'F8', 'G4', 'G5', 'G6',
                      'G7', 'G8', 'H5', 'H6', 'H7', 'H8']
    # Positions at the edge of the board where you can be knocked off.
    danger_positions = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B6', 'C1', 'C7',
                        'D1', 'D8', 'E1', 'E9', 'F2', 'F9', 'G3', 'G9', 'H4',
                        'H9', 'I5', 'I6', 'I7', 'I8', 'I9']

    @staticmethod
    def calculate_player_position_score(marbles: list):
        """
        Calculates the total score based on the positions of the players marbles.
        :param marbles: list
        :return: int
        """
        prime = Evaluator.prime_positions
        good = Evaluator.good_positions
        position_score = 0
        for marble in marbles:
            if marble in prime:
                position_score += 10
            elif marble in good:
                position_score += 5
            else:
                position_score -= 1
        return position_score

    @staticmethod
    def calculate_marble_set_score(black_marbles: list, white_marbles: list):
        """
        Provides a score for each player based on the number of 2 and 3 marble sets that they
        have at their disposal.
        :param black_marbles: list
        :param white_marbles: list
        :return: (black_score, white_score)
        """
        board = Board()
        black_3_marbles = len(board.generate_triple_sets(black_marbles, white_marbles, 'b'))
        white_3_marbles = len(board.generate_triple_sets(black_marbles, white_marbles, 'w'))
        black_2_marbles = len(board.generate_double_sets(black_marbles, white_marbles, 'b'))
        white_2_marbles = len(board.generate_double_sets(black_marbles, white_marbles, 'w'))

        black_score = black_2_marbles * 3 + black_3_marbles * 5
        white_score = white_2_marbles * 3 + white_3_marbles * 5
        return black_score, white_score

    @staticmethod
    def score_move(move_list: list, current_score: int):
        """
        We look at all possible moves that can be made and score each move based on
        how many marbles are pushed and if there are any eliminations.
        :param move_list: list
        :param current_score: int
        :return: int
        """
        multiplier = 1
        # If the player has removed 4 or 5 enemy marbles, the multiplier leans toward elimination
        if current_score > 3:
            multiplier = 5
        for move in move_list:
            move_score = 0
            # Enemy marble eliminated
            if move.get("elim") is True:
                move_score += 100 * multiplier
            # Favors pushing enemy marble over repositioning move
            move_score += move.get("pushes") * 30 * multiplier
            # Favors moving multiple marbles over single
            move_score += len(move.get("start")) * 20
            move["move_score"] = move_score

    @staticmethod
    def assess_risk(black_marbles: list, white_marbles: list):
        """
        Calculates knock off risk for each player on the board.
        :param black_marbles:
        :param white_marbles:
        :return: (black_risk, white_risk)
        """
        danger = Evaluator.danger_positions
        black_risk = 0
        white_risk = 0
        for black_marble in black_marbles:
            letter, num = Board.convert_to_nums(black_marble)
            left = Board.convert_to_string(letter, num - 1)
            right = Board.convert_to_string(letter, num + 1)
            upL = Board.convert_to_string(letter + 1, num)
            upR = Board.convert_to_string(letter + 1, num + 1)
            downL = Board.convert_to_string(letter - 1, num - 1)
            downR = Board.convert_to_string(letter - 1, num)
            test_spots = [left, right, upL, upR, downL, downR]
            if black_marble in danger:
                black_risk += 2
                for spot in test_spots:
                    if spot in white_marbles:
                        black_risk += 5

        for white_marble in white_marbles:
            letter, num = Board.convert_to_nums(white_marble)
            left = Board.convert_to_string(letter, num - 1)
            right = Board.convert_to_string(letter, num + 1)
            upL = Board.convert_to_string(letter + 1, num)
            upR = Board.convert_to_string(letter + 1, num + 1)
            downL = Board.convert_to_string(letter - 1, num - 1)
            downR = Board.convert_to_string(letter - 1, num)
            test_spots = [left, right, upL, upR, downL, downR]
            if white_marble in danger:
                white_risk += 2
                for spot in test_spots:
                    if spot in black_marbles:
                        white_risk += 5
        return black_risk, white_risk

    @staticmethod
    def calculate_board_score(move: dict, board: list, player_turn: chr, current_risk: int):
        """
        Calculates the score of the current board and adds it to the score of the move that generates
        this board to create a total for this move choice.
        :param move: dict
        :param board: list
        :param player_turn: chr
        :param current_risk: int
        """
        black_marbles, white_marbles = Board.read_marbles(board)
        black_pos_score = Evaluator.calculate_player_position_score(black_marbles)
        white_pos_score = Evaluator.calculate_player_position_score(white_marbles)

        black_set_score, white_set_score = Evaluator.calculate_marble_set_score(black_marbles, white_marbles)
        move_score = move.get("move_score")

        black_risk, white_risk = Evaluator.assess_risk(black_marbles, white_marbles)
        black_risk = black_risk - current_risk
        white_risk = white_risk - current_risk

        black_subtotal = black_pos_score + black_set_score - black_risk
        white_subtotal = white_pos_score + white_set_score - white_risk

        if player_turn == 'b':
            move["final_score"] = black_subtotal + move_score
        else:
            move["final_score"] = white_subtotal + move_score

    @staticmethod
    def generate_options(board: list, player_turn: chr):
        """
        Uses the current board state to generate all options and provide each move a score to then
        select the best option.
        :param board: list
        :param player_turn: chr
        :return: list
        """
        black_marbles, white_marbles = Board.read_marbles(board)
        black_risk, white_risk = Evaluator.assess_risk(black_marbles, white_marbles)
        if player_turn == 'b':
            risk = black_risk
        else:
            risk = white_risk

        board_object = Board()
        moves, resulting_boards = board_object.generate_all_boards(board, player_turn)
        # Assume score 0 for now
        Evaluator.score_move(moves, 0)
        for i in range(0, len(moves)):
            Evaluator.calculate_board_score(moves[i], resulting_boards[i], player_turn, risk)
        return moves, resulting_boards

    @staticmethod
    def filter_push(move: dict):
        """
        Function for filter, checks if a move pushes opponent marbles. Used in move ordering
        to first test push moves only as they are likely to yield higher scores.
        :param move: dict
        :return: boolean
        """
        if move.get("pushes") > 0:
            return True
        else:
            return False

    @staticmethod
    def minimax(board: list, player_turn: chr):
        """
        Generates all possible moves for the player and finds the best move the opponent can make
        for each board state. The minimax method then returns the move that leads to the weakest
        board state for the opponent.
        :param board: list
        :param player_turn: chr
        :return: dict
        """
        if player_turn == 'b':
            enemy_turn = 'w'
        else:
            enemy_turn = 'b'
        player_moves, enemy_start_boards = Evaluator.generate_options(board, player_turn)

        player_scores = [x.get("final_score") for x in player_moves]
        enemy_scores = []

        for enemy_start_board in enemy_start_boards:
            board_index = enemy_start_boards.index(enemy_start_board)
            player_score = player_scores[board_index]
            enemy_moves, player_start_boards = Evaluator.generate_options(enemy_start_board, enemy_turn)

            # Gets highest white score for first board.
            if enemy_start_boards.index(enemy_start_board) == 0:
                best_enemy_score = -10000000
                for move in enemy_moves:
                    score = move.get("final_score") - player_score
                    if score > best_enemy_score:
                        best_enemy_score = score
                enemy_scores.append(best_enemy_score)
            else:
                current_min = min(enemy_scores)
                best_enemy_score = -10000000
                break_flag = False

                # Checks moves where active player performs push, more likely to yield high score -> move ordering.
                push_moves = filter(Evaluator.filter_push, enemy_moves)
                for move in push_moves:
                    score = move.get("final_score") - player_score
                    if score > current_min:
                        enemy_scores.append(score)
                        break_flag = True
                        break
                if break_flag:
                    continue

                for move in enemy_moves:
                    if move.get("pushes") > 0:
                        continue
                    score = move.get("final_score") - player_score
                    if score > current_min:
                        enemy_scores.append(score)
                        break_flag = True
                        break
                    if score > best_enemy_score:
                        best_enemy_score = score
                if not break_flag:
                    enemy_scores.append(best_enemy_score)
            # print(enemy_start_board)
            # [print(x) for x in enemy_moves]
            # print("======================")

        # Gets the lowest score aka worst board state for the opponent which will be the best move for us.
        min_val = min(enemy_scores)
        check_scores = numpy.array(enemy_scores)
        min_index = numpy.where(check_scores == min_val)[0]

        best_index = 0
        best_score = -100000

        for i in min_index:
            if player_moves[i].get("final_score") > best_score:
                best_score = player_moves[i].get("final_score")
                best_index = i

        return player_moves[best_index]


if __name__ == '__main__':
    # string_state = "B4b,C3b,C4b,D2b,D7b,E8b,F4b,F9b,G4b,G5b,G8b,H4b,H5b," \
    #                "I5b,A2w,A3w,B2w,B3w,B5w,D3w,G6w,G7w,H8w,I6w,I9w"
    string_state = "A1b,A2b,A3b,A4b,A5b,B1b,B2b,B3b,B4b,B5b,B6b,C3b,C4b,C5b," \
                   "G5w,G6w,G7w,H4w,H5w,H6w,H7w,H8w,H9w,I5w,I6w,I7w,I8w,I9w"
    board_state = [x.strip() for x in string_state[0:].split(',')]
    turn = 'b'
    best_move = Evaluator.minimax(board_state, turn)
    print(best_move)
