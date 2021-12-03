import pygame as p
import pandas as pd
import chess



df = pd.read_csv('chess_games.csv')
moves = 'd4 d6 c4 g6 Nc3 Bg7 e4 Nc6 Be3 Nf6 Nge2 O-O h3 e5 d5 Ne7 Ng3 Ne8 f4 f5 exf5 Nxf5 Nxf5 Bxf5 fxe5 Bxe5 Be2 Qh4+ Bf2 Bg3 Bxg3 Qxg3+ Kd2 Nf6 Qe1 Qf4+ Kd1 Rae8 Qd2 Qxd2+ Kxd2 Ne4+ Nxe4 Rxe4 Rhe1 Rfe8 g4 Bd7 Bd3 Rd4 Rxe8+ Bxe8 Ke3 Rxd3+ Kxd3 c6 Re1 Kf7 Rb1 cxd5 cxd5 Kf6 Kd4 Kg5 Re1 Bf7 Re3 h6 Rc3 Kh4 a3 a6 b4 b5 Re3 Bg8 Ke4 g5 Kf5 Bh7+ Ke6 Bg6 Kxd6 Be4 Ke5 Bxd5 Kxd5 h5 gxh5 Kxh5 Kc6 a5 Kxb5 axb4 Kxb4'
#YuPwYPd7

def get_game():
    board_ = chess.Board()
    boards = [board_.fen()]
    for i in moves.split(' '):
        board_.push_san(i)
        boards.append(board_.fen())
    return boards



    
    
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
Fen_Chess = {'P':'wp','R':'wR','N':'wN','B':'wB','K':'wK','Q':'wQ','p':'bp','r':'bR','b':'bB','q':'bQ','k':'bK','n':'bN'}

def loadImages():
    pieces = ['wp','wR','wN','wB','wK','wQ','bp','bR','bB','bQ','bK','bN']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'),(SQ_SIZE,SQ_SIZE))   


def main():
    p.init()
    screen = p.display.set_mode((WIDTH , HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    loadImages()
    move_ordre = 0
    boards = get_game()

    runing = True
    board=boards[0]
    drawGameState(screen , board)
    while runing:
        for e in p.event.get():
            if e.type == p.QUIT:
                runing = False
            if e.type == p.KEYDOWN:
                if e.key == p.K_RIGHT:
                    if move_ordre < len(boards) -1:
                        move_ordre += 1
                        board=boards[move_ordre]
                if e.key == p.K_LEFT :
                    if move_ordre > 0:
                        move_ordre -= 1
                        board=boards[move_ordre]
        drawGameState(screen , board)
        clock.tick(MAX_FPS)
        p.display.flip()






def drawGameState(screen , board):
    drawBoard(screen)
    drawPieces(screen, fen_to_normal(board))

    
def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def fen_to_normal(board):
    Board=[[0]*DIMENSION for i in range(DIMENSION)]
    board=board.split(' ')[0].split('/')
    for i in range(DIMENSION):
        if len(board[i]) < 8:
            new=''
            for c in board[i]:
                if c in '12345678':
                    new+=int(c)*'1'
                else :
                    new+=c
            board[i] = new
        else:
            continue
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if board[row][col] == '1':
                Board[row][col]='--'
            else:
                Board[row][col]= Fen_Chess[board[row][col]]
    return Board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
                




if __name__ == '__main__' :
    main()
                        


