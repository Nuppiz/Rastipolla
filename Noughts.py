import sdl2.ext
from math import sqrt
from random import randint

# initialize  SDL2 objects & variables
sdl2.ext.init()
res_path        = sdl2.ext.Resources(__file__, ".")
width           = 640
height          = 480
window          = sdl2.ext.Window("Noughts and Crosses", size=(width, height))
window_surface  = window.get_surface()
window_pixels   = sdl2.ext.PixelView(window_surface)
window.show()

# draw background
color = sdl2.ext.Color(0, 127, 0)
sdl2.ext.fill(window_surface, color, (0, 0, width, height))

# load & draw picture
kuva = sdl2.ext.load_image(res_path.get_path("kuva.png"))
sdl2.SDL_SetColorKey(kuva, sdl2.SDL_TRUE, 0x0000FF)
sdl2.SDL_BlitScaled(kuva, None, window_surface, None)

running = True

class Board:
    
    board = []
    
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        
        # create board
        for row in range(rows):
            self.board.append(["-"] * (columns))
        
    # splits the cells into rows
    def print_board(self, board):
        for row in self.board:
            print (" ".join(row))
            
    def get_cols(self):
        return len(self.board[0])
    
    def get_rows(self):
        return len(self.board)
    
    def score_checker(self, character):
        if self.getMax(character) == 3:
            return 1
        elif self.check_diagonal(character) == 1:
            return 1
    
    def getMax(self, character):
        max_rows = self.check_rows(character)
        max_cols = self.check_columns(character)
        
        return max(max_rows, max_cols)
    
    # functions to check each row and column for consecutive characters (X or O)
    def check_rows(self, character):
        max_score = 0
        for row in range(0,len(self.board)):
            score = 0
            for column in range(0,len(self.board[0])):
                if self.board[row][column] == character:
                    score +=1
                    if score > max_score:
                        max_score = score
                else:
                    score = 0
                    
        return max_score
    
    def check_columns(self, character):
        max_score = 0
        for column in range(0,len(self.board[0])):
            score = 0
            for row in range(0,len(self.board)):
                if self.board[row][column] == character:
                    score +=1
                    if score > max_score:
                        max_score = score
                else:
                    score = 0
                    
        return max_score
    
    def check_diagonal(self, character):
        if self.board[0][0] == character and self.board[1][1] == character and self.board[2][2] == character:
            return 1
        elif self.board[2][0] == character and self.board[1][1] == character and self.board[0][2] == character:
            return 1
        else:
            return 0
            
class Gameplay:
    
    def __init__(self, play_area):
        self.play_area = play_area
    
    def player_input(self):
        
    # try-excepts to make sure player enters a number and not some other character
    # column first
        while True:    
            try:
                player_col = int(input("Enter Column: "))-1
            except ValueError:
                print ("Please enter a valid number.")
                continue
            #checks that player enters a number within the range of the board
            if not ((player_col >= 0 and player_col < Board.get_cols(self.play_area))):
                print ("Please enter a valid number.")
                continue
            else:
                break
            
        # then row
        while True:    
            try:
                player_row = int(input("Enter Row: "))-1
            except ValueError:        
                print ("Please enter a valid number.")
                continue
            if not ((player_row >= 0 and player_row < Board.get_rows(self.play_area))):
                print ("Please enter a valid number.")
                continue
            else:
                break
    
        # checks if the selected cell is already used up
        if not self.play_area.board[player_row][player_col] == "-":
            print ("Already in use!")
            self.player_input()
        
        # if all conditions are met, cell is filled with an X
        else:
            self.play_area.board[player_row][player_col] = "X"
            
    def ai_input(self):
        attempts = 0
        max_attempts = 20
    
        while True:
        # randint to generate a random pair of coordinates
            ai_y = randint(0, Board.get_cols(self.play_area) - 1)
            ai_x = randint(0, Board.get_rows(self.play_area) - 1)
        
            # checks that the cell is empty, if not, try again with new coords
            if self.play_area.board[ai_y][ai_x] != "-":
                attempts += 1
                continue
            else:
                self.play_area.board[ai_y][ai_x] = "O"
                break
            if attempts >= max_attempts:
                print("Out of attempts")
            break
            
    def game_loop(self):
        Gameboard.print_board(Gameboard)
        print ("Player 1's turn")
        self.player_input()
        Board.score_checker(Gameboard, "X")
        if Board.score_checker(Gameboard, "X") == 1:
            print ("Player 1 wins!")
            Gameboard.print_board(Gameboard)
            quit()
        Gameboard.print_board(Gameboard)
        print ("AI's turn")
        self.ai_input()
        Board.score_checker(Gameboard, "O")
        if Board.score_checker(Gameboard, "O") == 1:
            print ("AI wins!")
            Gameboard.print_board(Gameboard)
            quit()
        
Gameboard = Board(3, 3)   
Gameplay = Gameplay(Gameboard)

while running == True:
    # 1. GET INPUT & PROCESS EVENTS
    events = sdl2.ext.get_events()
    window.refresh()
    for event in events:
      if event.type == sdl2.SDL_QUIT:
        running = False
        break
    Gameplay.game_loop()