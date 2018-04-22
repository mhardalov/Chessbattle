import chess
from chess import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
import random

class Minimaxer:
    def __init__(self, bot, scorer):
        self.possible_moves = bot.possible_moves
        self.scorer = scorer

    def score(self, board):
        return self.scorer.score(board)

    def minimax(self, board, depth):
        pass

class RegularMinimaxer(Minimaxer):
    def __init__(self, bot, scorer):
        super().__init__(bot, scorer)

    def minimax(self, board, depth):
        # print ("minimax", depth, board.fen())
        # print("heuristic score,", self.score(board))
        if depth == 0 or board.is_game_over():
            return (self.score(board), None)

        if board.turn == WHITE: # maximize:
            best_score = -10000000
            best_move = None

            for move in self.possible_moves(board):
                board.push(move)
                move_score, _ = self.minimax(board, depth - 1)
                board.pop()

                if(move_score > best_score):
                    best_score, best_move = move_score, move

            # print ("depth ", depth, "-> chosen move", best_score, best_move)
            return (best_score, best_move)

        else: # minimize
            best_score = 10000000
            best_move = None

            for move in self.possible_moves(board):
                board.push(move)
                move_score, _ = self.minimax(board, depth - 1)
                board.pop()

                if move_score < best_score:
                    best_score, best_move = move_score, move

            # print ("depth ", depth, "-> chosen move", best_score, best_move)
            return (best_score, best_move)

class PriorityMinimaxer(Minimaxer):
    def __init__(self, bot, scorer, best, random):
        super().__init__(bot, scorer)
        self.best = best
        self.random = random

    def score_potential_move(self, board, move):
        board.push(move)
        res = self.score(board)
        board.pop()
        return res

    def minimax(self, board, depth):
        # print ("minimax", depth)
        if depth == 0 or board.is_game_over():
            # print(self.score(board))
            return (self.score(board), None)


        if board.turn == WHITE: # maximize:
            best_score = -1000000
            best_move = None

            potential_moves = [move for move in self.possible_moves(board)]
            potential_moves.sort(key=lambda move:self.score_potential_move(board, move))
            # print("potential", len(potential_moves))
            
            selected_moves = potential_moves if len(potential_moves) < self.best + self.random else \
                potential_moves[-self.best:] + random.sample(potential_moves[:-self.best], self.random)

            # print("selected", len(selected_moves))

            for move in selected_moves:
                board.push(move)
                move_score, _ = self.minimax(board, depth - 1)
                board.pop()

                if(move_score > best_score):
                    best_score, best_move = move_score, move

            # print ("choice", depth, best_move, best_score)
            return (best_score, best_move)

        else: # minimize
            best_score = 1000000
            best_move = None

            potential_moves = [move for move in self.possible_moves(board)]
            potential_moves.sort(key=lambda move:self.score_potential_move(board, move))
            # print("potential", len(potential_moves))

            selected_moves = potential_moves if len(potential_moves) < self.best + self.random else \
                potential_moves[0:self.best] + random.sample(potential_moves[self.best:], self.random)


            # print(len(selected_moves))

            for move in selected_moves:
                board.push(move)
                move_score, _ = self.minimax(board, depth - 1)
                board.pop()

                if move_score < best_score:
                    best_score, best_move = move_score, move

            # print ("choice", depth, best_move, best_score)
            return (best_score, best_move)

 
