import numpy as np
import pygame
import sys
import math
import random

ROW_COUNT = 10
COL_COUNT = 9
TO_WIN = 5
BLUE = (0,0,200)
RED = (200,0,0)
YELLOW = (200,200,0)
BLACK = (0,0,0)
GREEN = (0,200,0)

def make_board():
    column = COL_COUNT
    rows = ROW_COUNT
    board = np.zeros((rows,column))
    return board 

board = make_board()
game_over = 0
P1 =0
P2 =1
P1_PIECE = 1
P2_PIECE = 2
turn  = random.randint(0,1)
depth1 = 0

pygame.init()

SQUARE = 50

breadth = COL_COUNT*SQUARE
length = (ROW_COUNT+1)*50
RADIUS= int(SQUARE/2 - 5)

WINDOW_LENGTH = TO_WIN

size = (breadth,length)

screen = pygame.display.set_mode(size)
mfont = pygame.font.SysFont("Aerial",50)

#pygame.display.toggle_fullscreen()
def drop_piece(board,piece,col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            board[r][col] = piece
            break
            
def is_valid(board,col):
    return board[ROW_COUNT-1][col] == 0

def game_win(board,piece):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT-TO_WIN+1):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece and board[r][c+4] ==piece :
                #game_over = True
                return True

    for r in range(TO_WIN-1,ROW_COUNT):
        for c in range(COL_COUNT):
            if board[r][c] == piece and board[r-1][c] == piece and board[r-2][c] == piece and board[r-3][c] == piece and board[r-4][c] ==piece:
                #game_over = True
                return True

    for r in range(ROW_COUNT-TO_WIN+1):
        for c in range(COL_COUNT-TO_WIN+1):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece and board[r+4][c+4] ==piece:
                #game_over = True
                return True

    for r in range(TO_WIN-1,ROW_COUNT):
        for c in range(COL_COUNT-TO_WIN+1):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece and board[r-4][c+4] ==piece:
                #game_over = True  
                return True
    return False

def evaluate(board,window,piece):
    score = 0
    if window.count(piece) == TO_WIN:
        score+=200
    elif window.count(piece) == TO_WIN-1 and window.count(0) == 1:
        score+=100
    elif window.count(piece) == TO_WIN-2 and window.count(0) == 2:
        score+=40
    elif window.count(piece) == TO_WIN-3 and window.count(0) == 3:
        score+=10
    elif window.count(piece) == TO_WIN-4 and window.count(0) == 4:
        score+=2
    
    if window.count(1) == TO_WIN-1 and window.count(0) == 1:
        score -= 200
    
    return score

def score_pos(board,piece):
    score = 1000

    center_arr = [int(i) for i in list(board[:,COL_COUNT//2])]
    center_count = center_arr.count(piece)
    score += center_count*15
    
    for r in range(ROW_COUNT):
        row_arr = [int(i) for i in list(board[r,:])] 
        for c in range(COL_COUNT-TO_WIN+1):
            window = row_arr[c:c+WINDOW_LENGTH]
            score+=evaluate(board,window,piece)
            
    for c in range(COL_COUNT):
        col_arr = [int(i) for i in list(board[:,c])] 
        for r in range(ROW_COUNT-TO_WIN+1):
            window = col_arr[r:r+WINDOW_LENGTH]
            score+=evaluate(board,window,piece)
            
    for r in range(ROW_COUNT-TO_WIN+1):
        for c in range(COL_COUNT-TO_WIN+1):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score+=evaluate(board,window,piece)
            
    for r in range(ROW_COUNT-TO_WIN+1):
        for c in range(COL_COUNT-TO_WIN+1):
            window2 = [board[r+4-i][c+i] for i in range(WINDOW_LENGTH)]
            score+=evaluate(board,window,piece)
            
    return score            

def get_valid_pos(board):
    valid_loc = []
    for col in range(COL_COUNT):
        if is_valid(board,col):
            valid_loc.append(col)
    return valid_loc

def get_best_move(board,piece):
    valid_loc = get_valid_pos(board)
    best_max1 = 0
    best_col = random.choice(valid_loc)
    for col in valid_loc:
        temp_board = board.copy()
        drop_piece(temp_board,piece,col)
        score = score_pos(temp_board,piece)
        if score >best_max1 :
            best_max1 = score
            best_col =  col
        
    return best_col

def is_full(board):
    for c in range(COL_COUNT):
        if board[ROW_COUNT-1][c] == 0 :
            return False
    return True

def isTerminal(board):
    return is_full(board) or game_win(board,1) or game_win(board,2)

def mini_max(board,alpha,beta,depth,maxplayer):
    value = 0
    if depth ==0 or isTerminal(board):
        if isTerminal(board):
            if game_win(board,1) :
                return (None,-100000000)
            elif game_win(board,2):
                return (None,100000000)
            else:
                return (None,0)
        else:
            return (None,score_pos(board,2))
    
    if maxplayer == 1 :
        value = -math.inf
        valid_locs= get_valid_pos(board)
        column = random.choice(get_valid_pos(board))
        for col in valid_locs :
            temp_board = board.copy()
            drop_piece(temp_board,2,col)
            c1,new_score = mini_max(temp_board,alpha,beta,depth-1,0)
            if new_score > value :
                value = new_score
                column = col
            if value > alpha:
                alpha = value
            if alpha >=beta :
                break 
        return column,value
    
    else :
        value = math.inf
        valid_locs = get_valid_pos(board)
        column = random.choice(get_valid_pos(board))
        for col in valid_locs:
            temp_board = board.copy()
            drop_piece(temp_board,1,col)
            c1,new_score = mini_max(temp_board,alpha,beta,depth-1,1)
            if new_score < value:
                value = new_score
                column = col
            if beta> value:
                beta = value
            if alpha >=beta :
                break    
        return column,value

def print_board(board):
    print(np.flip(board,0))

def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,YELLOW,(c*SQUARE , (r+1)*SQUARE, SQUARE, SQUARE ))
            pygame.draw.circle(screen,BLACK,(int(c*SQUARE + SQUARE/2) , int((r+1)*SQUARE+SQUARE/2)), RADIUS)
    
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen,BLUE,(int(c*SQUARE + SQUARE/2) , length - int((r)*SQUARE+SQUARE/2)), RADIUS)    
            elif board[r][c] == 2 :
                pygame.draw.circle(screen,RED,(int(c*SQUARE + SQUARE/2) , length - int((r)*SQUARE+SQUARE/2)), RADIUS)


def find_difficulty(posx,posy):
    if posx>=20 and posx<=140 :
        if posy >=20 and posy<=80:
            return 0
        elif posy>=100 and posy<=160:
            return 2        
        elif posy>=200 and posy<=260:
            return 4
    return -1

flag=0

draw_board(board)

def flip(turn):
    if turn ==0 :
        return 1
    else:
        return 0

while not game_over:
    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit() 
        if e.type == pygame.MOUSEMOTION:            
            pygame.draw.rect(screen,BLACK,(0,0,breadth,SQUARE))
            posx = int(math.floor(e.pos[0]/SQUARE))
            if turn == 0:
                pygame.draw.circle(screen,BLUE,(int(posx*SQUARE + SQUARE/2) ,int(SQUARE/2)), RADIUS)
            else :
                pygame.draw.circle(screen,RED,(int(posx*SQUARE + SQUARE/2) ,int(SQUARE/2)), RADIUS)        
            pygame.display.update()

        if e.type == pygame.MOUSEBUTTONDOWN:
            if turn == 0 :
                col = int(math.floor(e.pos[0]/SQUARE))
                if is_valid(board,col):
                    drop_piece(board,1,col)
                    if game_win(board,1):
                        win = mfont.render("PLAYER1 WINS!! YAY",1, GREEN)
                        screen.blit(win,(10,10))
                        game_over = True
                    draw_board(board)
                else:
                    win = mfont.render("OOPS THIS STACK IS FULL. PLEASE TRY ANOTHER",1,GREEN)
                    screen.blit(win,(10,10))
                    turn = 1
            turn = flip(turn)

    if turn == 1 and not game_over:
        #col = random.randint(0,COL_COUNT-1)
        #col = get_best_move(board,P2_PIECE)
        col,sc = mini_max(board,-math.inf,math.inf,4,1)
        if is_valid(board,col):
            #pygame.time.wait(500)
            drop_piece(board,2,col)
            if game_win(board,2) :
                win = mfont.render("PLAYER2 WINS!! YAY",1, GREEN)
                screen.blit(win,(10,10))    
                game_over = True
            draw_board(board)
                    
        else :
            win = mfont.render("OOPS THIS STACK IS FULL. PLEASE TRY ANOTHER",1,GREEN)
            screen.blit(win,(10,10))
            turn = 0
    
    
        turn = flip(turn)

    draw_board(board)
    pygame.display.update()

    if is_full(board) :
        win = mfont.render("ALL STACKS ARE FULL. THE GAME ENDS IN DRAW",1,GREEN)
        screen.blit(win,(40,10))
        game_over = True
        sys.exit()

    if game_over :
        pygame.time.wait(5000)     
