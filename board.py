import pygame as pg
import time
from game import Game

class Piece():
    def __init__(self, name, image):
        self.name = name
        self.image = image

class Board():

    img = []
    
    def __init__(self):
        pg.init()

        self.white_board = (96,48,48)
        self.black_board = (120,72,56)
        self.colors = [self.white_board, self.black_board]

        self.size = [512, 512]
        self.square_size = 64

    def getting_images(self):
        pieces = ['bp', 'br', 'bn', 'bb', 'bq', 'bk', 'wp', 'wr', 'wn', 'wb', 'wq', 'wk']
        for piece in pieces:
            piece_image = pg.transform.scale(pg.image.load('assets/' + piece + '.png'), (self.square_size, self.square_size))
            self.img.append(Piece(piece, piece_image))

    def draw_board(self, screen, highlighted):
        for lines in range(8):
            for columns in range(8):
                if len(highlighted) > 0:
                    if (lines, columns) == highlighted[0]:
                        color = (217, 108, 80)
                    elif (lines, columns) in highlighted[1]:
                        color = (191, 130, 33)
                    else:
                        color = self.colors[(lines + columns) % 2]
                    pg.draw.rect(screen, color, [columns   * self.square_size, lines * self.square_size, self.square_size, self.square_size])
                else:
                    color = self.colors[(lines + columns) % 2]
                    pg.draw.rect(screen, color, [columns * self.square_size, lines * self.square_size, self.square_size, self.square_size])

    def draw_pieces(self, screen, game):
        for lines in range(8):
            for column in range(8):
                piece = game.board[lines][column]
                if piece != ' ':
                    for piece in self.img:
                        if piece.name == game.board[lines][column]:
                            screen.blit(piece.image, [column * self.square_size, lines * self.square_size])
                            
    def draw_state(self, screen):
        self.draw_board(screen)
        self.draw_pieces(screen, Game.game.board)

    
