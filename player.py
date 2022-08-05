import random

class Piece():
    def __init__(self, piece, player, position):
        self.piece = piece
        self.player = player
        self.position = position

def piece_value(piece):
    if piece == 'p':
        return 1
    elif piece == 'r':
        return 5
    elif piece == 'n':
        return 3
    elif piece == 'b':
        return 3
    elif piece == 'q':
        return 9
    elif piece == 'k':
        return 200
    else:
        return 0

def evaluate_game(board):
    white_points = 0
    black_points = 0
    for lines in range(8):
        for columns in range(8):
            position = board[lines][columns]
            if str(position)[0] == 'w':
                white_points += piece_value(str(position)[1])
            elif str(position)[0] == 'b':
                black_points += piece_value(str(position)[1])
    return white_points - black_points

def random_move(board, player, game):
    pieces = []
    for lines in range(8):
        for columns in range(8):
            if str(board[lines][columns])[0] == player:
                pieces.append(Piece(str(board[lines][columns])[1], player, (lines, columns)))
    number_of_random_movies = 0
    while number_of_random_movies == 0:
        random_piece = random.choice(pieces)
        valid_moves = []
        for line in range(8):
            for column in range(8):
                if game.valid_move(random_piece.position, (line, column), random_piece.player):
                    valid_moves.append((line, column))
        number_of_random_movies = len(valid_moves)
    random_move = random.choice(valid_moves)
    return game.move_pieces(random_piece.position, random_move, random_piece.player)