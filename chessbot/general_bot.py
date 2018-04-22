from .bot import ChessBot

import chess
import random

class SimpleBot(ChessBot):
    def __init__(self, name, scorer, minimaxer, depth, *minimaxer_params):
        super().__init__(name)
        self.scorer = scorer()
        self.minimaxer = minimaxer(self, self.scorer, *minimaxer_params)
        self.depth = depth

    def move(self, board):
        self.scorer.reset_scorings()
        score, move = self.minimaxer.minimax(board, self.depth)
        return move

class AdaptiveBot(ChessBot):
    def __init__(self, name, scorer, minimaxer, initial_depth, scoring_threshold, *minimaxer_params):
        super().__init__(name)
        self.scorer = scorer()
        self.minimaxer = minimaxer(self, self.scorer, *minimaxer_params)
        self.depth = initial_depth
        self.min_depth = initial_depth
        self.scoring_threshold = scoring_threshold

    def move(self, board):
        self.scorer.reset_scorings()
        if board.fullmove_number <= 2:
            self.depth = self.min_depth
        score, move = self.minimaxer.minimax(board, self.depth)
        # can we go deeper?
        if self.scorer.get_scorings() > self.scoring_threshold and self.depth > self.min_depth:
            self.depth -= 1
            print("reducing depth")
        else:
            estimated_scorings = self.scorer.get_scorings() ** ((self.depth + 2) / (self.depth))
            print("esitmated scorings", estimated_scorings)
            if estimated_scorings < self.scoring_threshold:
                print("increasing depth")
                self.depth += 1
        return move

