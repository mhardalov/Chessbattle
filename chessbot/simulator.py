import time

import chess
import chess.svg

import numpy as np
import random as rnd

from .bot import ChessBot

from IPython.display import SVG, display, clear_output
from concurrent.futures import ThreadPoolExecutor


class ChessSimulator:
    OUTCOMES = ['White', 'Black', 'Pat']

    def __init__(self, player1, player2):
        assert issubclass(type(player1), ChessBot)
        assert issubclass(type(player2), ChessBot)

        self.board = chess.Board()

        self.p1 = player1
        self.p2 = player2
        self.results = []

        self.players = [self.p1, self.p2]
        rnd.shuffle(self.players)

    def print_board(self, svg, clear=False):
        clear_output(wait=True)
        display(svg)

    def simulate(self, rounds=3, timeout=10, turn_sleep_ms=0):
        self.results = []
        for r in range(rounds):
            self.board.reset()

            # Even games first player is white
            step = r % 2

            while (not self.board.is_game_over()):
                player = self.players[step % 2]
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(player.move, self.board.copy())
                    next_move = future.result(timeout=timeout)
                self.board.push(next_move)

                self.print_board(SVG(chess.svg.board(board=self.board)))
                step += 1
                if (turn_sleep_ms > 0):
                    time.sleep(turn_sleep_ms / 1000)

            last_board = SVG(chess.svg.board(board=self.board))
            winner = self.result(self.board)
            self.results.append((last_board, winner))
        clear_output(wait=True)
        for (svg, winner) in self.results:
            print('Winner {}'.format(self.OUTCOMES[winner]))
            display(svg)

    def result(self, board):
        if (len(list(board.legal_moves)) > 0):
            return 2
        else:
            return int(board.turn)
