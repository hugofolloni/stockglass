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
                                squares = []
                                highlighted = []
                            else:
                                squares.append((line, column))
                                if(game.valid_move(squares[0], (line, column), player)):
                                    game.move_pieces(squares[0], squares[1], player)
                                    squares = []
                                    highlighted = []
                                    print(ia.evaluate_game(game.board))

                                    ia.random_move(game.board, 'b', game) # Worst algorithm ever
             
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

#### O QUE FALTA:

## JOGO
# - movimento de peões

# - xeque e xeque-mate
# - stalemate
# - promoção
# - en-passant e roque 

## IA
# - Implementar o algoritmo de busca em profundidade

