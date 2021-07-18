import sdl2.ext
from math import sqrt

# initialize  SDL2 objects & variables
sdl2.ext.init()
width = 640
height = 480
window = sdl2.ext.Window("Noughts and Crosses", size=(width, height))
window_surface = window.get_surface()
window_pixels   = sdl2.ext.PixelView(window_surface)
window.show()

running = True

class Board:
    board = []
    
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        for row in range(rows):
            self.board.append(["-"] * (columns))
        
    # splits the cells into rows
    def print_board(self):
        for row in self.board:
            print (" ".join(row))
            
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
            if not ((player_col >= 0 and player_col < len(self.board[0]))):
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
            if not ((player_row >= 0 and player_row < len(self.board))):
                print ("Please enter a valid number.")
                continue
            else:
                break
    
        # checks if the selected cell is already used up
        if not self.board[player_row][player_col] == "-":
            print ("Already in use!")
            self.player_input()
        
        # if all conditions are met, cell is filled with an X
        else:
            self.board[player_row][player_col] = "X"
        
Gameboard = Board(3, 3)

while running == True:
    # 1. GET INPUT & PROCESS EVENTS
    events = sdl2.ext.get_events()
    for event in events:
      if event.type == sdl2.SDL_QUIT:
        running = False
        break
    Gameboard.print_board()
    Gameboard.player_input()