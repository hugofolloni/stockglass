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

    def valid_move(self, start, end, player):
        if player == 'w':
            if str(self.board[start[0]][start[1]])[0] == 'w':
                if self.board[end[0]][end[1]] == ' ' or str(self.board[end[0]][end[1]])[0] == 'b':
                    return True
        elif player == 'b':
            if  str(self.board[start[0]][start[1]])[0] == 'b':
                if self.board[end[0]][end[1]] == ' ' or  str(self.board[end[0]][end[1]])[0] == 'w':
                    return True
        return False

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
            if self.valid_move(start, end, player):
                self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
                self.board[start[0]][start[1]] = ' '
   

