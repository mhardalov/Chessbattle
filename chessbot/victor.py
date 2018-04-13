import chess
import random as rnd
import timeit
from math import sqrt, log

from .bot import ChessBot

class ChessBotVictor(ChessBot):
    def __init__(self, name, opt_dict = None):
        super().__init__(name, opt_dict)
        self.depth = opt_dict['depth']
        self.start_board = None
        self.is_white = True

        self.pawns_eval_white = [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]

        self.pawns_eval_black = [i for i in reversed(self.pawns_eval_white)]

        self.knights_eval_white = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ]

        self.knights_eval_black = [i for i in reversed(self.knights_eval_white)]

        self.bishops_eval_white = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20
        ]

        self.bishops_eval_black = [i for i in reversed(self.bishops_eval_white)]

        self.rooks_eval_white = [
             0,  0,  0,  0,  0,  0,  0,  0,
             5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
             0,  0,  0,  5,  5,  0,  0,  0
        ]

        self.rooks_eval_black = [i for i in reversed(self.rooks_eval_white)]

        self.queen_eval_white = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
             -5,  0,  5,  5,  5,  5,  0, -5,
              0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20
        ]
        
        self.queen_eval_black = [i for i in reversed(self.queen_eval_white)]

        self.king_eval_white = [
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
             20, 20,  0,  0,  0,  0, 20, 20,
             20, 30, 10,  0,  0, 10, 30, 20
        ]

        self.king_eval_black = [i for i in reversed(self.king_eval_white)]

        self.king_end_game_eval_white = [
            -50,-40,-30,-20,-20,-30,-40,-50,
            -30,-20,-10,  0,  0,-10,-20,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-30,  0,  0,  0,  0,-30,-30,
            -50,-30,-30,-30,-30,-30,-30,-50
        ]

        self.king_end_game_eval_black = [i for i in reversed(self.king_end_game_eval_white)]

    def is_end_game(self, board):
        n_pawns = len(board.pieces(chess.PAWN, True)) + len(board.pieces(chess.PAWN, False))
        n_knights = len(board.pieces(chess.KNIGHT, True)) + len(board.pieces(chess.KNIGHT, False))
        n_bishops = len(board.pieces(chess.BISHOP, True)) + len(board.pieces(chess.BISHOP, False))
        n_rooks = len(board.pieces(chess.ROOK, True)) + len(board.pieces(chess.ROOK, False))
        n_queens = len(board.pieces(chess.QUEEN, True)) + len(board.pieces(chess.QUEEN, False))
        n_kings = len(board.pieces(chess.KING, True)) + len(board.pieces(chess.KING, False))

        if n_pawns + n_knights + n_bishops + n_rooks + n_queens + n_kings <= 22:
            return True
        else:
            return False

    def calc_heuristic_score(self, board, depth):
        score = 0

        for i in range(8*8):
            piece = board.piece_at(i)
            if not piece:
                continue

            if piece.color == self.is_white:
                if piece.piece_type == chess.PAWN:
                    if self.is_white:
                        score += self.pawns_eval_white[i]
                    else:
                        score += self.pawns_eval_black[i]                    

                elif piece.piece_type == chess.KNIGHT:
                    if self.is_white:
                        score += self.knights_eval_white[i]
                    else:
                        score += self.knights_eval_black[i]                    

                elif piece.piece_type == chess.BISHOP:
                    if self.is_white:
                        score += self.bishops_eval_white[i]
                    else:
                        score += self.bishops_eval_black[i]                    

                elif piece.piece_type == chess.ROOK:
                    if self.is_white:
                        score += self.rooks_eval_white[i]
                    else:
                        score += self.rooks_eval_black[i]                    

                elif piece.piece_type == chess.QUEEN:
                    if self.is_white:
                        score += self.queen_eval_white[i]
                    else:
                        score += self.queen_eval_black[i]                    

                elif piece.piece_type == chess.KING and self.is_end_game(board):
                    if self.is_white:
                        score += self.king_end_game_eval_white[i]
                    else:
                        score += self.king_end_game_eval_black[i]                    

                elif piece.piece_type == chess.KING:
                    if self.is_white:
                        score += self.king_eval_white[i]
                    else:
                        score += self.king_eval_black[i]

                else:
                    pass

            else:
                if piece.piece_type == chess.PAWN:
                    if not self.is_white:
                        score -= self.pawns_eval_white[i]
                    else:
                        score -= self.pawns_eval_black[i]                    

                elif piece.piece_type == chess.KNIGHT:
                    if not self.is_white:
                        score -= self.knights_eval_white[i]
                    else:
                        score -= self.knights_eval_black[i]                    

                elif piece.piece_type == chess.BISHOP:
                    if not self.is_white:
                        score -= self.bishops_eval_white[i]
                    else:
                        score -= self.bishops_eval_black[i]                    

                elif piece.piece_type == chess.ROOK:
                    if not self.is_white:
                        score -= self.rooks_eval_white[i]
                    else:
                        score -= self.rooks_eval_black[i]                    

                elif piece.piece_type == chess.QUEEN:
                    if not self.is_white:
                        score -= self.queen_eval_white[i]
                    else:
                        score -= self.queen_eval_black[i]                    

                elif piece.piece_type == chess.KING and self.is_end_game(board):
                    if not self.is_white:
                        score -= self.king_end_game_eval_white[i]
                    else:
                        score -= self.king_end_game_eval_black[i]                    

                elif piece.piece_type == chess.KING:
                    if not self.is_white:
                        score -= self.king_eval_white[i]
                    else:
                        score -= self.king_eval_black[i]

                else:
                    pass

        # Opponent looses King
        if board.is_checkmate() and (not self.is_white == board.turn):
            score += 9000

        # Bot looses King
        if board.is_checkmate() and (self.is_white == board.turn):
            score += -9000

        # Opponent looses Queen
        if len(self.start_board.pieces(chess.QUEEN, (not self.is_white))) > len(board.pieces(chess.QUEEN, (not self.is_white))):
            score += 900
        
        # Bot looses Queen        
        if len(self.start_board.pieces(chess.QUEEN, self.is_white)) > len(board.pieces(chess.QUEEN, self.is_white)):
            score += -900

        # Opponent looses Rook
        if len(self.start_board.pieces(chess.ROOK, (not self.is_white))) > len(board.pieces(chess.ROOK, (not self.is_white))):
            score += 500
        
        # Bot looses Rook        
        if len(self.start_board.pieces(chess.ROOK, self.is_white)) > len(board.pieces(chess.ROOK, self.is_white)):
            score += -500

        # Opponent looses Bishop      
        if len(self.start_board.pieces(chess.BISHOP, (not self.is_white))) > len(board.pieces(chess.BISHOP, (not self.is_white))):
            score += 300
        
        # Bot looses Bishop        
        if len(self.start_board.pieces(chess.BISHOP, self.is_white)) > len(board.pieces(chess.BISHOP, self.is_white)):
            score += -300
        
        # Opponent looses Knight        
        if len(self.start_board.pieces(chess.KNIGHT, (not self.is_white))) > len(board.pieces(chess.KNIGHT, (not self.is_white))):
            score += 300
        
        # Bot looses Knight        
        if len(self.start_board.pieces(chess.KNIGHT, self.is_white)) > len(board.pieces(chess.KNIGHT, self.is_white)):
            score += -300

        # Opponent looses Pawn    
        if len(self.start_board.pieces(chess.PAWN, (not self.is_white))) > len(board.pieces(chess.PAWN, (not self.is_white))):
            score += 100
        
        # Bot looses Pawn        
        if len(self.start_board.pieces(chess.PAWN, self.is_white)) > len(board.pieces(chess.PAWN, self.is_white)):
            score += -100

        # Makes AI smarter with weighting depth (number of moves)
        score += (depth-1) * 100
        return score

    def minimax(self, board, depth, alpha, beta):
        if depth == 1 or board.is_game_over():
            return self.calc_heuristic_score(board, depth)

        elif board.turn == self.is_white:
            v = -10**6

            for a in self.possible_moves(board):
                board_copy = board.copy()
                board_copy.push(a)

                v = max(v, self.minimax(board_copy, depth-1, alpha, beta))
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

                v = min(v, self.minimax(board_copy, depth-1, alpha, beta))
                beta = min(beta, v)

                if alpha >= beta:
                    # print("prune")                    
                    break

            return v

    def move(self, board):
        self.is_white = board.turn
        self.start_board = board.copy()
        best_score = -10**6
        current_score = 0
        best_move = None

        for move in self.possible_moves(board):
            board_copy = board.copy()
            board_copy.push(move)
            current_score = self.minimax(board_copy, self.depth, -10**6, 10**6)

            if current_score > best_score:
                best_score = current_score
                best_move = move

        return best_move


# # # # # # # # # # # # # # # # # # # # # #
# Chess Bot using Monte Carlo Tree Search #
# # # # # # # # # # # # # # # # # # # # # #

class ChessBotMonteCarlo(ChessBot):
    def __init__(self, name, opt_dict = None):
        super().__init__(name, opt_dict)
        self.n_simulations = opt_dict["n_simulations"]
        self.n_interations = opt_dict["n_iterations"]
        self.is_white = True

    class Node:
        def __init__(self, n_wins, n_simulations, board, parent, children):
            self.n_wins = n_wins
            self.n_simulations = n_simulations
            self.board = board
            self.parent = parent
            self.children = children

        def add_child(self, node):
            node.parent = self
            self.children.append(node)

    def get_uct(self, node, c=2):
        return (node.n_wins / node.n_simulations) + sqrt(c*log(node.parent.n_simulations)/node.n_simulations)

    def pick_best_child(self, root):
        best_uct = -10**6
        current_uct = 0
        best_child = None

        for child in root.children:
            current_uct = self.get_uct(child)
            if current_uct > best_uct:
                best_uct = current_uct
                best_child = child

        return best_child

    def simulate(self, node):
        n_wins = 0
  
        for _ in range(self.n_simulations):
            board_copy = node.board.copy()

            # print("Random Playout start...")
            while board_copy.result() == '*':
                moves = self.possible_moves(board_copy)
                board_copy.push(moves[rnd.randint(0, len(moves)-1)])
            # print("Random Playout ended.")            

            if (board_copy.result() == "1-0" and self.is_white) or (board_copy.result() == "0-1" and not self.is_white):
                n_wins += 1
            else:
                pass

        return self.Node(n_wins, self.n_simulations, node.board.copy(), None, [])

    def backpropagate(self, node):
        for child in node.children:
            node.n_wins += child.n_wins
            node.n_simulations += child.n_simulations

        while node.parent != None:
            node.parent.n_wins += node.n_wins
            node.parent.n_simulations += node.n_simulations

            node = node.parent

        return node

    def monte_carlo_tree_search(self, root):
        for _ in range(self.n_interations):
            # print("Wins: " + str(root.n_wins))
            # print("Simulations: " + str(root.n_simulations))            

            # Selection
            node = root
            while len(node.children) > 0:
                node = self.pick_best_child(node)

            if len(self.possible_moves(node.board)) == 0:
                break

            # Expansion
            expanded_nodes = []
            moves = self.possible_moves(node.board)
            for _ in range(len(moves)//2):
                board_copy = node.board.copy()            
                board_copy.push(moves[rnd.randint(0, len(moves)-1)])
                expanded_nodes.append(self.Node(0, 0, board_copy, None, []))
            
            # Simulation
            for expanded_node in expanded_nodes:
                node.add_child(self.simulate(expanded_node))

            # Backpropagation
            root = self.backpropagate(node)          

        return root

    def move(self, board):
        self.is_white = board.turn
        root = self.monte_carlo_tree_search(self.Node(0, 0, board, None, []))
        
        best_stat = -10^6
        current_state = 0
        best_node = None

        for node in root.children:
            current_state = node.n_wins / node.n_simulations
            if current_state > best_stat:
                best_stat = current_state
                best_node = node

        return best_node.board.pop()
