from string import ascii_lowercase as alphabet

MAX = True
MIN = False
NEG_INF = float('-inf')
POS_INF = float('inf')

def find_col(pos):
    return ord(pos[0])

def find_row(pos):
    return pos[1]

def find_position(row, col):
    return (chr(col + ord('a')), row)

def is_valid_position(row, col):
    return row < 5 and row >= 0 and col >= 97 and col < 102

def is_threatening(row, col, board: dict, is_black: bool, checks: dict):
    pos = find_position(row, col)
    if pos not in board:
        return False
    else:
        piece_type, piece_color = board[pos]
        not_same_color = ((piece_color == "Black") ^ (is_black))
        if piece_type == "King" and not_same_color:
            checks.add(pos)
        return not_same_color

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

    '''
    @param piece_type The String Piece Type
    @param current_pos_desc Current Pawn Position (Pawn)
    
    Calls the appropriate function
    '''
    def assign_threats(piece_type, current_pos_desc, gameboard, is_black):
        
        threatened_places_set = set()
        checks = {}

        if piece_type == "Pawn":
            for pos in current_pos_desc:
                Piece.pawn_threatens(pos, threatened_places_set, checks, gameboard, is_black)
        elif piece_type == "Rook" or piece_type == "Queen":
            Piece.rook_threatens(current_pos_desc, threatened_places_set, checks, gameboard, is_black)
        elif piece_type == "Bishop" or piece_type == "Queen":
            Piece.bishop_threatens(current_pos_desc, threatened_places_set, checks, gameboard, is_black)
        elif piece_type == "Knight":
            Piece.knight_threatens(current_pos_desc, threatened_places_set, checks, gameboard, is_black)
        elif piece_type == "King":
            Piece.king_threatens(current_pos_desc, threatened_places_set, checks, gameboard, is_black)

        return threatened_places_set, checks
        
    '''
    @param pos Position of Pawn e.g. ('a', 1)
    returns number of pieces the Pawn threatens
    '''
    def pawn_threatens(pos: tuple, threat_set: set, checks: dict, gameboard: dict, is_black: bool):
        current_row = find_row(pos)
        current_col = find_col(pos)

        possible_moves = [(1, 1), (1, -1)]
        for move in possible_moves:
            row = current_row + move[0]
            col = current_col + move[1]
            if is_valid_position(row, col) and is_threatening(row, col, gameboard, is_black, checks):
                threat_set.add(find_position(row, col))

    '''
    @param pos Position of King
    returns number of pieces the King threatens
    '''
    def king_threatens(pos: tuple, threat_set: set, checks: dict, gameboard: dict, is_black: bool):
        current_row = find_row(pos)
        current_col = find_col(pos)

        possible_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for move in possible_moves:
            row = current_row + move[0]
            col = current_col + move[1]
            if is_valid_position(row, col) and is_threatening(row, col, gameboard, is_black, checks):
                threat_set.add(find_position(row, col))

    '''
    @param pos Position of Knight
    returns number of pieces the Knight threatens
    '''
    def knight_threatens(pos: tuple, threat_set: set, checks: dict, gameboard: dict, is_black: bool):
        current_row = find_row(pos)
        current_col = find_col(pos)

        possible_moves = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for move in possible_moves:
            row = current_row + move[0]
            col = current_col + move[1]
            if is_valid_position(row, col) and is_threatening(row, col, gameboard, is_black, checks):
                threat_set.add(find_position(row, col))

    '''
    @param pos
    returns number of pieces the Bishop threatens
    '''
    def bishop_threatens(pos: tuple, threat_set: set, checks: dict, gameboard: dict, is_black: bool):
        current_row = find_row(pos)
        current_col = find_col(pos)

        min_end = 5
        
        # Left-to-right diagonal from piece
        for i in range(1, min_end):
            row_i = current_row + i
            col_i = current_col + i
            if not is_valid_position(row_i, col_i):
                break
            elif is_threatening(row_i, col_i):
                    t += 1

        # right-to-left diagonal from piece
        for i in range(1, min_end):
            row_i = current_row - i
            col_i = current_col + i
            if not is_valid_position(row_i, col_i):
                break
            elif is_threatening(row_i, col_i):
                    t += 1
            
        # Left-to-right diagonal before piece
        for i in range(1, min_end):
            row_i = current_row - i
            col_i = current_col - i
            if not is_valid_position(row_i, col_i):
                break
            elif is_threatening(row_i, col_i):
                    t += 1
        
        # right-to-left diagonal from piece
        for i in range(1, min_end):
            row_i = current_row + i
            col_i = current_col - i
            if not is_valid_position(row_i, col_i):
                break
            elif is_threatening(row_i, col_i):
                    t += 1

        return t

    '''
    @param pos
    returns moves a Rook can do from pos
    '''
    def rook_threatens(pos):
        t = 0
        current_row = find_row(pos)
        current_col = find_col(pos)

        for column in range(current_col + 1, Board.total):
            #Same row all columns part of Rook's moves
            if not is_valid_position(current_row, column):
                break
            elif is_threatening(current_row, column):
                t += 1

        for column in range(current_col - 1, -1, -1):
            #Same row all columns part of Rook's moves
            if not is_valid_position(current_row, column):
                break
            elif is_threatening(current_row, column):
                t += 1

        for row in range(current_row + 1, Board.total):
            #Same column all rows part of Rook's moves
            if not is_valid_position(row, current_col):
                break
            elif is_threatening(row, current_col):
                t += 1

        for row in range(current_row - 1, -1, -1):
            #Same column all rows part of Rook's moves
            if not is_valid_position(row, current_col):
                break
            elif is_threatening(row, current_col):
                t += 1

        return t

class Game:
    n = 5

    def __init__(self, board):
        self.rows = 5
        self.cols = 5
        black_string = "Black"
        self.gameboard = board
        self.black_pieces = {"Pawn": []}
        self.white_pieces = {"Pawn": []}
        
        for (pos, piece_info) in board.items():
            piece_type = piece_info[0]
            piece_color = piece_info[1]
            if piece_color == black_string:
                if piece_type == "Pawn":
                    self.black_pieces[piece_type].append(pos)
                else:
                    self.black_pieces[piece_type] = pos
            else:
                if piece_type == "Pawn":
                    self.white_pieces[piece_type].append(pos)
                else:
                    self.white_pieces[piece_type] = pos

        # NEED: An O(1) way to tell if White/Black King cannot move to any position because it would be under check - isTerminal
        # NEED: Enumerate all possible white piece moves (Queen then Bishop then Rook then Knight then Pawn then King - since King cannot check another King) and rank moves based on if 
        #       Rank by:
        #       1) The move puts Black King in check
        #       2) The move takes a piece ranked by most valuable piece it can take (King > Queen > Bishop > Rook > Knight > Pawn)
        #       3) The move brings threatens centre pieces (b1 to d3)
        # Observation: Same color pieces act as obstacles for pieces
        
        self.black_piece_threats = {}
        self.white_piece_threats = {}
        for piece_type, pos in self.black_pieces.items():
            threatened_positions, checks = Piece.assign_threats(piece_type, pos, board, True)
            self.black_piece_threats[piece_type] = threatened_positions

        for piece_type, pos in self.white_pieces.items():
            threatened_positions, checks = Piece.assign_threats(piece_type, pos, board, False)
            self.white_piece_threats[piece_type] = threatened_positions

    #Implement your minimax with alpha-beta pruning algorithm here.
    def ab(self, num_moves_without_capture, depth, alpha, beta, player):
        
        # Checks if we are at a leaf node, or if MAX/MIN cannot make any more moves
        if depth == 0 or self.is_terminal() or num_moves_without_capture == 50:
            return self.evaluation(alpha, beta) # Evaluation of Leaf Nodes

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
    Returns True if the State is a Win, Loss or Draw State
    '''
    def is_terminal(self):
        # If King is under checkmate or threatened on all sides, Win for opposing side
        # If no piece is threatening any other piece, draw
        pass

    #TODO
    def actions(player):
        pass

    #TODO
    def execute_move(self, move, num_moves_without_capture):
        pass
    
    #TODO
    def evaluation(self, alpha, beta):
        pass

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