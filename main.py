import pygame as pg
import time
from game import Game
from board import Board

class Main():
    def __init__(self):
        board = Board()
        screen = pg.display.set_mode((board.size[0], board.size[1]))
        clock = pg.time.Clock()
        screen.fill(pg.Color(255, 255, 255))
        game = Game()
        board.getting_images()
        running = True
        square = ()
        game_over = False
        player = 'w'
        squares = []
        highlighted = []

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if not game_over:
                        current_location = pg.mouse.get_pos()
                        column = current_location[0] // board.square_size
                        line = current_location[1] // board.square_size
                        if len(squares) == 0:
                            if game.valid_select(line, column, player):
                                squares.append((line, column))
                                highlighted = game.highlight_square(screen, board, line, column, player)
                        elif len(squares) == 1:
                            if(squares[0][0] == line and squares[0][1] == column):
                                squares.pop()
                            else:
                                squares.append((line, column))
                                game.move_pieces(squares[0], squares[1], player)
                                squares = []
                                highlighted = []
                                print('lance!!!')
                                if player == 'w':
                                    player = 'b'
                                else:
                                    player = 'w'
                        print(squares)
            board.draw_board(screen, highlighted)
            board.draw_pieces(screen, game)
            pg.display.update()
            clock.tick(60)

if __name__ == "__main__":
    Main()
