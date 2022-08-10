import random

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

def random_move(player, game):
    if player == 'w':
        enemy = 'b'
    else:
        enemy = 'w'
    moves = game.possible_moves(enemy)
    if len(moves) == 0:
        return print('No possible moves')
    choosen = random.choice(moves)
    random_piece_position = (choosen[0], choosen[1])
    random_move = (choosen[2], choosen[3])
    return game.move_pieces(random_piece_position, random_move, player)