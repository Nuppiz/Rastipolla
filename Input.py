import sdl2.ext
import Graphics
import Board

from random import randint

# functions controlling player and AI input

class Input:
  
  def __init__(self):
    self.mouse_x = 0
    self.mouse_y = 0
    self.correctMove_X = 0
    self.correctMove_Y = 0
    self.make_move = 0

g_Input = Input()

def mouse_processor(board, player_symbol):
    
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
                cheater(board, player_symbol)
    
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

def player_input(board, player_symbol):
        
    while True:
            
            mouse_processor(board, player_symbol)
            
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
                    board[player_row][player_col] = player_symbol
                    Graphics.draw_symbol(player_symbol, player_col, player_row)
                    g_Input.make_move = 0
                    g_Input.correctMove_X = 0
                    g_Input.correctMove_Y = 0
                    Graphics.window.refresh()
                    break
        
def ai_one_and_one(board, ai_symbol):
    # if this function is used, AI will always go for 1, 1 coordinates on its first turn

    board[1][1] = ai_symbol
    Graphics.draw_symbol(ai_symbol, 1, 1)
    Graphics.window.refresh()

def ai_first(board, ai_symbol):
    # before the AI makes its first move, it checks for the best cell to start from
    # based on how much empty space there is around the selected cell
    empty_space = 0
    max_empty_space = 0 # how much empty space there is around the cell that has the most of it
    best_move = [0, 0]

    for y in range(3):
        for x in range(3):
            if board[y][x] == "-":
                board[y][x] = ai_symbol
                # check for empty space around the cell within the boundaries of the board
                empty_space = check_surroundings(board, y, x)
            if empty_space >= max_empty_space:
                max_empty_space = empty_space
                best_move = [y, x]
            board[y][x] = "-"
            empty_space = 0
    board[best_move[0]][best_move[1]] = ai_symbol
    Graphics.draw_symbol(ai_symbol, best_move[1], best_move[0])

def check_surroundings(board, row, column):

    # set the boundaries of the grid
    top = -1
    bottom = 1
    left = -1
    right = 1

    empty_space = 0

    if row + top < 0: # prevent the function from checking cells beyond the top boundary
        top = 0
    if row + bottom > 2: # prevent the function from checking cells beyond the bottom boundary
        bottom = 0
    
    if column + left < 0: # prevent the function from checking cells beyond the left boundary
        left = 0
    if column + right > 2: # prevent the function from checking cells beyond the right boundary
        right = 0

    # check for empty spaces around the given cell, and finally return that amount to the main function
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            if board[row + y][column + x] == '-':
                empty_space += 1
    return empty_space

def cheater(board, player_symbol):
    # tells the player their best possible move
    bestVal = -1000
    bestMove = [-1, -1]
 
    for row in range(3):
        for column in range(3):
            if board[row][column] == '-':
                
                # Make the move
                board[row][column] = player_symbol

                # compute evaluation function for this
                # move.
                moveVal = minimax(board, True, 0)

                # Undo the move
                board[row][column] = '-'

                # If the value of the current move is
                # more than the best value, then update
                # best/
                if moveVal > bestVal:               
                    bestMove = [row, column]
                    bestVal = moveVal
                    
    print ("The best player move is:",bestMove,"and the value of the best move is:",bestVal)

def ai_prevent_player_win(board, player_symbol, ai_symbol):
    for y in range (3):
        for x in range(3):
            if board[y][x] == "-": # checks that the cell is empty
                board[y][x] = player_symbol # put a temporary X in the chosen cell

                # if that X would result in a player win, switch it to O to prevent it
                if Board.score_checker(board, player_symbol) == 1:
                    board[y][x] = ai_symbol
                    Graphics.draw_symbol(ai_symbol, x, y)
                    return True
                # else erase the temporary X and try again
                else:
                    board[y][x] = "-"
    return False

def ai_move(board, player_symbol, ai_symbol):

    # AI function that uses minimax to determine the best move
    bestVal = 1000
    bestMove = [-1, -1]
 
    for row in range(3):
        for column in range(3):
            if board[row][column] == '-':
                
                # Make the move
                board[row][column] = ai_symbol

                # compute evaluation function for this
                # move.
                moveVal = minimax(board, False, 0, player_symbol, ai_symbol)

                # Undo the move
                board[row][column] = '-'

                # If the value of the current move is
                # less than the best value, then update
                # best/
                if moveVal < bestVal:               
                    bestMove = [row, column]
                    bestVal = moveVal

    print ("The best AI move is:",bestMove,"and the value of the best move is:",bestVal)
    board[bestMove[0]][bestMove[1]] = ai_symbol
    Graphics.draw_symbol(ai_symbol, bestMove[1], bestMove[0])
    return True

def ai_logic(board, ai_symbol, player_symbol):
    success = ai_prevent_player_win(board, player_symbol, ai_symbol, )

    if success == False:
        ai_move(board, player_symbol, ai_symbol)

def ai_random(board, ai_symbol):
    # alternative AI function that just chooses random coordinates
    while True:
    # randint to generate a random pair of coordinates
        ai_y = randint(0, len(board) - 1)
        ai_x = randint(0, len(board[0]) - 1)
    
        # checks that the cell is empty, if not, try again with new coords
        if board[ai_y][ai_x] != "-":
            continue
        else:
            board[ai_y][ai_x] = ai_symbol
            Graphics.draw_symbol(ai_symbol, ai_x, ai_y)
            Graphics.window.refresh()
            break

def evaluate(board, player_symbol, ai_symbol):
    if Board.score_checker(board, player_symbol) == 1:
        return 10

    elif Board.score_checker(board, ai_symbol) == 1:
        return -10

    else:
        return 0

def minimax(board, isMax, depth, player_symbol, ai_symbol):

    result = evaluate(board, player_symbol, ai_symbol)
 
    if result == 10:
        return result - depth
 
    if result == -10:
        return result + depth

    if Board.count_chars(board, '-') == 0:
        return 0

    if isMax == True:
        best = -1000
        for y in range(3):
            for x in range(3):
                if board[y][x] == '-':
                    board[y][x] = player_symbol
                    best = max(best, minimax(board, False, depth + 1, player_symbol, ai_symbol))
                    board[y][x] = '-'
        return best

    elif isMax == False:
        best = 1000
        for y in range(3):
            for x in range(3):
                if board[y][x] == '-':
                    board[y][x] = ai_symbol
                    best = min(best, minimax(board, True, depth + 1, player_symbol, ai_symbol))
                    board[y][x] = '-'
        return best
