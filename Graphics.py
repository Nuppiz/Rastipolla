import sdl2.ext
import ctypes

from time import sleep
from math import sqrt

# initialize  SDL2 objects & variables
sdl2.ext.init()
res_path        = sdl2.ext.Resources(__file__, ".")
width           = 800
height          = 600
res_index       = 1 # index number for the currently used resolution
window_p        = sdl2.SDL_CreateWindow(b"Noughts and Crosses", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, width, height, sdl2.SDL_WINDOW_RESIZABLE, sdl2.SDL_WINDOW_SHOWN)
window          = window_p.contents
window_surface  = sdl2.SDL_GetWindowSurface(window)
factory         = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
spriterenderer  = factory.create_sprite_render_system(window)
uifactory       = sdl2.ext.UIFactory(factory)
uiprocessor     = sdl2.ext.UIProcessor()

# load textures
textures = {
  "splash" : sdl2.ext.load_image(res_path.get_path("splash.png")),
  "grid"   : sdl2.ext.load_image(res_path.get_path("grid.png")),
  "cross"  : sdl2.ext.load_image(res_path.get_path("cross.png")),
  "nought" : sdl2.ext.load_image(res_path.get_path("nought.png")),
  "winner" : sdl2.ext.load_image(res_path.get_path("youwon.png")),
  "loser"  : sdl2.ext.load_image(res_path.get_path("youlost.png")),
  "tie"    : sdl2.ext.load_image(res_path.get_path("tie.png"))
}

# set transparencies
for tex in textures.values():
  sdl2.SDL_SetColorKey(tex, sdl2.SDL_TRUE, 0xFF00FF)

# load splash screen
sdl2.SDL_BlitScaled(textures["splash"], None, window_surface, sdl2.SDL_Rect(0, 0, width, height))

# render code and event processor for the start screen, which currently has just one button - New Game
def start_screen():

    # global value which is monitored by the main program to monitor if this button is clicked, and start a new game if it has been
    global NewGameClicked
    NewGameClicked = 0
    
    # button to start a new game - how can I scale the size for this?
    startgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("start.png"))
    #startgame.size = int(width * 0.313), int(height * 0.208)
    startgame.position = int(width * 0.344), int(height * 0.563)
    
    spriterenderer.render((startgame))
    
    startgame.click += restart # calls the function to start a new game, by changing NewGameClicked to 1
    
    running = True
    
    while running:

        sdl2.SDL_UpdateWindowSurface(window_p)
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                quit()

            if event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    print("User resized window")

            uiprocessor.dispatch([startgame], event)
            
            if NewGameClicked == 1:
                NewGameClicked = 0
                return 1

# function to draw a single X or O on the grid
def draw_symbol(symbol, y, x):

    window_surface = sdl2.SDL_GetWindowSurface(window)

    # grid_table is a temporary table that stores the necessarily values for aligning and rescaling the symbol graphics
    # these values are calculated in the screen_query function, the reason why this is called each time a symbol is drawn is to keep the symbol locations
    # and sizes correctly updated if the screen resolution is changed mid-game
    grid_table = screen_query()

    # empty space on the left of the screen
    horizontal_margin = grid_table[0]
    # empty space on the top of the screen
    vertical_margin = grid_table[1]
    # size of each square on the grid
    square_size_h = grid_table[2]
    square_size_v = grid_table[3]

    # decide which symbol to draw based on what argument is sent to the function
    if symbol == "X":
        symbol = textures["cross"]
        
    elif symbol == "O":
        symbol = textures["nought"]
    
    draw_x = horizontal_margin + (int(x) * square_size_h) # horizontal draw location
    draw_y = vertical_margin + (int(y) * square_size_v) # vertical draw location

    # draw X or O at the correct grid location, scaled to screen size
    sdl2.SDL_BlitScaled(symbol, None, window_surface, sdl2.SDL_Rect(draw_x, draw_y, int(width * 0.219), int(height * 0.292)))

# function that goes through the "board" table and calls the above function to draw appropriate symbols on the grid
def draw_symbols(board):
    for row in range(3):
        for column in range(3):
            symbol = board[row][column]
            if board[row][column] != "-":
                draw_symbol(symbol, row, column)
    sdl2.SDL_UpdateWindowSurface(window_p)

# function that "clears" the screen by drawing new empty items on top
def clear_screen():
    window_surface = sdl2.SDL_GetWindowSurface(window)

    # draw background colour
    color = sdl2.ext.Color(0, 0, 127, 0)
    sdl2.SDL_FillRect(window_surface, None, color)

    # draw grid
    sdl2.SDL_BlitScaled(textures["grid"], None, window_surface, sdl2.SDL_Rect(0, 0, width, height))

# render code and event processor for the "Game Over" screen, which currently has two buttons - Play Again or Quit
def end_screen(ending, board):

    window_surface = sdl2.SDL_GetWindowSurface(window)
    spriterenderer = factory.create_sprite_render_system(window)
    
    global NewGameClicked
    NewGameClicked = 0
    
    # select the ending graphic based on how the game ended
    if ending == 1:
        end_type = textures["winner"]
        
    elif ending == 2:
        end_type = textures["tie"]
        
    elif ending == 3:
        end_type = textures["loser"]
    
    running = True

    sdl2.SDL_BlitScaled(end_type, None, window_surface, sdl2.SDL_Rect(0, 0, width, height)) # draw ending screen depending on how the game ended
    sdl2.SDL_UpdateWindowSurface(window_p)
    sleep(1) # small pause before buttons appear
    
    # button rendering and what functions they activate

    newgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("playagain.png"))
    newgame.position = int(width * 0.078), int(height * 0.667)
    quitgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("quit.png"))
    quitgame.position = int(width * 0.722), int(height * 0.667)
    
    spriterenderer.render((newgame, quitgame))
    sdl2.SDL_UpdateWindowSurface(window_p)
    
    newgame.click += restart
    quitgame.click += endgame
    
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                quit()

            if event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    print("User resized window")
                    redraw(window, board)
                    end_screen_mini(ending) # redraw ending graphics in new resolution
            
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN: 
                if event.button.button == sdl2.SDL_BUTTON_RIGHT:   
                    change_resolution(board)
                    end_screen_mini(ending) # redraw ending graphics in new resolution

            uiprocessor.dispatch([newgame, quitgame], event)
            
            if NewGameClicked == 1:
                NewGameClicked = 0
                return 1

def end_screen_mini(ending):
    # miniaturized version of the above function to just redraw the ending graphics

    window_surface = sdl2.SDL_GetWindowSurface(window)
    spriterenderer = factory.create_sprite_render_system(window)
    
    global NewGameClicked
    NewGameClicked = 0
    
    # select the ending graphic based on how the game ended
    if ending == 1:
        end_type = textures["winner"]
        
    elif ending == 2:
        end_type = textures["tie"]
        
    elif ending == 3:
        end_type = textures["loser"]

    sdl2.SDL_BlitScaled(end_type, None, window_surface, sdl2.SDL_Rect(0, 0, width, height)) # draw ending screen depending on how the game ended

    newgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("playagain.png"))
    newgame.position = int(width * 0.078), int(height * 0.667)
    quitgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("quit.png"))
    quitgame.position = int(width * 0.722), int(height * 0.667)
    
    spriterenderer.render((newgame, quitgame))

    sdl2.SDL_UpdateWindowSurface(window_p)

# this is the function that is called by the New Game/Play Again buttons, and simply changes the value of NewGameClicked so the main program knows to start a new game
def restart(button, event):
    global NewGameClicked
    
    NewGameClicked = 1

# this just quits the game
def endgame(button, event):
    quit()

# change the play area's resolution and redraw the screen accordingly
def change_resolution(board):

    global height
    global width
    global res_index # by default this is 1, and it's just used to decide which resolution to use next

    res_changed = 0 # just a switch to make sure the game only changes resolution once per click instead of looping through them

    if res_index == 1 and res_changed == 0:
        res_index = 2 # this changes so that the next time the function is called, it knows to change to a different resolution than before
        width = 1280
        height = 960
        res_changed = 1
    elif res_index == 2 and res_changed == 0:
        res_index = 0
        width = 640
        height = 480
        res_changed = 1
    elif res_index == 0 and res_changed == 0:
        res_index = 1
        width = 800
        height = 600
        res_changed = 1

    print("New size of the window is", width, height)
    sdl2.SDL_SetWindowSize(window_p, width, height)

    # graphics are redrawn for the new screen size
    clear_screen()
    draw_symbols(board)
    sdl2.SDL_UpdateWindowSurface(window_p)

def screen_query():
    # calculate grid margins and square size, then send them as a table to whatever function is asking for them

    aspect_ratio = (width / height) / 1.333
    screen_area = width * height

    horizontal_margin = int(width * 0.165)
    vertical_margin = int(height * 0.053)
    square_size_h = int(width * 0.227)
    square_size_v = int(height * 0.303)
    print ("SS H:", square_size_h,", V:", square_size_v)

    screen_table = [horizontal_margin, vertical_margin, square_size_h, square_size_v]

    return screen_table

def return_window():
    # dummy function so the "window" variable can be used outside of Graphics.py
    return window

def refresh_screen(window):
    sdl2.SDL_UpdateWindowSurface(window)

def redraw(window, board):

    global width
    global height

    # for GetWindowSize to work, we need to convert the width and height into separate ctype variables
    width_p = ctypes.c_int()
    height_p = ctypes.c_int()

    sdl2.SDL_GetWindowSize(window, width_p, height_p)

    print("New size of the window is", width_p.value, height_p.value)
    sdl2.SDL_SetWindowSize(window_p, width_p.value, height_p.value)

    # then for the graphics drawing functions, we need to convert them back to normal Python integers
    width = int(width_p.value)
    height = int(height_p.value)

    # graphics are redrawn for the new screen size
    clear_screen()
    draw_symbols(board)
    sdl2.SDL_UpdateWindowSurface(window_p)