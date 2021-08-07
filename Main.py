import sdl2.ext
import Graphics
import Board
import Input

def game_loop(board):
    
    global NewGame
    
    NewGame = True
    
    Board.print_board(Gameboard)
    print ("Player 1's turn")
    Input.player_input(Gameboard)
    if Board.score_checker(Gameboard, "X") == 1:
        Board.print_board(Gameboard)
        print (NewGame)
        Graphics.end_screen(1, Gameboard)
        if NewGame == True:
            main()         
    elif Board.draw_check(Gameboard) == 1:
        Graphics.end_screen(2, Gameboard)
        
    Board.print_board(Gameboard)
    print ("AI's turn")
    Input.ai_input(Gameboard)
    if Board.score_checker(Gameboard, "O") == 1:
        Board.print_board(Gameboard)
        Graphics.end_screen(3, Gameboard)
    elif Board.draw_check(Gameboard) == 1:
        Graphics.end_screen(2, Gameboard)
        
Gameboard = []

def main():
    running = True 
    
    Board.clear_board(Gameboard)
    Graphics.clear_screen()
    Board.init_board(Gameboard)
    
    while running == True:
        Graphics.window.refresh()
        game_loop(Gameboard)
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        
main()