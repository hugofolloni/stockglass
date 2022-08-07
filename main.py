import pygame as pg
from game import Game
from board import Board
import player as ia 

class Main():
    def __init__(self):
        board = Board()
        screen = pg.display.set_mode((board.size[0], board.size[1]))
        clock = pg.time.Clock()
        screen.fill(pg.Color(255, 255, 255))
        game = Game()
        board.getting_images()
        running = True
        game_over = False
        player = 'w'
        squares = []
        highlighted = []
        moves = []
        player2 = True
        escape_check_player = 'b'

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print(moves)
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if not game_over:
                        current_location = pg.mouse.get_pos()
                        column = current_location[0] // board.square_size
                        line = current_location[1] // board.square_size
                        if len(squares) == 0:
                            if game.valid_select(line, column, player):
                                squares.append((line, column))
                                highlighted = game.highlight_square(line, column, player)
                        elif len(squares) == 1:
                            if(squares[0][0] == line and squares[0][1] == column):
                                squares = []
                                highlighted = []
                            else:
                                squares.append((line, column))
                                if player == 'w':
                                    escape_check_player = 'b'
                                else:
                                    escape_check_player = 'w'
                                if (squares[0][0], squares[0][1], squares[1][0], squares[1][1]) in game.possible_moves(escape_check_player):
                                    move = game.move_pieces(squares[0], squares[1], player)
                                    moves.append(move)
                                    squares = []
                                    highlighted = []
                                    print(ia.evaluate_game(game.board))

                                    if game.check(player):
                                        if len(game.possible_moves(player)) == 0:
                                            print('Checkmate')
                                            game_over = True
                                        else:
                                            print('Check')
                                    else:
                                        if len(game.possible_moves(player)) == 0:
                                            print('Stalemate')
                                
                                            
                                    if player2:
                                        if player == 'w':
                                            player = 'b'
                                        else:
                                            player = 'w'
                                    else:
                                        move = ia.random_move(game.board, 'b', game) # Worst algorithm ever
                                        moves.append(move)

                                    board.draw_board(screen, highlighted)
                                    board.draw_pieces(screen, game)
                                    pg.display.update()
                                    clock.tick(60)
                                else:
                                    squares = []
                                    highlighted = []
            board.draw_board(screen, highlighted)
            board.draw_pieces(screen, game)
            pg.display.update()
            clock.tick(60)

if __name__ == "__main__":
    Main()
