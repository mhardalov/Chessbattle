import chess
from chess import SquareSet
from chess import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING

class BoardScorer:
    def __init__(self):
        self.total_scorings = 0

    def reset_scorings(self):
        self.total_scorings = 0

    def get_scorings(self):
        return self.total_scorings

    def scorer(self, board):
        pass

    def score(self, board):
        self.total_scorings += 1
        return self.scorer(board)

class SimpleScorer(BoardScorer):
    def __init__(self):
        super().__init__()

    def scorer(self, board): # WHITE maximizes, BLACK minimizes
        if board.is_game_over():
            return {"1-0": 10000, "1/2-1/2": 0, "0-1": -10000}[board.result()]

        res = 0
        scores = {PAWN:1, KNIGHT:3, BISHOP:3, ROOK:5, QUEEN: 9, KING:0}
        color_factors = {WHITE: 1, BLACK: -1}

        for square in range(64):
           piece = board.piece_at(square)
           if piece: res += scores[piece.piece_type] * color_factors[piece.color]
        
        return res

class ComplexScorer(BoardScorer):
    def __init__(self):
        super().__init__()

    square_scores = [5] * 64
    square_scores[chess.D4] = 10
    square_scores[chess.D5] = 10
    square_scores[chess.E4] = 10
    square_scores[chess.D5] = 10

    def scorer(self, board): # WHITE maximizes, BLACK minimizes
        if board.is_game_over():
            return {"1-0": 100000, "1/2-1/2": 0, "0-1": -100000}[board.result()]

        res = 0
        scores = {PAWN:1, KNIGHT:3, BISHOP:3, ROOK:5, QUEEN:9, KING:10}
        color_factors = {WHITE: 1, BLACK: -1}

        white_territory = 0
        black_territory = 0

        score_board = [[0]*8 for _ in range(8)]
        attackers_count = [[0] * 64 for _ in range(2)]
        weakest_attacker = [[12] * 64 for _ in range(2)]
               
        for square in range(64):
            piece = board.piece_at(square)
            if piece:
                piece_score = scores[piece.piece_type]
                targets = board.attacks(square)
                for target in targets:
                    attackers_count[int(piece.color)][target] += 1
                    if piece_score < weakest_attacker[int(piece.color)][target]:
                        weakest_attacker[int(piece.color)][target] = piece_score

        for square in range(64):
            piece = board.piece_at(square)

            if piece:
                # print(square)
                # print(piece)
                piece_score = 100 * scores[piece.piece_type]
                # print("base", piece_score)
                num_atk = attackers_count[not piece.color][square]
                num_def = attackers_count[piece.color][square]

                # print(num_atk)
                # print(num_def)

                to_move = board.turn == chess.WHITE if piece.color == chess.WHITE \
                    else board.turn == chess.BLACK

                # penalty for attackers
                if num_atk > 0:
                    if num_def > 0: # if there are defenders, penalize for weakest attacker
                        piece_score -= max(0, 50 * (scores[piece.piece_type] - weakest_attacker[not piece.color][square]))
                    else: #penalty if there is any attacker
                        piece_score -= 50 * scores[piece.piece_type]

                # print("after penalty", piece_score)

                #bonux for defenders
                enough_defenders = num_atk - 1 if to_move else num_atk
                # print(enough_defenders)
                if num_def >= enough_defenders: piece_score += 10 * scores[piece.piece_type]

                # print("after_bonus", piece_score)

                score_board[square//8][square%8] = piece_score * color_factors[piece.color]
                res += piece_score * color_factors[piece.color]
            else: # empty square, compute territory bonuses
                square_worth = self.square_scores[square]
                if attackers_count[int(chess.WHITE)][square] > attackers_count[int(chess.BLACK)][square]:
                    res += square_worth
                    score_board[square//8][square%8] = square_worth
                elif attackers_count[int(chess.WHITE)][square] < attackers_count[int(chess.BLACK)][square]:
                    res -= square_worth
                    score_board[square//8][square%8] = -square_worth

        # print(board)
        # for i in range(8):
        #    print(score_board[i])

        return res


