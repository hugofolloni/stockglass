from operator import index
import random
import copy
import csv 
from game import Game
class Move():
    def __init__(self, diff, positions):
        self.diff = diff
        self.positions = positions

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
        return 
    choosen = random.choice(moves)
    random_piece_position = (choosen[0], choosen[1])
    random_move = (choosen[2], choosen[3])
    return game.move_pieces(random_piece_position, random_move, player)

def depth_one(player, game):
    if player == 'w':
        enemy = 'b'
    else:
        enemy = 'w'
    moves = game.possible_moves(enemy)
    if len(moves) == 0:
        return
    rates = []
    for item in moves:
        copy_game = copy.deepcopy(game)
        copy_game.move_pieces((item[0], item[1]), (item[2], item[3]), player)
        rates.append(Move(evaluate_game(copy_game.board), item))
    rates.sort(key=lambda x: x.diff, reverse=False)
    best_moves = []
    for item in rates:
        if item.diff == rates[0].diff:
            best_moves.append(item)
    choosen = random.choice(best_moves).positions
    random_piece_position = (choosen[0], choosen[1])
    random_move = (choosen[2], choosen[3])
    return game.move_pieces(random_piece_position, random_move, player)

def min_max(game, main_player, player, depth):
    if player == 'w':
        enemy = 'b'
    else:
        enemy = 'w'
    moves = game.possible_moves(enemy)
    if len(moves) == 0:
        return evaluate_game(game.board)
    if depth == 0:
        return evaluate_game(game.board)
    if main_player == player:
        max_value = -9999
        for item in moves:
            copy_game = copy.deepcopy(game)
            copy_game.move_pieces((item[0], item[1]), (item[2], item[3]), player)
            if evaluate_game(copy_game.board) < 0:
                break
            max_value = max(max_value, min_max(copy_game, main_player, enemy, depth - 1))
        return max_value    
    else:
        min_value = 9999
        for item in moves:
            copy_game = copy.deepcopy(game)
            copy_game.move_pieces((item[0], item[1]), (item[2], item[3]), player)
            if evaluate_game(copy_game.board) > 0:
                break
            min_value = min(min_value, min_max(copy_game, main_player, enemy, depth - 1))
        return min_value
        

def depth_two(player, game):
    if player == 'w':
        enemy = 'b'
    else:
        enemy = 'w'
    moves = game.possible_moves(enemy)
    if len(moves) == 0:
        return
    rates = []
    for item in moves:
        copy_game = copy.deepcopy(game)
        copy_game.move_pieces((item[0], item[1]), (item[2], item[3]), player)
        mean = 0
        number_of_moves = 0
        moves_2 = copy_game.possible_moves(player)
        for item_2 in moves_2:
            copy_game_2 = copy.deepcopy(copy_game)
            copy_game_2.move_pieces((item_2[0], item_2[1]), (item_2[2], item_2[3]), player)
            moves_3 = copy_game_2.possible_moves(enemy)
            for item_3 in moves_3:
                copy_game_3 = copy.deepcopy(copy_game_2)
                copy_game_3.move_pieces((item_3[0], item_3[1]), (item_3[2], item_3[3]), player)
                mean += evaluate_game(copy_game_3.board)
                number_of_moves += 1
        mean /= number_of_moves
        rates.append(Move(mean, item))
    rates.sort(key=lambda x: x.diff, reverse=False)
    best_moves = []
    for item in rates:
        if item.diff == rates[0].diff:
            best_moves.append(item)
        else: 
            break
    choosen = random.choice(best_moves).positions
    random_piece_position = (choosen[0], choosen[1])
    random_move = (choosen[2], choosen[3])
    return game.move_pieces(random_piece_position, random_move, player)
    # for item in moves:
    #     print(min_max(game, player, enemy, 2))

class Opening():
    def __init__(self, name, moves):
        self.name = name
        self.moves = moves

def handle_csv():
    file = open('assets/high_elo_opening.csv', 'r')
    reader = csv.reader(file)
    openings = []
    for row in reader:
        moves = row[10]
        moves = moves.split(',')
        opening = []
        for move in moves:
            if move.find('.') == -1:
                splitted = move.split("'")
                opening.append(splitted[1])     
            else:
                move = move.split('.')[1].split("'")[0]
                opening.append(move)
         
        if len(opening) > 4 and "O-O" not in opening and "O-O-O" not in opening:
            exists = False
            for item in openings:
                if item.moves == opening:
                    exists = True
                    break
            if not exists:
                 openings.append(Opening(row[0], opening))
            
    return openings

def find_opening(moves):
    openings = handle_csv()

    possible_openings = []
    for item in openings:
        matches = False
        max_size = min(len(item.moves), len(moves))
        for idx in range(max_size):
            if moves[idx] == item.moves[idx]:
                matches = True
            else:
                matches = False
                break
        if matches:
            possible_openings.append(item)
        
    return possible_openings


def move(player, game, moves):
    opening = find_opening(moves)
    if len(opening) > 0:
        try:
            choosen = random.choice(opening)
            notation_to_move(game, choosen.moves[len(moves)], player)
            game.opening = choosen.name
            return choosen.moves[len(moves)]
        except:
            return depth_one(player, game)
    else:
        return depth_one(player, game)

def notation_to_move(game, notation, player):
    pieces = ["N", "B", "R", "Q", "K"]
    columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
    lines = ["8", "7", "6", "5", "4", "3", "2", "1"]

    if player == 'w':
        enemy = 'b'
    else:
        enemy = 'w'

    possibles_by_end = []

    notation = ''.join(notation)

    if notation.find("x") == -1 and notation[0] in pieces:
        end = (lines.index(notation[2]), columns.index(notation[1]))
    elif notation.find("x") == -1 and not notation[0] in pieces:
        end = (lines.index(notation[1]), columns.index(notation[0]))
    else:
        end = (lines.index(notation[3]), columns.index(notation[2]))
    possible = game.possible_moves(enemy)
    for item in possible:
        if item[2] == end[0] and item[3] == end[1]:
            possibles_by_end.append(item)
    for item in possibles_by_end:
        if str(game.board[item[0]][item[1]])[1] == 'p' and not notation[0] in pieces:
            return game.move_pieces((item[0], item[1]), (end[0], end[1]), player)
        if str(game.board[item[0]][item[1]])[1].upper() == notation[0]:
            return game.move_pieces((item[0], item[1]), (end[0], end[1]), player)
        

# if __name__ ==  '__main__':
#     # game = Game()
#     # notation_to_move(game, "e4", 'w')
#     # # notation_to_move(game, "Nf5", 'b')
#     # # notation_to_move(game, "cxd3", 'w')
#     # # notation_to_move(game, "Nxd3", 'b')
#     openings = handle_csv()
#     for item in openings:
#         print(item.name, item.moves)