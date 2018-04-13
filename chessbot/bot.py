import abc
import numpy as np
import random as rnd

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
