# functions for creating and editing the board as well as fetching data from it
    
def init_board(board):
    # create board
    for row in range(3):
        board.append(["-"] * (3))
    
# splits the cells into rows
def print_board(board):
    for row in board:
        print (" ".join(row))

# clear the board when a new game is started        
def clear_board(board):
    for row in range(3):
        for column in range(3):
            board[row][column] = "-"
                
def victory_check(board, character):
    if getMax(board, character) == 3:
        return 1
    elif check_diagonal(board, character) == 1:
        return 1
    else:
        return 0

def getMax(board, character):
    max_rows = check_rows(board, character)
    max_cols = check_columns(board, character)
    
    return max(max_rows, max_cols)

# functions to check each row and column for consecutive characters (X or O)
def check_rows(board, character):
    max_score = 0
    for row in range(3):
        score = 0
        for column in range(3):
            if board[row][column] == character:
                score +=1
                if score > max_score:
                    max_score = score
            else:
                score = 0
                
    return max_score

def check_columns(board, character):
    max_score = 0
    for column in range(3):
        score = 0
        for row in range(3):
            if board[row][column] == character:
                score +=1
                if score > max_score:
                    max_score = score
            else:
                score = 0
                
    return max_score

def check_diagonal(board, character):
    if board[0][0] == character and board[1][1] == character and board[2][2] == character:
        return 1
    elif board[2][0] == character and board[1][1] == character and board[0][2] == character:
        return 1
    else:
        return 0
    
# helper function to count the amount of empty cells left on the board
def count_chars(board, char):
    count = 0
    for row in board:
        count += row.count(char)
    return count
    
# if no empty cells are left and neither player has the required score, game ends in a draw
def draw_check(board):
    if count_chars(board, '-') == 0:
        print ("Board full, it's a draw!")
        print_board(board)
        return 1
    else:
        return 0

# function to check the current status of the given cell
def check_status(board, y, x, player_symbol, ai_symbol):
    if board[y][x] == "-":
        return 0
    elif board[y][x] == player_symbol:
        return 1
    elif board[y][x] == ai_symbol:
        return 2
