import sdl2.ext
import Graphics

from random import randint

# functions controlling player and AI input

mouseClicked = False

def mouse_processor():
    
    global mouseClicked
    
    events = sdl2.ext.get_events()
    Graphics.window.refresh()
    
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            quit()
        elif event.type == sdl2.SDL_MOUSEMOTION:
            mouse_x = event.motion.x
            mouse_y = event.motion.y
        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            mouse_x = event.motion.x
            mouse_y = event.motion.y
            if event.button.button == sdl2.SDL_BUTTON_LEFT:
                mouseClicked = True       
                print (mouseClicked, mouse_x, mouse_y)
                check_cursor(mouse_x, mouse_y)
    
def check_cursor(mouse_x, mouse_y):
    
    global correctMove_X
    global correctMove_Y
    
    global player_col
    global player_row
    
    while True: 
        if int(mouse_x) >= 104 and int(mouse_x) <= 245:
            player_col = 0
            correctMove_X = 1
        elif int(mouse_x) >= 249 and int(mouse_x) <= 390:
            player_col = 1
            correctMove_X = 1
        elif int(mouse_x) >= 394 and int(mouse_x) <= 535:
            player_col = 2
            correctMove_X = 1
        else:
            print ("Clicked outside of the play area (X).")
            
        if int(mouse_y) >= 24 and int(mouse_y) <= 165:
            player_row = 0
            correctMove_Y = 1
        elif int(mouse_y) >= 169 and int(mouse_y) <= 310:
            player_row = 1
            correctMove_Y = 1
        elif int(mouse_y) >= 314 and int(mouse_y) <= 455:
            player_row = 2
            correctMove_Y = 1
        else:
            print ("Clicked outside of the play area (Y).")
           
        return player_col, player_row

def player_input(board):
    
    global mouseClicked
    global correctMove_X
    global correctMove_Y
        
    while True:
            
            mouse_processor()
            
            if mouseClicked == True and correctMove_X == True and correctMove_Y == True:
                # checks if the selected cell is already used up
                if not board[player_row][player_col] == "-":
                    print ("Already in use!")
                    mouseClicked = False
                    correctMove_X = False
                    correctMove_Y = False
                    continue
                
                # if all conditions are met, cell is filled with an X
                else:
                    board[player_row][player_col] = "X"
                    Graphics.draw_cross(player_col, player_row)
                    mouseClicked = False
                    correctMove_X = False
                    correctMove_Y = False
                    Graphics.window.refresh()
                    break
        
def ai_input(board):
    attempts = 0
    max_attempts = 20

    while True:
    # randint to generate a random pair of coordinates
        ai_y = randint(0, len(board) - 1)
        ai_x = randint(0, len(board[0]) - 1)
    
        # checks that the cell is empty, if not, try again with new coords
        if board[ai_y][ai_x] != "-":
            attempts += 1
            continue
        else:
            board[ai_y][ai_x] = "O"
            Graphics.draw_nought(ai_x, ai_y)
            Graphics.window.refresh()
            break
        if attempts >= max_attempts:
            print("Out of attempts")
        break

def ai_move(board):
    bestScore = -1000
    bestMove = None
    
    row = 0
    column = 0

    for column in range(0, 2):
        column += 1
        for row in range(0, 2):        
            if board[row][column] == "-":
                board[row][column] = "O"
                score = miniMax(board, 0, True)
                board[row][column] = "-"
                if score > bestScore:
                    bestScore = score
                    board[row][column] = "O"
                    break
            row += 1
            
scores = {
    "X": -10,
    "O": 10,
    };
            
def miniMax(board, depth, isMaximizing):
    
    row = 0
    column = 0
    
    if isMaximizing == True:
        bestScore = -100
        
        for column in range(0, 2):
            column += 1
            for row in range(0, 2):  
        
                if board[row][column] == "-":
                    board[row][column] = "O"
                    score = miniMax(board, depth + 1, False)
                    board[row][column] = "-"
                    bestScore = max(score, bestScore)
                row += 1
            
        return bestScore
    
    else:
        bestScore = 100
        
        for column in range(0, 2):
            column += 1
            for row in range(0, 2):  
        
                if board[row][column] == "-":
                    board[row][column] = "X"
                    score = miniMax(board, depth + 1, True)
                    board[row][column] = "-"
                    bestScore = min(score, bestScore)
                row += 1
            
        return bestScore