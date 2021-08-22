import sdl2.ext
import Graphics
import Board

from random import randint
from math import inf

# functions controlling player and AI input

class Input:
  
  def __init__(self):
    self.mouse_x = 0
    self.mouse_y = 0
    self.correctMove_X = 0
    self.correctMove_Y = 0
    self.make_move = 0

g_Input = Input()

def mouse_processor(board):
    
    events = sdl2.ext.get_events()
    Graphics.window.refresh()
    
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            quit()
        
        # when left mouse button is clicked, send coordinates to check if an X can be added on the board
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            g_Input.mouse_x = event.motion.x
            g_Input.mouse_y = event.motion.y
            if event.button.button == sdl2.SDL_BUTTON_LEFT:   
                check_cursor(g_Input.mouse_x, g_Input.mouse_y)
            if event.button.button == sdl2.SDL_BUTTON_RIGHT:   
                cheater(board)
    
def check_cursor(mouse_x, mouse_y):
    
    global player_col
    global player_row
    
    while True: 
        if int(mouse_x) >= 104 and int(mouse_x) <= 245:
            player_col = 0
            g_Input.correctMove_X = 1
        elif int(mouse_x) >= 249 and int(mouse_x) <= 390:
            player_col = 1
            g_Input.correctMove_X = 1
        elif int(mouse_x) >= 394 and int(mouse_x) <= 535:
            player_col = 2
            g_Input.correctMove_X = 1
        else:
            print ("Clicked outside of the play area (X).")
            break
            
        if int(mouse_y) >= 24 and int(mouse_y) <= 165:
            player_row = 0
            g_Input.correctMove_Y = 1
        elif int(mouse_y) >= 169 and int(mouse_y) <= 310:
            player_row = 1
            g_Input.correctMove_Y = 1
        elif int(mouse_y) >= 314 and int(mouse_y) <= 455:
            player_row = 2
            g_Input.correctMove_Y = 1
        else:
            print ("Clicked outside of the play area (Y).")
            break
        
        if g_Input.correctMove_X == 1 and g_Input.correctMove_Y == 1:
            g_Input.make_move = 1  
            return player_col, player_row

def player_input(board):
        
    while True:
            
            mouse_processor(board)
            
            if g_Input.make_move == 1:
                # checks if the selected cell is already used up
                if not board[player_row][player_col] == "-":
                    print ("Already in use!")
                    g_Input.make_move = 0
                    g_Input.correctMove_X = 0
                    g_Input.correctMove_Y = 0
                    continue
                
                # if all conditions are met, cell is filled with an X
                else:
                    board[player_row][player_col] = "X"
                    Graphics.draw_symbol(1, player_col, player_row)
                    g_Input.make_move = 0
                    g_Input.correctMove_X = 0
                    g_Input.correctMove_Y = 0
                    Graphics.window.refresh()
                    break
        
def ai_input(board):

    while True:
    # randint to generate a random pair of coordinates
        ai_y = randint(0, len(board) - 1)
        ai_x = randint(0, len(board[0]) - 1)
    
        # checks that the cell is empty, if not, try again with new coords
        if board[ai_y][ai_x] != "-":
            continue
        else:
            board[ai_y][ai_x] = "O"
            Graphics.draw_symbol(2, ai_x, ai_y)
            Graphics.window.refresh()
            break

def cheater(board):
    bestVal = 1000
    bestMove = [-1, -1]
 
    for row in range(3):    
        for column in range(3):
         
            # Check if cell is empty
            if board[row][column] == '-':
             
                # Make the move
                board[row][column] = "O"
 
                # compute evaluation function for this
                # move.
                moveVal = minimax(board, column, row)
 
                # Undo the move
                board[row][column] = '-'
 
                # If the value of the current move is
                # more than the best value, then update
                # best/
                if moveVal > bestVal:               
                    bestMove = [row, column]
                    bestVal = moveVal
                    
    print ("The best AI move is:",bestMove,"and the value of the best move is :",bestVal)

def evaluate(board):
    if Board.score_checker(board, "X") == 1:
        return 1

    elif Board.score_checker(board, "O") == 1:
        return 2

    else:
        return 0

def minimax(board, x, y):
    score = 0

    result = evaluate(board)
 
    if result == 1:
        return 1
 
    if result == 2:
        return -1

    if Board.count_chars(board, '-') == 0:
        return 0

    best = 0

    for y in range(3):
        for x in range(3):
            if board[y][x] == '-':
                board[y][x] = "O"
                score = score + minimax(board, x, y)
                board[y][x] = '-'
                best = min(score, best)
    return best
