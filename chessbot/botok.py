from chessbot.bot import ChessBot

import chess
from chess import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING

class ChessBotOK(ChessBot):
    def __init__(self, name, opt_dict = None):
        super().__init__(name, opt_dict)
        self.depth = opt_dict['depth']

    def score(self, board): # WHITE maximizes, BLACK minimizes
        if board.is_game_over():
            return {"1-0": 10000, "1/2-1/2": 0, "0-1": -10000}[board.result()]

        res = 0
        scores = {PAWN:1, KNIGHT:3, BISHOP:3, ROOK:5, QUEEN: 9, KING:0}
        color_factors = {WHITE: 1, BLACK: -1}

        for square in range(64):
            piece = board.piece_at(square)
            if piece: res += scores[piece.piece_type] * color_factors[piece.color]

        return res

    def minimax(self, board, depth):
        if depth == 0 or board.is_game_over():
            return (self.score(board), None)

        if board.turn == WHITE: # maximize:
            best_score = -100000
            best_move = None

            for move in self.possible_moves(board):
                board.push(move)
                move_score, _ = self.minimax(board, depth - 1)
                board.pop()

                if(move_score > best_score):
                    best_scpre, best_move = move_score, move

            return (best_score, best_move)

        else: # minimize
            best_score = 100000
            best_move = None

            for move in self.possible_moves(board):
                board.push(move)
                move_score, _ = self.minimax(board, depth - 1)
                board.pop()

                if move_score < best_score:
                    best_score, best_move = move_score, move

            return (best_score, best_move)

    def move(self, board):
        score, move = self.minimax(board, self.depth)
        return move

