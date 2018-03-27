import time

import chess
import chess.svg

import numpy as np
import random as rnd

from .bot import ChessBot

from IPython.display import SVG, display, clear_output
from concurrent.futures import ThreadPoolExecutor


class ChessSimulator:
    OUTCOMES = ['White', 'Black', 'Draw']

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

    def simulate(self, rounds=4, timeout=10, turn_sleep_ms=0, display_board_size=450):
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

                self.print_board(SVG(chess.svg.board(board=self.board, size=display_board_size)))
                step += 1
                if (turn_sleep_ms > 0):
                    time.sleep(turn_sleep_ms / 1000)

            last_board = SVG(chess.svg.board(board=self.board, size=display_board_size))
            winner = {'1-0': 0,
                      '0-1': 1,
                      '1/2-1/2': 2}[self.board.result()]
            self.results.append((last_board, winner))
        clear_output(wait=True)
        for (svg, winner) in self.results:
            print('Winner {}'.format(self.OUTCOMES[winner]))
            display(svg)

