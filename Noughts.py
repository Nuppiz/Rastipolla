import sdl2.ext
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
grid = sdl2.ext.load_image(res_path.get_path("grid.png"))
cross = sdl2.ext.load_image(res_path.get_path("cross.png"))
nought = sdl2.ext.load_image(res_path.get_path("nought.png"))
sdl2.SDL_SetColorKey(grid, sdl2.SDL_TRUE, 0xFF00FF)
sdl2.SDL_SetColorKey(cross, sdl2.SDL_TRUE, 0xFF00FF)
sdl2.SDL_SetColorKey(nought, sdl2.SDL_TRUE, 0xFF00FF)
sdl2.SDL_BlitSurface(grid, None, window_surface, None)

running = True

def draw(marker, x, y):
    
    draw_x = 105 + (int(x) * 145) # horizontal draw location
    draw_y = 25 + (int(y) * 145) # vertical draw location

    sdl2.SDL_BlitSurface(marker, None, window_surface, sdl2.SDL_Rect(draw_x, draw_y)) # draw X or O at the correct grid location

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
        else:
            return 0
    
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
        
mouseClicked = False
correctMove = False
        
def mouse_processor():
    
    global mouseClicked
    global correctMove
    
    mouse_x = 0
    mouse_y = 0
    
    events = sdl2.ext.get_events()
    
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            return False
        elif event.type == sdl2.SDL_MOUSEMOTION:
            mouse_x = event.motion.x
            mouse_y = event.motion.y
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if event.button.button == sdl2.SDL_BUTTON_LEFT:
                mouseClicked = True
        return mouse_x, mouse_y
         
        if int(mouse_x) > 104 and int(mouse_x) < 245:
            player_col = 0
            correctMove = True
        elif int(mouse_x) > 249 and int(mouse_x) < 390:
            player_col = 1
            correctMove = True
        elif int(mouse_x) > 394 and int(mouse_x) < 535:
            player_col = 2
            correctMove = True
        else:
            print ("Clicked outside of the play area.")
            
        if int(mouse_y) > 24 and int(mouse_x) < 165:
            player_row = 0
            correctMove = True
        elif int(mouse_y) > 169 and int(mouse_x) < 310:
            player_row = 1
            correctMove = True
        elif int(mouse_y) > 314 and int(mouse_x) < 455:
            player_row = 2
            correctMove = True
        else:
            print ("Clicked outside of the play area.")
            
        return player_col, player_row
    
def player_input(board):
    
    global mouseClicked
    global correctMove
        
    while True:
        mouse_processor()
        
        if mouseClicked == True and correctMove == True:
            # checks if the selected cell is already used up
            if not Gameboard[player_row][player_col] == "-":
                print ("Already in use!")
                mouseClicked = False
                correctMove = False
                continue
            
            # if all conditions are met, cell is filled with an X
            else:
                Gameboard[player_row][player_col] = "X"
                draw(cross, player_col, player_row)
                mouseClicked = False
                correctMove = False
                window.refresh()
                break
            
class Gameplay:
    
    def __init__(self, play_area):
        self.play_area = play_area
            
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
                draw(nought, ai_x, ai_y)
                window.refresh()
                break
            if attempts >= max_attempts:
                print("Out of attempts")
            break

    def ai_move(self):
        bestScore = -1000
        bestMove = None
        
        row = 0
        column = 0

        for column in range(0, 2):
            column += 1
            for row in range(0, 2):        
                if self.play_area.board[row][column] == "-":
                    self.play_area.board[row][column] = "O"
                    score = self.miniMax(self.play_area.board, 0, True)
                    self.play_area.board[row][column] = "-"
                    if score > bestScore:
                        bestScore = score
                        self.play_area.board[row][column] = "O"
                        break
                row += 1
                
    scores = {
        "X": -10,
        "O": 10,
        };
                
    def miniMax(self, board, depth, isMaximizing):
        
        row = 0
        column = 0
        
        if isMaximizing == True:
            bestScore = -100
            
            for column in range(0, 2):
                column += 1
                for row in range(0, 2):  
            
                    if self.play_area.board[row][column] == "-":
                        self.play_area.board[row][column] = "O"
                        score = self.miniMax(self.play_area.board, depth + 1, False)
                        self.play_area.board[row][column] = "-"
                        bestScore = max(score, bestScore)
                    row += 1
                
            return bestScore
        
        else:
            bestScore = 100
            
            for column in range(0, 2):
                column += 1
                for row in range(0, 2):  
            
                    if self.play_area.board[row][column] == "-":
                        self.play_area.board[row][column] = "X"
                        score = self.miniMax(self.play_area.board, depth + 1, True)
                        self.play_area.board[row][column] = "-"
                        bestScore = min(score, bestScore)
                    row += 1
                
            return bestScore
            
    def game_loop(self):
        Gameboard.print_board(Gameboard)
        print ("Player 1's turn")
        player_input(Gameboard)
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

def main():
    running = True
    
    while running == True:
        window.refresh()
        Gameplay.game_loop()
        
main()