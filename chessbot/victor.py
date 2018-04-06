import chess
from .bot import ChessBot

class ChessBotVictor(ChessBot):
    def __init__(self, name, opt_dict = None):
        super().__init__(name, opt_dict)
        self.depth = opt_dict['depth']
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

        if board.is_checkmate() and (not self.is_white == board.turn): # Takes King
            score += 9000

        if board.is_checkmate() and (self.is_white == board.turn): # Looses King
            score += -9000

        if len(board.pieces(chess.QUEEN, self.is_white)) > len(board.pieces(chess.QUEEN, (not self.is_white))): # Takes Queen
            score += 900
        
        if len(board.pieces(chess.QUEEN, self.is_white)) < len(board.pieces(chess.QUEEN, (not self.is_white))): # Looses Queen
            score += -900

        if len(board.pieces(chess.ROOK, self.is_white)) > len(board.pieces(chess.ROOK, (not self.is_white))): # Takes Rook
            score += 500
        
        if len(board.pieces(chess.ROOK, self.is_white)) < len(board.pieces(chess.ROOK, (not self.is_white))): # Looses Rook
            score += -500

        if len(board.pieces(chess.BISHOP, self.is_white)) > len(board.pieces(chess.BISHOP, (not self.is_white))): # Takes Bishop
            score += 300
        
        if len(board.pieces(chess.BISHOP, self.is_white)) < len(board.pieces(chess.BISHOP, (not self.is_white))): # Looses Bishop
            score += -300

        if len(board.pieces(chess.KNIGHT, self.is_white)) > len(board.pieces(chess.KNIGHT, (not self.is_white))): # Takes Knight
            score += 300
        
        if len(board.pieces(chess.KNIGHT, self.is_white)) < len(board.pieces(chess.KNIGHT, (not self.is_white))): # Looses Knight
            score += -300

        if len(board.pieces(chess.PAWN, self.is_white)) > len(board.pieces(chess.PAWN, (not self.is_white))): # Takes Pawn
            score += 100
        
        if len(board.pieces(chess.PAWN, self.is_white)) < len(board.pieces(chess.PAWN, (not self.is_white))): # Looses Pawn
            score += -100

        # Makes AI smarter with weighting depth (number of moves)
        score += (depth-1) * 100
        return score

    def minimax(self, board, depth, alpha, beta):
        if depth == 1 or board.is_checkmate():
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
