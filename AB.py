from string import ascii_lowercase as alphabet

TOTAL = 5
MAX = True
MIN = False
NEG_INF = float('-inf')
POS_INF = float('inf')
WHITE_STRING = "White"
KING_STRING = "King"
PAWN_STRING = "Pawn"
QUEEN_STRING = "Queen"
BISHOP_STRING = "Bishop"
ROOK_STRING = "Rook"
KNIGHT_STRING = "Knight"

WEAK_POINTS_ORDER = [ROOK_STRING, BISHOP_STRING, KNIGHT_STRING]
MOVE_PIECE_ORDER = [QUEEN_STRING, ROOK_STRING, BISHOP_STRING, KNIGHT_STRING, PAWN_STRING, KING_STRING]
VALUABLE_PIECE_ORDER = [QUEEN_STRING, ROOK_STRING, BISHOP_STRING, KNIGHT_STRING]

def find_col(pos):
    return ord(pos[0])

def find_row(pos):
    return pos[1]

def find_position(row: int, col: int):
    pos = (chr(col), row)
    return pos

'''
Returns True iff pos is inside the gameboard
'''
def is_valid_position(row: int, col: int):
    return (row < TOTAL and row >= 0 and col >= 97 and col < 102)

'''
Returns True iff pos can be captured or threatened, not blocked by same color piece
'''
def is_targetable_position(pos: tuple, gameboard: dict, is_black: bool):
    return (is_black and gameboard[pos][1] == WHITE_STRING) or (not is_black and gameboard[pos][1] != WHITE_STRING)

class Piece:
    white_symbols = {
        KING_STRING: "♚",
        QUEEN_STRING: "♛",
        KNIGHT_STRING: "♞",
        BISHOP_STRING: "♝",
        ROOK_STRING: "♜",
        PAWN_STRING: "W"#"♟"
    }

    black_symbols = {
        KING_STRING: "♔",
        QUEEN_STRING: "♕",
        KNIGHT_STRING: "♘",
        BISHOP_STRING: "♗",
        ROOK_STRING: "♖",
        PAWN_STRING: "B"
    }

    score = {
        KING_STRING: 150,
        QUEEN_STRING: 9,
        ROOK_STRING: 6,
        BISHOP_STRING: 3,
        KNIGHT_STRING: 4,
        PAWN_STRING: 1
    }

    threatened_score = {
        KING_STRING: 30,
        QUEEN_STRING: 4.5,
        ROOK_STRING: 4,
        BISHOP_STRING: 3,
        KNIGHT_STRING: 3,
        PAWN_STRING: 0.5
    }

    white_pawn_attack_moveset = [(1, 1), (1, -1)]
    black_pawn_attack_moveset = [(-1, 1), (-1, -1)]
    white_pawn_moveset = [(1, 0)]
    black_pawn_moveset = [(-1, 0)]
    king_moveset = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    knight_moveset = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)] 

    def calculate_threat(threat_set: set, board: dict, capture_candidates: set, player: bool):
        score = 0
        for pos in threat_set:
            if pos in board:
                piece_type = board[pos][0]
                score += Piece.threatened_score[piece_type]
                opp_piece_is_white = board[pos][1] == WHITE_STRING
                if (opp_piece_is_white and player is MIN) or (not opp_piece_is_white and player is MAX):
                    # This Piece is being threatened
                    capture_candidates.add(pos)
        return score

    '''
    @param piece_type The String Piece Type
    @param current_pos_desc Current Pawn Position (Pawn)
    @param is_black Boolean if the piece that is attacking is black or not
    
    Calls the appropriate function
    '''
    def assign_threats(piece_type: str, current_pos_desc: tuple, gameboard: dict, is_black: bool):
        threatened_places = set()

        if piece_type == PAWN_STRING:
            Piece.pawn_threatens(current_pos_desc, threatened_places, gameboard, is_black)
        if piece_type == ROOK_STRING or piece_type == QUEEN_STRING:
            Piece.rook_threatens(current_pos_desc, threatened_places, gameboard, is_black)
        if piece_type == BISHOP_STRING or piece_type == QUEEN_STRING:
            Piece.bishop_threatens(current_pos_desc, threatened_places, gameboard, is_black)
        if piece_type == KNIGHT_STRING:
            Piece.knight_threatens(current_pos_desc, threatened_places, gameboard, is_black)
        if piece_type == KING_STRING:
            Piece.king_threatens(current_pos_desc, threatened_places, gameboard, is_black)

        return threatened_places
        
    '''
    @param pos Position of Pawn e.g. ('a', 1)
    @param threat_set Set of positions that are threatened by the pawn, is mutated
    @param gameboard Dictionary of gameboard
    @param is_black Boolean for whether the pawn is black or white
    Adds places that pawn threatens to threat_set
    '''
    def pawn_threatens(pos: tuple, threat_set: set, gameboard: dict, is_black: bool):
        current_row = find_row(pos)
        current_col = find_col(pos)

        # Positions Pawn can capture
        moveset = Piece.black_pawn_attack_moveset if is_black else Piece.white_pawn_attack_moveset
        for move in moveset:
            row = current_row + move[0]
            col = current_col + move[1]
            pos = find_position(row, col)
            if is_valid_position(row, col) and (pos in gameboard and is_targetable_position(pos, gameboard, is_black)):
                threat_set.add(pos)

        # Positions Pawn can move to
        moveset = Piece.black_pawn_moveset if is_black else Piece.white_pawn_moveset
        for move in moveset:
            row = current_row + move[0]
            col = current_col + move[1]
            pos = find_position(row, col)
            if is_valid_position(row, col) and (pos not in gameboard):
                threat_set.add(pos)

    '''
    @param pos Position of King
    returns number of pieces the King threatens
    '''
    def king_threatens(pos: tuple, threat_set: set, gameboard: dict, is_black: bool):
        current_row = find_row(pos)
        current_col = find_col(pos)

        for move in Piece.king_moveset:
            row = current_row + move[0]
            col = current_col + move[1]
            pos = find_position(row, col)
            if is_valid_position(row, col) and (pos not in gameboard or (pos in gameboard and is_targetable_position(pos, gameboard, is_black))):
                threat_set.add(pos)
    '''
    @param pos Position of Knight
    returns number of pieces the Knight threatens
    '''
    def knight_threatens(current_pos: tuple, threat_set: set, gameboard: dict, is_black: bool):
        current_row = find_row(current_pos)
        current_col = find_col(current_pos)

        for move in Piece.knight_moveset:
            row = current_row + move[0]
            col = current_col + move[1]
            pos = find_position(row, col)
            if is_valid_position(row, col) and (pos not in gameboard or (pos in gameboard and is_targetable_position(pos, gameboard, is_black))):
                threat_set.add(pos)

    '''
    @param pos
    returns number of pieces the Bishop threatens
    '''
    def bishop_threatens(pos: tuple, threat_set: set, gameboard: dict, is_black: bool):
        current_row = find_row(pos)
        current_col = find_col(pos)

        min_end = TOTAL
        
        # Left-to-right diagonal from piece
        for i in range(1, min_end):
            row_i = current_row + i
            col_i = current_col + i
            pos = find_position(row_i, col_i)
            if not is_valid_position(row_i, col_i):
                break
            if pos in gameboard:
                if is_targetable_position(pos, gameboard, is_black):
                    threat_set.add(pos)
                break
            else:
                threat_set.add(pos)

        # right-to-left diagonal from piece
        for i in range(1, min_end):
            row_i = current_row - i
            col_i = current_col + i
            pos = find_position(row_i, col_i)
            if not is_valid_position(row_i, col_i):
                break
            if pos in gameboard:
                if is_targetable_position(pos, gameboard, is_black):
                    threat_set.add(pos)
                break
            else:
                threat_set.add(pos)
            
        # Left-to-right diagonal before piece
        for i in range(1, min_end):
            row_i = current_row - i
            col_i = current_col - i
            pos = find_position(row_i, col_i)
            if not is_valid_position(row_i, col_i):
                break
            if pos in gameboard:
                if is_targetable_position(pos, gameboard, is_black):
                    threat_set.add(pos)
                break
            else:
                threat_set.add(pos)
        
        # right-to-left diagonal from piece
        for i in range(1, min_end):
            row_i = current_row + i
            col_i = current_col - i
            pos = find_position(row_i, col_i)
            if not is_valid_position(row_i, col_i):
                break
            if pos in gameboard:
                if is_targetable_position(pos, gameboard, is_black):
                    threat_set.add(pos)
                break
            else:
                threat_set.add(pos)

    '''
    @param pos
    returns moves a Rook can do from pos
    '''
    def rook_threatens(pos: tuple, threat_set: set, gameboard: dict, is_black: bool):
        current_row = find_row(pos)
        current_col = find_col(pos)

        for column in range(current_col + 1, TOTAL):
            #Same row all columns part of Rook's moves
            if not is_valid_position(current_row, column):
                break
            pos = find_position(current_row, column)
            if pos in gameboard:
                if is_targetable_position(pos, gameboard, is_black):
                    threat_set.add(pos)
                break
            else:
                threat_set.add(pos)

        for column in range(current_col - 1, -1, -1):
            #Same row all columns part of Rook's moves
            if not is_valid_position(current_row, column):
                break
            pos = find_position(current_row, column)
            if pos in gameboard:
                if is_targetable_position(pos, gameboard, is_black):
                    threat_set.add(pos)
                break
            else:
                threat_set.add(pos)

        for row in range(current_row + 1, TOTAL):
            #Same column all rows part of Rook's moves
            if not is_valid_position(row, current_col):
                break
            pos = find_position(row, current_col)
            if pos in gameboard:
                if is_targetable_position(pos, gameboard, is_black):
                    threat_set.add(pos)
                break
            else:
                threat_set.add(pos)

        for row in range(current_row - 1, -1, -1):
            #Same column all rows part of Rook's moves
            if not is_valid_position(row, current_col):
                break
            pos = find_position(row, current_col)
            if pos in gameboard:
                if is_targetable_position(pos, gameboard, is_black):
                    threat_set.add(pos)
                break
            else:
                threat_set.add(pos)

    def is_checkmate(king_pos: tuple, enemy_threats: dict):
        # Check King Moveset for intersection with enemy_threats
        current_row = find_row(king_pos)
        current_col = find_col(king_pos)
        king_checkmate = True #Assume True, if its False we'll find out
        
        for move in Piece.king_moveset:
            row = current_row + move[0]
            col = current_col + move[1]
            if not is_valid_position(row, col):
                continue # Cannot escape with this move
            else:
                pos = find_position(row, col)
                if pos not in enemy_threats:
                    king_checkmate = False
                    break
        king_check = king_pos in enemy_threats

        return king_check and king_checkmate
    
    def moves_threatening_king(our_threats: dict, enemy_weak_points: dict, our_pieces: dict, moves_added: set):
        moves = []
        for piece in VALUABLE_PIECE_ORDER:
            if piece not in our_pieces: # We can't do anything anyways
                continue
            # Common points that piece can move to, in order to threaten enemy King
            attacking_points = our_threats.keys() & enemy_weak_points[piece]
            
            for point in attacking_points:
                piece_pos = our_pieces[piece]
                # If this piece's position is inside the set of all positions from which we can move to point from
                if piece_pos in our_threats[point] and (piece_pos, point) not in moves_added:
                    move = (piece_pos, point)
                    moves.append(move)
                    moves_added.add(move)

        return moves

    def moves_attacking_king(king_pos: tuple, our_threats: dict, moves_added: set):
        # Check King Moveset for intersection with enemy_threats
        current_row = find_row(king_pos)
        current_col = find_col(king_pos)
        moves = []

        if king_pos in our_threats:
            # Pick some element from set and add move to capture King
            start_points = our_threats[king_pos]
            for start_pos in start_points:
                move = (start_pos, king_pos)
                if move not in moves_added:
                    moves.append(move)
                    moves_added.add(move)
        
        for move in Piece.king_moveset:
            row = current_row + move[0]
            col = current_col + move[1]
            if not is_valid_position(row, col):
                continue # Cannot escape with this move
            else:
                pos = find_position(row, col)
                if pos in our_threats:
                    start_points = our_threats[pos]
                    for start_pos in start_points:
                        move = (start_pos, pos)
                        if move not in moves_added:
                            moves.append(move)
                            moves_added.add(move)
        return moves

    def moves_attacking_others(capture_candidates: set, enemy_pieces: dict, our_threats: dict, moves_added: set):
        moves = []
        for piece in VALUABLE_PIECE_ORDER:
            # If it's a piece that exists and it is a piece that can be captured
            if piece in enemy_pieces and enemy_pieces[piece] in capture_candidates:
                piece_to_capture_pos = enemy_pieces[piece]
                start_points = our_threats[piece_to_capture_pos]
                for start_pos in start_points:
                    move = (start_pos, piece_to_capture_pos)
                    if move not in moves_added:
                        moves.append(move)
                        moves_added.add(move)
        if PAWN_STRING in enemy_pieces:
            for pos in enemy_pieces[PAWN_STRING]:
                if pos in capture_candidates:
                    start_points = our_threats[pos]
                    for start_pos in start_points:
                        move = (start_pos, pos)
                        if move not in moves_added:
                            moves.append(move)
                            moves_added.add(move)
        return moves

    def all_moves(our_threats: dict, moves_added: set):
        moves = []
        for end_point in our_threats.keys():
            set_of_start_points = our_threats[end_point]
            for start_point in set_of_start_points:
                move = (start_point, end_point)
                if move not in moves_added:
                    moves.append(move)
                    moves_added.add(move)
        return moves

class GameBoard:
    n = TOTAL
    
    def __init__(self, board: dict):
        self.rows = TOTAL
        self.cols = TOTAL
        self.board = board
        self.black_pieces = {PAWN_STRING: []}
        self.white_pieces = {PAWN_STRING: []}
        self.min_threats = {}
        self.max_threats = {}
        self.black_capture_candidates = set()
        self.white_capture_candidates = set()
        self.piece_score = 0
        self.threat_score = 0
        
        for (pos, piece_info) in board.items():
            piece_type = piece_info[0]
            piece_color = piece_info[1]
            if piece_color == WHITE_STRING:
                if piece_type == PAWN_STRING:
                    self.white_pieces[piece_type].append(pos)
                else:
                    self.white_pieces[piece_type] = pos
                self.piece_score += Piece.score[piece_type]
                threat_set = Piece.assign_threats(piece_type, pos, board, False)
                self.threat_score += Piece.calculate_threat(threat_set, board, self.black_capture_candidates, MAX)
                self.update_pieces_with_threats(MAX, threat_set, pos)

            else:
                if piece_type == PAWN_STRING:
                    self.black_pieces[piece_type].append(pos)
                else:
                    self.black_pieces[piece_type] = pos
                self.piece_score -= Piece.score[piece_type]
                threat_set = Piece.assign_threats(piece_type, pos, board, True)
                self.threat_score -= Piece.calculate_threat(threat_set, board, self.white_capture_candidates, MIN)
                self.update_pieces_with_threats(MIN, threat_set, pos)
        
        self.is_terminal_game = False
        
        if not KING_STRING in self.white_pieces or not KING_STRING in self.black_pieces:
            self.is_terminal_game = True # Since a King is captured
    
    '''
    Returns True if the State is a Win, Loss or Draw State - No Piece threatening each other
    '''
    def is_terminal(self, player):
        if self.is_terminal_game:
            return True
        else:
            self.moves = self.actions(player)
            return (len(self.max_threats) == 0) if player is MAX else (len(self.min_threats) == 0) or len(self.moves) == 0
    
    def actions(self, player: bool):
        moves = []
        moves_added = set()

        if player is MAX:
            # Moves that capture King
            moves.extend(Piece.moves_attacking_king(self.black_pieces[KING_STRING], self.max_threats, moves_added))

            # Moves that will capture pieces
            moves.extend(Piece.moves_attacking_others(self.black_capture_candidates, self.black_pieces, self.max_threats, moves_added))
            
            # All other moves that are not in moves_added
            moves.extend(Piece.all_moves(self.max_threats, moves_added))

        else:
            # Moves that capture King
            moves.extend(Piece.moves_attacking_king(self.white_pieces[KING_STRING], self.min_threats, moves_added))

            # Moves that will capture pieces
            moves.extend(Piece.moves_attacking_others(self.white_capture_candidates, self.white_pieces, self.min_threats, moves_added))

            # All other moves that are not in moves_added
            moves.extend(Piece.all_moves(self.min_threats, moves_added))

        return moves

    def execute_move(self, move: tuple, num_moves_without_capture: int, is_min_move: bool):
        start = move[0]
        end = move[1]
        moving_piece_type = self.board[start][0]
        is_capture = end in self.board
        next_board = dict(self.board)
        
        # Update Board
        del next_board[start]
        if is_min_move:
            next_board[end] = (moving_piece_type, "Black")
        else:
            next_board[end] = (moving_piece_type, WHITE_STRING)

        next_gameboard = GameBoard(next_board)
        
        if is_capture:
            return (0, next_gameboard)
        else:
            return (num_moves_without_capture + 1, next_gameboard)
    
    '''
    Returns 400 for win state, -400 for loss state, 0 for draw state, calculates piece and threats score to decide other states' value
    '''
    def evaluation(self, num_moves, player):
        if self.is_terminal(player):
            if KING_STRING in self.black_pieces and Piece.is_checkmate(self.black_pieces[KING_STRING], self.max_threats):
                return 400 # Win State -  Arbitrarily Large Number
            elif KING_STRING in self.white_pieces and Piece.is_checkmate(self.white_pieces[KING_STRING], self.min_threats):
                return -400 # Loss State - Arbitrarily Small Number
            else:    
                final_score =  self.piece_score # Calculated Utility for this State
                return final_score
        elif num_moves >= 50 and KING_STRING in self.black_pieces and KING_STRING in self.white_pieces:
            return 0 # Draw - Zero Value
        else:
            final_score = self.piece_score # Calculated Utility for this State
            return final_score
    
    def update_pieces_with_threats(self, player: bool, threat_set: set, pos: tuple):
        threat_dict = self.max_threats if player is MAX else self.min_threats
        for threatened_pos in threat_set:
            if threatened_pos not in threat_dict:
                threat_dict[threatened_pos] = set()
            threat_dict[threatened_pos].add(pos)

def max_move(gameboard: GameBoard, num_moves_without_capture: int, depth, alpha, beta):
    #  if we are at a leaf node, or if MAX/MIN cannot make any more moves
    if depth == 0 or gameboard.is_terminal(MAX) or num_moves_without_capture == 50:
        eval = gameboard.evaluation(MAX, num_moves_without_capture) # Evaluation of Leaf Nodes
        return eval, None
    
    maxEval = NEG_INF
    best_move = None
    for move in gameboard.moves: # Move Ordering done here
        num_moves_without_capture, next_gameboard = gameboard.execute_move(move, num_moves_without_capture ,False)
        eval, returned_move = min_move(next_gameboard, num_moves_without_capture, depth - 1, alpha, beta)
        if eval > maxEval:
            maxEval = eval
            best_move = move
        alpha = max(maxEval, alpha)
        if beta <= eval:
            return (eval, move)
    return (maxEval, best_move)

def min_move(gameboard: GameBoard, num_moves_without_capture, depth, alpha, beta):
    #  if we are at a leaf node, or if MAX/MIN cannot make any more moves
    if depth == 0 or gameboard.is_terminal(MIN) or num_moves_without_capture == 50:
        eval = gameboard.evaluation(MIN, num_moves_without_capture) # Evaluation of Leaf Nodes
        return eval, None
    
    minEval = POS_INF
    best_move = None
    for move in gameboard.moves: # Move Ordering done here
        num_moves_without_capture, next_gameboard = gameboard.execute_move(move, num_moves_without_capture, True)
        eval, returned_move = max_move(next_gameboard, num_moves_without_capture, depth - 1, alpha, beta)
        if eval < minEval:
            minEval = eval
            best_move = move
        beta = min(minEval, beta)
        if eval <= alpha:
            return (eval, move)
    return (minEval, best_move)
    
#Implement your minimax with alpha-beta pruning algorithm here.
def ab(gameboard: GameBoard):
    best_value, move = max_move(gameboard, 0, 3, NEG_INF, POS_INF)
    return move

starting_pieces = {
        ("e", 4) : (KING_STRING, "Black"),
        ("d", 4): (QUEEN_STRING, "Black"),
        ("c", 4): (BISHOP_STRING, "Black"),
        ("b", 4): (KNIGHT_STRING, "Black"),
        ("a", 4): (ROOK_STRING, "Black"),
        ("a", 3): (PAWN_STRING, "Black"),
        ("b", 3): (PAWN_STRING, "Black"),
        ("c", 3): (PAWN_STRING, "Black"),
        ("d", 3): (PAWN_STRING, "Black"),
        ("e", 3): (PAWN_STRING, "Black"),
        ("e", 0) : (KING_STRING, WHITE_STRING),
        ("d", 0): (QUEEN_STRING, WHITE_STRING),
        ("c", 0): (BISHOP_STRING, WHITE_STRING),
        ("b", 0): (KNIGHT_STRING, WHITE_STRING),
        ("a", 0): (ROOK_STRING, WHITE_STRING),
        ("a", 1): (PAWN_STRING, WHITE_STRING),
        ("b", 1): (PAWN_STRING, WHITE_STRING),
        ("c", 1): (PAWN_STRING, WHITE_STRING),
        ("d", 1): (PAWN_STRING, WHITE_STRING),
        ("e", 1): (PAWN_STRING, WHITE_STRING)
    }

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

# Win: Every position that Black King can move to is threatened, and Black King is threatened or Black King can only move to threatened position (but has available moves - not blocked by its own pieces)
# Loss: Every position that White King can move to is threatened, and White King is threatened or White King can only move to threatened position (but has available moves - not blocked by its own pieces)
# Draw: 50 moves have passed without any captures and both Kings are on the board, or if there are no possible moves to make (e.g. All black/white pieces blocked by black/white pieces)

def studentAgent(gameboard):
    # MAX is always White piece

    game_board = GameBoard(gameboard)
    
    move = ab(game_board)
    return move
