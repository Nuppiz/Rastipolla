import sdl2.ext
import Graphics
import Board
import Input

def game_loop(board):
    
    global NewGameClicked
    NewGameClicked = 0

    Board.print_board(Gameboard)
    print ("AI's turn")
    if Board.count_chars(board, "-") == 9: # if AI starts first, its first move will be random to give it some extra flavor
        Input.ai_random(Gameboard)
    else:
        Input.ai_logic(Gameboard)
    if Board.score_checker(Gameboard, "O") == 1:
        Board.print_board(Gameboard)
        if Graphics.end_screen(3, Gameboard):
            main()
    elif Board.draw_check(Gameboard) == 1:
        if Graphics.end_screen(2, Gameboard):
            main()
    
    
    Board.print_board(Gameboard)
    print ("Player 1's turn")
    Input.player_input(Gameboard)
    if Board.score_checker(Gameboard, "X") == 1:
        Board.print_board(Gameboard)
        if Graphics.end_screen(1, Gameboard):
            main()
    elif Board.draw_check(Gameboard) == 1:
        if Graphics.end_screen(2, Gameboard):
            main()

def main():
    running = True 
    
    Board.clear_board(Gameboard)
    Graphics.clear_screen()
    
    while running == True:
        Graphics.window.refresh()
        game_loop(Gameboard)
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                quit()
                
Gameboard = []
Board.init_board(Gameboard)
if Graphics.start_screen():
    main()