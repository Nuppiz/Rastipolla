import sdl2.ext
import Graphics
import Board
import Input

def game_loop(board, player_symbol, ai_symbol):
    
    global NewGameClicked
    NewGameClicked = 0

    # AI loop
    Board.print_board(Gameboard)
    Graphics.draw_symbols(Gameboard)
    print ("AI's turn")
    if Board.count_chars(board, "-") > 7: # on the first turn, the AI uses a different logic for determining its first move
        Input.ai_first(Gameboard, ai_symbol)
    else:
        Input.ai_logic(Gameboard, ai_symbol, player_symbol)
    if Board.victory_check(Gameboard, ai_symbol) == 1:
        Board.print_board(Gameboard)
        Graphics.draw_symbols(Gameboard)
        if Graphics.end_screen(3, Gameboard):
            main()
    elif Board.draw_check(Gameboard) == 1:
        Graphics.draw_symbols(Gameboard)
        if Graphics.end_screen(2, Gameboard):
            main()

    # player loop
    Board.print_board(Gameboard)
    Graphics.draw_symbols(Gameboard)
    print ("Player 1's turn")
    Input.player_input(Gameboard, player_symbol)
    if Board.victory_check(Gameboard, player_symbol) == 1:
        Board.print_board(Gameboard)
        Graphics.draw_symbols(Gameboard)
        if Graphics.end_screen(1, Gameboard):
            main()
    elif Board.draw_check(Gameboard) == 1:
        Graphics.draw_symbols(Gameboard)
        if Graphics.end_screen(2, Gameboard):
            main()

def main():
    running = True 
    
    Board.clear_board(Gameboard)
    Graphics.clear_screen()
    
    while running == True:
        Graphics.window.refresh()
        game_loop(Gameboard, "X", "O")
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                quit()
                
Gameboard = []
Board.init_board(Gameboard)
if Graphics.start_screen():
    main()