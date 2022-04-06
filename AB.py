from lzma import is_check_supported
from string import ascii_lowercase as alphabet

TOTAL = 5
MAX = True
MIN = False
NEG_INF = float('-inf')
POS_INF = float('inf')
WHITE_STRING = "White"
KING_STRING = "King"

MOVE_PIECE_ORDER = ["Queen", "Rook", "Bishop", "Knight", "Pawn", "King"]
VALUABLE_PIECE_ORDER = ["King", "Queen", "Rook", "Bishop", "Knight", "Pawn"]

def find_col(pos):
    return ord(pos[0])

def find_row(pos):
    return pos[1]

def find_position(row, col):
    return (chr(col + ord('a')), row)

'''
Returns True iff pos is inside the gameboard
'''
def is_valid_position(row, col):
    return (row < TOTAL and row >= 0 and col >= 97 and col < 102)

'''
Returns True iff pos can be captured or threatened, not blocked by same color piece
'''
def is_targetable_position(pos: tuple, gameboard: dict, is_black: bool):
    return is_black and gameboard[pos][1] == WHITE_STRING
    

# def is_threatening(pos, board: dict, is_black: bool):
#     if pos not in board:
#         return False
#     else:
#         piece_type, piece_color = board[pos]
#         not_same_color = ((piece_color == "Black") ^ (is_black))
#         if piece_type == "King" and not_same_color:
#             .add(pos)
#         return not_same_color

class Piece:
    white_symbols = {
        "King": "♚",
        "Queen": "♛",
        "Knight": "♞",
        "Bishop": "♝",
        "Rook": "♜",
        "Pawn": "♟"
    }

    black_symbols = {
        "King": "♔",
        "Queen": "♕",
        "Knight": "♘",
        "Bishop": "♗",
        "Rook": "♖",
        "Pawn": "♙"
    }

    score = {
        "King": 100,
        "Queen": 9,
        "Rook": 5,
        "Bishop": 4,
        "Knight": 4,
        "Pawn": 1
    }

    threatened_score = {
        "King": 9,
        "Queen": 4.5,
        "Rook": 3,
        "Bishop": 2,
        "Knight": 2,
        "Pawn": 0.5
    }

    white_pawn_attack_moveset = [(1, 1), (1, -1)]
    black_pawn_attack_moveset = [(-1, 1), (-1, -1)]
    white_pawn_moveset = [(1, 0)]
    black_pawn_moveset = [(-1, 0)]
    king_moveset = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    knight_moveset = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)] 

    def calculate_threat(threat_set: set, board: dict):
        score = 0
        for pos in threat_set:
            piece_type = board[pos][0]
            score += Piece.threatened_score[piece_type]

        return score

    '''
    @param piece_type The String Piece Type
    @param current_pos_desc Current Pawn Position (Pawn)
    @param is_black Boolean if the piece that is attacking is black or not
    
    Calls the appropriate function
    '''
    def assign_threats(piece_type: str, current_pos_desc, gameboard: dict, is_black: bool):
        threatened_places = set()

        if piece_type == "Pawn":
            for pos in current_pos_desc:
                Piece.pawn_threatens(pos, threatened_places, gameboard, is_black)
        if piece_type == "Rook" or piece_type == "Queen":
            Piece.rook_threatens(current_pos_desc, threatened_places, gameboard, is_black)
        if piece_type == "Bishop" or piece_type == "Queen":
            Piece.bishop_threatens(current_pos_desc, threatened_places, gameboard, is_black)
        if piece_type == "Knight":
            Piece.knight_threatens(current_pos_desc, threatened_places, gameboard, is_black)
        if piece_type == "King":
            Piece.king_threatens(current_pos_desc, threatened_places, gameboard, is_black)

        return threatened_places
        
    '''
    @param pos Position of Pawn e.g. ('a', 1)
    Adds places that pawn threatens to threat_set
    '''
    def pawn_threatens(pos: tuple, threat_set: set, gameboard: dict, is_black: bool):
        current_row = find_row(pos)
        current_col = find_col(pos)

        moveset = Piece.black_pawn_attack_moveset if is_black else Piece.white_pawn_attack_moveset
        for move in moveset:
            row = current_row + move[0]
            col = current_col + move[1]
            pos = find_position(row, col)
            if is_valid_position(row, col) and (pos in gameboard) and is_targetable_position(pos, gameboard, is_black):
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
            if is_valid_position(row, col) and (pos in gameboard) and is_targetable_position(pos, gameboard, is_black):
                threat_set.add(pos)
    '''
    @param pos Position of Knight
    returns number of pieces the Knight threatens
    '''
    def knight_threatens(pos: tuple, threat_set: set, gameboard: dict, is_black: bool):
        current_row = find_row(pos)
        current_col = find_col(pos)

        for move in Piece.knight_moveset:
            row = current_row + move[0]
            col = current_col + move[1]
            pos = find_position(row, col)
            if is_valid_position(row, col) and (pos in gameboard) and is_targetable_position(pos, gameboard, is_black):
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

    def is_checkmate(king_pos: tuple, enemy_threats: set):
        # Check King Moveset for intersection with enemy_threats
        current_row = find_row(king_pos)
        current_col = find_col(king_pos)
        threats = 0
        for move in Piece.king_moveset:
            row = current_row + move[0]
            col = current_col + move[1]
            if not is_valid_position(row, col):
                threats += 1 #Cannot escape with this move
            else:
                pos = find_position(row, col)
                if pos in enemy_threats:
                    threats += 1
        return threats == 8

class Game:
    n = TOTAL

    def __init__(self, board):
        self.rows = TOTAL
        self.cols = TOTAL
        self.gameboard = board
        self.king_moves = set()
        self.black_pieces = {"Pawn": []}
        self.white_pieces = {"Pawn": []}
        self.min_threats = set()
        self.max_threats = set()
        self.piece_score = 0
        self.threat_score = 0
        
        for (pos, piece_info) in board.items():
            piece_type = piece_info[0]
            piece_color = piece_info[1]
            if piece_color == WHITE_STRING:
                if piece_type == "Pawn":
                    self.white_pieces[piece_type].append(pos)
                else:
                    self.white_pieces[piece_type] = pos
                self.piece_score += Piece.score[piece_type]
                threat_set = Piece.assign_threats(piece_type, pos, board, False)
                self.threat_score += Piece.calculate_threat(threat_set, board)
                self.max_threats.union(threat_set)

            else:
                if piece_type == "Pawn":
                    self.black_pieces[piece_type].append(pos)
                else:
                    self.black_pieces[piece_type] = pos
                self.piece_score -= Piece.score[piece_type]
                threat_set = Piece.assign_threats(piece_type, pos, board, True)
                self.threat_score -= Piece.calculate_threat(threat_set, board)
                self.min_threats.union(threat_set)

        # self.white_pieces_under_threat = set() # Keep track of how many white pieces are threatened to be taken over
        
        self.is_terminal_game = False
        
        # Check if White King is threatened
        if not KING_STRING in self.white_pieces and not KING_STRING in self.black_pieces:
            self.is_terminal_game = True # Since a King is captured
        elif KING_STRING in self.white_pieces:
            white_king_pos = self.white_pieces[KING_STRING]
            black_king_pos = self.black_pieces[KING_STRING]
            self.is_terminal_game = Piece.is_checkmate(white_king_pos, self.min_threats) or Piece.is_checkmate(black_king_pos, self.max_threats)
    
        # NEED: An O(1) way to tell if White/Black King cannot move to any position because it would be under check - isTerminal
        # NEED: Enumerate all possible white piece moves (Queen then Bishop then Rook then Knight then Pawn then King - since King cannot check another King) and rank moves based on if 
        #       Rank by:
        #       1) The move puts Black King in check
        #       2) The move takes a piece ranked by most valuable piece it can take (King > Queen > Bishop > Rook > Knight > Pawn)
        #       3) The move brings threatens centre pieces (b1 to d3)
        # Observation: Same color pieces act as obstacles for pieces

    #Implement your minimax with alpha-beta pruning algorithm here.
    def ab(self, num_moves_without_capture, depth, alpha, beta, player):
        
        #  if we are at a leaf node, or if MAX/MIN cannot make any more moves
        if depth == 0 or self.is_terminal() or num_moves_without_capture == 50:
            return self.evaluation(num_moves_without_capture) # Evaluation of Leaf Nodes

        elif player is MAX:
            maxEval = NEG_INF
            for move in self.actions(player): # Move Ordering done here
                num_moves_without_capture = self.execute_move(move, num_moves_without_capture)
                eval = self.ab(num_moves_without_capture, depth - 1, alpha, beta, MIN)
                maxEval = max(maxEval, eval)
                alpha = max(maxEval, alpha)
                if beta <= alpha:
                    break

        elif player is MIN:
            minEval = POS_INF
            for move in self.actions(player): # Move Ordering done here
                num_moves_without_capture = self.execute_move(move, num_moves_without_capture)
                eval = self.ab(num_moves_without_capture, depth - 1, alpha, beta, MAX)
                minEval = min(minEval, eval)
                beta = min(minEval, beta)
                if beta <= alpha:
                    break
    
    '''
    Returns True if the State is a Win, Loss or Draw State - No Piece threatening each other
    '''
    def is_terminal(self):
        return self.is_terminal_game or (len(self.max_threats) == 0 and len(self.min_threats) == 0)
    
    def actions(player):
        

    #TODO
    def execute_move(self, move, num_moves_without_capture):
        pass
    
    '''
    Returns 400 for win state, -400 for loss state, 0 for draw state, calculates piece and threats score to decide other states' value
    '''
    def evaluation(self, num_moves):
        if self.is_terminal():
            if KING_STRING in self.black_pieces and Piece.is_checkmate(self.black_pieces[KING_STRING], self.max_threats):
                return 400 # Win State -  Arbitrarily Large Number
            elif KING_STRING in self.black_pieces and Piece.is_checkmate(self.white_pieces[KING_STRING], self.min_threats):
                return -400 # Loss State - Arbitrarily Small Number
        elif num_moves >= 50 and KING_STRING in self.black_pieces and KING_STRING in self.white_pieces:
            return 0 # Draw - Zero Value
        else:
            return self.threat_score + self.piece_score # Calculated Utility for this State               

class State:
    pass


def print_game(gameboard):
    horizontal_line = '-' * gameboard.n * 4
    print("  " + " | ".join(alphabet[:gameboard.n]))
    for i in range(gameboard.rows):
        row_string = str(i) + " "
        for j in range(gameboard.cols):
            next_piece_str = " "
            current_piece = find_position(i, j)
            if current_piece in gameboard.black_positions:
                next_piece_str = Piece.black_symbols[(gameboard.black_positions[current_piece])]
            elif current_piece in gameboard.white_positions:
                next_piece_str = Piece.white_symbols[(gameboard.white_positions[current_piece])]
            row_string += next_piece_str + " | "
        print(row_string)
        print(horizontal_line)

starting_pieces = {
        ("e", 4) : ("King", "Black"),
        ("d", 4): ("Queen", "Black"),
        ("c", 4): ("Bishop", "Black"),
        ("b", 4): ("Knight", "Black"),
        ("a", 4): ("Rook", "Black"),
        ("a", 3): ("Pawn", "Black"),
        ("b", 3): ("Pawn", "Black"),
        ("c", 3): ("Pawn", "Black"),
        ("d", 3): ("Pawn", "Black"),
        ("e", 3): ("Pawn", "Black"),
        ("e", 0) : ("King", "White"),
        ("d", 0): ("Queen", "White"),
        ("c", 0): ("Bishop", "White"),
        ("b", 0): ("Knight", "White"),
        ("a", 0): ("Rook", "White"),
        ("a", 1): ("Pawn", "White"),
        ("b", 1): ("Pawn", "White"),
        ("c", 1): ("Pawn", "White"),
        ("d", 1): ("Pawn", "White"),
        ("e", 1): ("Pawn", "White")
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

    game_board = Game(gameboard)
    print_game(game_board)
    
    move = game_board.ab(0, 4, NEG_INF, POS_INF, MAX)
    return move #Format to be returned (('a', 0), ('b', 3))

studentAgent(starting_pieces)
# Note: Comment when submitting 