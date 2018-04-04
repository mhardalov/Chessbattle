import abc
import numpy as np
import random as rnd

import chess

class ChessBot:
    def __init__(self, name, opt_dict = None):
        self.name = name
        pass

    @abc.abstractmethod
    def move(self, board):
        pass
    
    def possible_moves(self, board):
        moves = list(board.legal_moves)
        rnd.shuffle(moves)
        return moves
    
    def get_name(self):
        return self.__class__.__name__ + ' ' + self.name

    def get_short_name(self):
        return self.name[0:3]

class ChessBotDumb(ChessBot):

    def move(self, board):
        moves = self.possible_moves(board)
        king = board.king(not board.turn)
        weights = np.array([abs(king - move.to_square) for move in moves]) ** 3
        weights = (weights.max() + 1 - weights)
        next_move = moves[np.random.choice(len(moves), 1, p=weights / weights.sum())[0]]
        
        return next_move
    
class ChessBotLessDumb(ChessBot):
    def __init__(self, name, opt_dict = None):
        super().__init__(name, opt_dict)
        self.attack_prob = opt_dict['attack_prob']
    
    def move(self, board):
        moves = self.possible_moves(board)
    
        attacks = [move for move in moves if board.piece_at(move.to_square) is not None]

        if (len(attacks) > 0 and np.random.choice([0,1], 1, p=[ 1 - self.attack_prob, self.attack_prob])[0]):
            weights = np.array([board.piece_at(move.to_square).piece_type
                                for move in moves if board.piece_at(move.to_square) is not None])
            next_move = attacks[np.random.choice(len(attacks), 1, p=weights/weights.sum())[0]]
        else:
            king = board.king(not board.turn)
            weights = np.array([abs(king - move.to_square) for move in moves]) ** 3
            weights = (weights.max() + 1 - weights)
            next_move = moves[np.random.choice(len(moves), 1, p=weights / weights.sum())[0]]

        return next_move

class ChessBotVictor(ChessBot):
    def __init__(self, name, opt_dict = None):
        super().__init__(name, opt_dict)
        self.depth = opt_dict['depth']

    def calc_heuristic_score(self, board, is_white):
        score = 0     

        pawns_table = [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]

        knights_table = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ]

        bishops_table = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20
        ]

        rooks_table = [
             0,  0,  0,  0,  0,  0,  0,  0,
             5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
             0,  0,  0,  5,  5,  0,  0,  0
        ]

        queen_table = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
             -5,  0,  5,  5,  5,  5,  0, -5,
              0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20
        ]

        king_table = [
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
             20, 20,  0,  0,  0,  0, 20, 20,
             20, 30, 10,  0,  0, 10, 30, 20
        ]

        king_end_game_table = [
            -50,-40,-30,-20,-20,-30,-40,-50,
            -30,-20,-10,  0,  0,-10,-20,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-30,  0,  0,  0,  0,-30,-30,
            -50,-30,-30,-30,-30,-30,-30,-50
        ]

        for i in range(8*8):
            piece = board.piece_at(i)
            if not piece:
                continue

            if piece.piece_type == chess.PAWN:
                score += pawns_table[i]

            elif piece.piece_type == chess.KNIGHT:
                score += knights_table[i]

            elif piece.piece_type == chess.BISHOP:
                score += bishops_table[i]

            elif piece.piece_type == chess.ROOK:
                score += rooks_table[i]

            elif piece.piece_type == chess.QUEEN:
                score += queen_table[i]

            elif piece.piece_type == chess.KING and board.fullmove_number > 15:
                score += king_end_game_table[i]

            elif piece.piece_type == chess.KING:
                score += king_table[i]

            else:
                pass

        if not is_white:
            score *= -1

        if board.is_checkmate() and (not is_white == board.turn):
            score += 9000

        if board.is_checkmate() and (is_white == board.turn):
            score -= 9000

        if len(board.pieces(5, is_white)) > len(board.pieces(5, (not is_white))): # Takes Queen
            score += 900
        
        if len(board.pieces(5, is_white)) < len(board.pieces(5, (not is_white))): # Looses Queen
            score += -900

        if len(board.pieces(4, is_white)) > len(board.pieces(4, (not is_white))): # Takes Rook
            score += 500
        
        if len(board.pieces(4, is_white)) < len(board.pieces(4, (not is_white))): # Looses Rook
            score += -500

        if len(board.pieces(3, is_white)) > len(board.pieces(3, (not is_white))): # Takes Bishop
            score += 300
        
        if len(board.pieces(3, is_white)) < len(board.pieces(3, (not is_white))): # Looses Bishop
            score += -300

        if len(board.pieces(2, is_white)) > len(board.pieces(2, (not is_white))): # Takes Knight
            score += 300
        
        if len(board.pieces(2, is_white)) < len(board.pieces(2, (not is_white))): # Looses Knight
            score += -300

        if len(board.pieces(1, is_white)) > len(board.pieces(1, (not is_white))): # Takes Pawn
            score += 100
        
        if len(board.pieces(1, is_white)) < len(board.pieces(1, (not is_white))): # Looses Pawn
            score += -100

        return score

    def minimax(self, board, is_white, depth, alpha, beta):
        if depth == 0 or board.is_checkmate():
            return self.calc_heuristic_score(board, is_white)
        
        elif board.turn == is_white:
            v = -10**6

            for a in self.possible_moves(board):
                board_copy = board.copy()
                board_copy.push(a)

                v = max(v, self.minimax(board_copy, is_white, depth-1, alpha, beta))
                alpha = max(alpha, v)

                if alpha >= beta:
                    # print("prune")
                    break

            return v

        else:
            v = 10**6

            for a in self.possible_moves(board):
                board_copy = board.copy()
                board_copy.push(a)

                v = min(v, self.minimax(board_copy, is_white, depth-1, alpha, beta))
                beta = min(beta, v)

                if alpha >= beta:
                    # print("prune")                    
                    break

            return v

    def move(self, board):
        moves = self.possible_moves(board)
        bestScore = -10**6
        current_score = 0
        bestMove = None

        for move in moves:
            board_copy = board.copy()
            board_copy.push(move)
            current_score = self.minimax(board_copy, board.turn, self.depth, -10**6, 10**6)

            if current_score > bestScore:
                bestScore = current_score
                bestMove = move

        return bestMove
