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
    
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = [["-"] * columns] * rows
        
    # splits the cells into rows
    def print_board(self):
        for row in self.board:
            print (" ".join(row))
            
    def get_cols(self):
        return len(self.board[0])
    
    def get_rows(self):
        return len(self.board)
            
Gameboard = Board(3, 3)
            
class Gameplay:
    
    def __init__(self, board):
        self.board = board
    
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
            if not ((player_col >= 0 and player_col < Board.get_cols(self))):
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
            if not ((player_row >= 0 and player_row < Board.get_rows(self))):
                print ("Please enter a valid number.")
                continue
            else:
                break
    
        # checks if the selected cell is already used up
        if not self.board[player_row][player_col] == "-":
            print ("Already in use!")
            self.player_input(self)
        
        # if all conditions are met, cell is filled with an X
        else:
            self.board[player_row][player_col] = "X"
            
    def ai_input(self):
        attempts = 0
        max_attempts = 20
    
        while True:
        # randint to generate a random pair of coordinates
            ai_y = randint(0, len(self.board) - 1)
            ai_x = randint(0, len(self.board[0]) - 1)
        
            # checks that the cell is empty, if not, try again with new coords
            if self.board[ai_y][ai_x] != "-":
                attempts += 1
                continue
            else:
                self.board[ai_y][ai_x] = "O"
                attempts += 1
                break
            if attempts >= max_attempts:
                print("Out of attempts")
            break
            
    def game_loop(self):
        print ("Player 1's turn")
        self.player_input()
        Gameboard.print_board()
        print ("AI's turn")
        self.ai_input()
        Gameboard.print_board()
        
Gameplay = Gameplay(Gameboard)

while running == True:
    # 1. GET INPUT & PROCESS EVENTS
    events = sdl2.ext.get_events()
    window.refresh()
    for event in events:
      if event.type == sdl2.SDL_QUIT:
        running = False
        break
    Gameboard.print_board()
    Gameplay.game_loop()
    break