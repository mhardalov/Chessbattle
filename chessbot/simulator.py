import time

import chess
import chess.svg

import numpy as np
import random as rnd

from .bot import ChessBot

from IPython.display import SVG, display, clear_output
from concurrent.futures import ThreadPoolExecutor


class ChessSimulator:
    DRAW = "Draw"

    def __init__(self, player1, player2, shuffle=True):
        assert issubclass(type(player1), ChessBot)
        assert issubclass(type(player2), ChessBot)

        self.board = chess.Board()

        self.p1 = player1
        self.p2 = player2
        self.results = []

        self.players = [self.p1, self.p2]
        if shuffle: rnd.shuffle(self.players)

    def print_board(self, svg, clear=True):
        if clear: clear_output(wait=True)
        display(svg)

    def simulate(self, rounds=4, timeout=10, turn_sleep_ms=0, verbose_size=450, verbose=True):
        self.results = []
        for r in range(rounds):
            self.board.reset()

            # Even games first player is white
            step = r % 2
            outcomes = [self.players[step].get_name(), self.players[1 - step].get_name(), self.DRAW]

            while (not self.board.is_game_over()):
                player = self.players[step % 2]
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(player.move, self.board.copy())
                    next_move = future.result(timeout=timeout)
                self.board.push(next_move)

                if verbose: self.print_board(SVG(chess.svg.board(board=self.board, size=verbose_size)))
                step += 1
                if (turn_sleep_ms > 0):
                    time.sleep(turn_sleep_ms / 1000)

            last_board = SVG(chess.svg.board(board=self.board, size=verbose_size))
            winner_id = {'1-0': 0, '0-1': 1,'1/2-1/2': 2}[self.board.result()]
            winner = outcomes[winner_id]
            self.results.append((last_board, winner))

        if verbose: clear_output(wait=True)
        summary = {self.p1.get_name(): 0, self.p2.get_name(): 0}
        for (svg, winner) in self.results:
            if verbose: print('Game: {} vs {}. Winner: {}'
                    .format(self.players[0].get_name(), self.players[1].get_name(), winner))
            if winner != self.DRAW: summary[winner] += 1.0
            else:
                summary[self.p1.get_name()] += 0.5
                summary[self.p2.get_name()] += 0.5
            if verbose: display(svg)
        return summary
