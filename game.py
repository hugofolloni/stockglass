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

    def valid_square(self, start, end, player):
        if player == 'w':
            if str(self.board[start[0]][start[1]])[0] == 'w':
                if self.board[end[0]][end[1]] == ' ' or str(self.board[end[0]][end[1]])[0] == 'b':
                    return True
        elif player == 'b':
            if  str(self.board[start[0]][start[1]])[0] == 'b':
                if self.board[end[0]][end[1]] == ' ' or  str(self.board[end[0]][end[1]])[0] == 'w':
                    return True
        return False

    def valid_move(self, start, end, player):
        piece = str(self.board[start[0]][start[1]])[1]
        return self.valid_square(start, end, player) and (end in self.moves_by_piece(piece, start, player))

    def valid_select(self, line, column, player):
        if str(self.board[line][column])[0] == player:
            return True
        return False

    def highlight_square(self, screen, board, line, column, player):
        highlighted = []
        highlighted.append((line, column))
        possible_moves = []
        start = (line, column)
        for lines in range(8):
            for columns in range(8):
                if self.valid_move(start, (lines, columns), player):
                    possible_moves.append((lines, columns))
        highlighted.append(possible_moves)
        return highlighted

    def move_pieces(self, start, end, player):
        if self.valid_move(start, end, player):
            self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
            self.board[start[0]][start[1]] = ' '
    
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
            return self.all_moves(start)
        elif piece == 'n':
            sums = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
            knight_moves = []
            for sum in sums:
                end = (start[0] + sum[0], start[1] + sum[1])
                if end[0] < 8 and end[0] >= 0 and end[1] < 8 and end[1] >= 0:
                    if self.valid_square(start, end, player):
                        knight_moves.append(end)
            return knight_moves


