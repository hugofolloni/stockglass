import copy


class Game():
    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]
        self.whiteMoves = True
        self.whiteInCheck = False
        self.blackInCheck = False
        self.whiteCastleR = True
        self.whiteCastleL = True
        self.blackCastleR = True
        self.blackCastleL = True
        self.whiteLostCastleR = False
        self.whiteLostCastleL = False
        self.blackLostCastleR = False
        self.blackLostCastleL = False

    def valid_square(self, start, end, player):
        try:
            if player == 'w':
                if str(self.board[start[0]][start[1]])[0] == 'w':
                    if self.board[end[0]][end[1]] == ' ' or str(self.board[end[0]][end[1]])[0] == 'b':
                        return True
            elif player == 'b':
                if  str(self.board[start[0]][start[1]])[0] == 'b':
                    if self.board[end[0]][end[1]] == ' ' or  str(self.board[end[0]][end[1]])[0] == 'w':
                        return True
            return False
        except:
            return False

    def valid_move(self, start, end, player):
        try:
            piece = str(self.board[start[0]][start[1]])[1]
            return self.valid_square(start, end, player) and (end in self.moves_by_piece(piece, start, player))
        except:
            return False

    def valid_select(self, line, column, player):
        if str(self.board[line][column])[0] == player:
            return True
        return False

    def highlight_square(self, line, column, player):
        if player == 'w':
            escape_check_player = 'b'
        else:
            escape_check_player = 'w'
        highlighted = []
        highlighted.append((line, column))
        possible_moves = []
        start = (line, column)
        for move in self.possible_moves(escape_check_player):
            if str(start[0]) == str(move[0]) and str(start[1]) == str(move[1]):
                possible_moves.append((move[2], move[3]))
        highlighted.append(possible_moves)
        return highlighted

    def castling_moves(self):
        return [(0, 4, 0, 6), (0, 4, 0, 2), (7, 4, 7, 6), (7, 4, 7, 2)]


    def move_pieces(self, start, end, player):
        if self.valid_move(start, end, player):
            # if (start[0], start[1], end[0], end[1]) in self.castling_moves():
            #     print('castling')
            # #     self.castling(start, end, player)
            # else:
                took = self.board[end[0]][end[1]] != ' '
                case_pawn_start = None
                if took:
                    case_pawn_start = start[1]
                self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
                if player == 'w':
                    if end[0] == 0 and str(self.board[end[0]][end[1]])[1] == 'p':
                        self.board[end[0]][end[1]] = 'wq'
                else:
                    if end[0] == 7 and str(self.board[end[0]][end[1]])[1] == 'p':
                        self.board[end[0]][end[1]] = 'bq'
                self.board[start[0]][start[1]] = ' '
                # self.can_castle(player)
                return self.chess_notation(case_pawn_start, end, took)
    
    def chess_notation(self, start, end, took):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        numbers = ['8', '7', '6', '5', '4', '3', '2', '1']
        if took:
            modifier = 'x'
        else:
            modifier = ''
        piece = str(self.board[end[0]][end[1]])[1].upper()
        if piece == 'P':
            if took:
                piece = letters[start]
            else:
                piece = ''
        return piece + modifier + letters[end[1]] + numbers[end[0]]

    def inverse_chess_notation(self, notation):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        numbers = ['8', '7', '6', '5', '4', '3', '2', '1']
        if notation[1] == 'x':
            took = True
        else:
            took = False
        if notation[0] == 'P':
            piece = 'p'
        else:
            piece = notation[0]
        return (letters.index(notation[2]), numbers.index(notation[3]), piece, took)

    def linear_moves(self, start):
        right_horizontal_moves = []
        left_horizontal_moves = []
        up_vertical_moves = []
        down_vertical_moves = []
        for line in range(8):
            if line == start[0]:
                for column in range(8):
                    if column == start[1]:
                        continue
                    if column > start[1]:
                        right_horizontal_moves.append((line, column))
                    else:
                        left_horizontal_moves.append((line, column))
        for column in range(8):
            if column == start[1]:
                for line in range(8):
                    if line == start[0]:
                        continue
                    if line > start[0]:
                        up_vertical_moves.append((line, column))
                    else:
                        down_vertical_moves.append((line, column))
        left_horizontal_moves.reverse()
        down_vertical_moves.reverse()
        return [right_horizontal_moves, left_horizontal_moves, up_vertical_moves, down_vertical_moves]

    def diagonal_moves(self, start):
        right_up_moves = []
        left_up_moves = []
        right_down_moves = []
        left_down_moves = []
        size = 8
        start_copy = start
        while(start_copy[0] > 0 and start_copy[1] > 0):
            start_copy = (start_copy[0] - 1, start_copy[1] - 1)
            right_down_moves.append(start_copy)
        start_copy = start
        while(start_copy[0] > 0 and start_copy[1] < size - 1):
            start_copy = (start_copy[0] - 1, start_copy[1] + 1)
            left_down_moves.append(start_copy)
        start_copy = start
        while(start_copy[0] < size - 1 and start_copy[1] > 0): 
            start_copy = (start_copy[0] + 1, start_copy[1] - 1)
            right_up_moves.append(start_copy)
        start_copy = start
        while(start_copy[0] < size - 1 and start_copy[1] < size - 1):
            start_copy = (start_copy[0] + 1, start_copy[1] + 1)
            left_up_moves.append(start_copy)
        return [right_up_moves, left_up_moves, right_down_moves, left_down_moves]
            
                    
    def all_moves(self, start):
        all_moves = []
        for move in self.linear_moves(start):
            all_moves.extend(move)
        for move in self.diagonal_moves(start):
            all_moves.extend(move)
        return all_moves

    def get_blocked_moves(self, list, player):
        allowed_moves = []
        for item in list:
            if self.board[item[0]][item[1]] == ' ':
                    allowed_moves.append(item)
            elif self.board[item[0]][item[1]] == player:
                break
            else:
                allowed_moves.append(item)
                break
        return allowed_moves

    def moves_by_piece(self, piece, start, player):
        if piece == 'p' or piece == 'n':
            return self.special_moves(piece, start, player)
        else:
            linear_moves = self.linear_moves(start)
            right_horizontal_moves = self.get_blocked_moves(linear_moves[0], player)
            left_horizontal_moves = self.get_blocked_moves(linear_moves[1], player)
            up_vertical_moves = self.get_blocked_moves(linear_moves[2], player)
            down_vertical_moves = self.get_blocked_moves(linear_moves[3], player)
            diagonal_moves = self.diagonal_moves(start)
            right_up_moves = self.get_blocked_moves(diagonal_moves[0], player)
            left_up_moves = self.get_blocked_moves(diagonal_moves[1], player)
            right_down_moves = self.get_blocked_moves(diagonal_moves[2], player)
            left_down_moves = self.get_blocked_moves(diagonal_moves[3], player)
            if piece == 'q':
                return right_horizontal_moves + left_horizontal_moves + up_vertical_moves + down_vertical_moves + right_up_moves + left_up_moves + right_down_moves + left_down_moves
            elif piece == 'r':
                return right_horizontal_moves + left_horizontal_moves + up_vertical_moves + down_vertical_moves
            elif piece == 'b':
                return right_down_moves + left_down_moves + right_up_moves + left_up_moves
            elif piece == 'k':
                moves = [right_down_moves, left_down_moves, right_up_moves, left_up_moves, right_horizontal_moves, left_horizontal_moves, up_vertical_moves, down_vertical_moves]
                king_moves = []
                for move in moves:
                    if len(move) > 0:
                        king_moves.append(move[0])
                return king_moves
        
    def special_moves(self, piece, start, player):
        if piece == 'p':
            return self.pawn_moves(start, player)
        elif piece == 'n':
            sums = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
            knight_moves = []
            for sum in sums:
                end = (start[0] + sum[0], start[1] + sum[1])
                if end[0] < 8 and end[0] >= 0 and end[1] < 8 and end[1] >= 0:
                    if self.valid_square(start, end, player):
                        knight_moves.append(end)
            return knight_moves

    def pawn_moves(self, start, player):
        line = start[0]
        column = start[1]
        pawn_move = []
        if player == 'w':
            if line == 6:
                if self.board[line - 2][column] == ' ' and self.board[line - 1][column] == ' ':
                    pawn_move.append((line - 2, column))
            if self.board[line - 1][column] == ' ':
                pawn_move.append((line - 1, column))
            if column + 1 < 8 and str(self.board[line - 1][column + 1])[0] == 'b':
                pawn_move.append((line - 1, column + 1))
            if column - 1 >= 0 and str(self.board[line - 1][column - 1])[0] == 'b':
                pawn_move.append((line - 1, column - 1))
        else:
            if line == 1:
                if self.board[line + 2][column] == ' ' and self.board[line + 1][column] == ' ':
                    pawn_move.append((line + 2, column))
            if self.board[line + 1][column] == ' ':
                pawn_move.append((line + 1, column))
            if column + 1 < 8 and str(self.board[line + 1][column + 1])[0] == 'w':
                pawn_move.append((line + 1, column + 1))
            if column - 1 >= 0 and str(self.board[line + 1][column - 1])[0] == 'w':
                pawn_move.append((line + 1, column - 1))
        return pawn_move

    def check(self, player):
        if player == 'w': 
            king_position = ()
            for line in range(8):
                for column in range(8):
                    if self.board[line][column] == 'bk':
                        king_position = (line, column)
                        break
            for i in range(8):
                for j in range(8):
                    if str(self.board[i][j])[0] == 'w':
                        if self.valid_move((i, j), king_position, player):
                            self.blackInCheck = True
                            return True
            return False
        else:
            king_position = ()
            for line in range(8):
                for column in range(8):
                    if self.board[line][column] == 'wk':
                        king_position = (line, column)
                        break
            for i in range(8):
                for j in range(8):
                    if str(self.board[i][j])[0] == 'b':
                        if self.valid_move((i, j), king_position, player):
                            self.whiteInCheck = True
                            return True
            return False
    
    def possible_moves(self, player):
        moves = []
        to_escape_check = []
        if player == 'w':
            for i in range(8):
                for j in range(8):
                    if str(self.board[i][j])[0] == 'b':
                        for lines in range(8):
                            for columns in range(8):
                                if self.valid_move((i, j), (lines, columns), 'b'):
                                    moves.append((i, j, lines, columns))
            for item in moves:
                can_escape = True
                game = copy.deepcopy(self)
                game.move_pieces((item[0], item[1]), (item[2], item[3]), 'b')
                king_position = ()
                for line in range(8):
                    for column in range(8):
                        if game.board[line][column] == 'bk':
                            king_position = (line, column)
                            break
                for i in range(8):
                    for j in range(8):
                        if str(game.board[i][j])[0] == 'w':
                            if game.valid_move((i, j), king_position, 'w'):
                                can_escape = False
                if can_escape:
                    to_escape_check.append((item[0], item[1], item[2], item[3]))   
            # if self.blackCastleL:
            #     to_escape_check.append((0, 4, 0, 2))
            # if self.blackCastleR:
            #     to_escape_check.append((0, 4, 0, 6))
        else:
            for i in range(8):
                for j in range(8):
                    if str(self.board[i][j])[0] == 'w':
                        for lines in range(8):
                            for columns in range(8):
                                if self.valid_move((i, j), (lines, columns), 'w'):
                                    moves.append((i, j, lines, columns))
            for item in moves:
                can_escape = True
                game = copy.deepcopy(self)
                game.move_pieces((item[0], item[1]), (item[2], item[3]), 'w')
                king_position = ()
                for line in range(8):
                    for column in range(8):
                        if game.board[line][column] == 'wk':
                            king_position = (line, column)
                            break
                for i in range(8):
                    for j in range(8):
                        if str(game.board[i][j])[0] == 'b':
                            if game.valid_move((i, j), king_position, 'b'):
                                can_escape = False
                if can_escape:
                    to_escape_check.append((item[0], item[1], item[2], item[3]))
            # if self.whiteCastleL:
            #     to_escape_check.append((7, 4, 7, 2))
            # if self.whiteCastleR:
            #     to_escape_check.append((7, 4, 7, 6))
        return to_escape_check

    # def can_castle(self, player):
    #     if player == 'w':
    #         if self.board[7][7] != 'wr' and self.board[7][4] != 'wk':
    #             self.whiteLostCastleR = True
    #         if self.board[7][0] != 'wr' and self.board[7][4] != 'wk':
    #             self.whiteLostCastleL = True
    #     else:
    #         if self.board[0][7] != 'br' and self.board[0][4] != 'bk':
    #             self.blackLostCastleR = True
    #         if self.board[0][0] != 'br' and self.board[0][4] != 'bk':
    #             self.blackLostCastleL = True
    #     if player == 'w':
    #         if self.board[7][6] != ' ' or self.board[7][5] != ' ' or self.whiteLostCastleR:
    #             self.whiteCastleR = False
    #         if self.board[7][1] != ' ' or self.board[7][2] != ' ' or self.board[7][3] != ' ' or self.whiteLostCastleL:
    #             self.whiteCastleL = False
    #     else:
    #         if self.board[0][6] != ' ' or self.board[0][5] != ' ' or self.blackLostCastleR:
    #             self.blackCastleR = False
    #         if self.board[0][1] != ' ' or self.board[0][2] != ' ' or self.board[0][3] != ' ' or self.blackLostCastleL:
    #             self.blackCastleL = False
