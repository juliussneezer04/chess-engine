import sys
from string import ascii_lowercase as alphabet

# Helper functions to aid in your implementation. Can edit/remove

def find_col(pos):
    return ord(pos[0]) - ord('a')

def find_row(pos):
    return int(pos[1:])

def find_position(row, col):
    return (chr(col + ord('a')), row)

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

    def __init__(self, name, color, pos):
        self.name = name
        self.symbol = Piece.Symbols[self.name]
        self.color = color
        self.pos = pos

class Knight(Piece):
    
    def __init__(self, color, pos):
        super().__init__("Knight", color, pos)
        pass

    def __str__(self):
        return self.symbol
        
class Rook(Piece):
    pass

class Bishop(Piece):
    pass
        
class Queen(Piece):
    pass
        
class King(Piece):
    pass
        
class Pawn(Piece):
    #New Piece to be implemented
    pass

class Game:
    n = 5

    def __init__(self, board):
        self.rows = 5
        self.cols = 5
        black_string = "Black"
        self.black_positions = {k: v[0] for k,v in board.items() if black_string == v[1]}
        self.white_positions = {k: v[0] for k,v in board.items() if black_string != v[1]}

class State:
    pass

#Implement your minimax with alpha-beta pruning algorithm here.
def ab():
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

pieces = {
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

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    game_board = Game(gameboard)
    print_game(game_board)
    move = (None, None)
    return move #Format to be returned (('a', 0), ('b', 3))

studentAgent(pieces)
# Note: Comment when submitting