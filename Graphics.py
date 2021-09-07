import sdl2.ext
#import sdl2.sdlimage

from time import sleep

global height
global width
global res_index

# initialize  SDL2 objects & variables
sdl2.ext.init()
res_path        = sdl2.ext.Resources(__file__, ".")
width           = 800
height          = 600
res_index       = 1
window          = sdl2.ext.Window("Noughts and Crosses", size=(width, height), flags=sdl2.SDL_WINDOW_RESIZABLE)
window_surface  = window.get_surface()
factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
spriterenderer = factory.create_sprite_render_system(window)
uifactory = sdl2.ext.UIFactory(factory)
uiprocessor = sdl2.ext.UIProcessor()
window.show()

# calculate grid margins and sizes
horizontal_margin = int(width * 0.165)
vertical_margin = int(height * 0.053)
square_size = int(width * 0.227)

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

def start_screen():
    global NewGameClicked
    NewGameClicked = 0
    
    startgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("start.png"))
    #startgame.size = int(width * 0.313), int(height * 0.208)
    startgame.position = int(width * 0.344), int(height * 0.563)
    
    spriterenderer.render((startgame))
    
    startgame.click += restart
    
    running = True
    
    while running:

        window.refresh()
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                quit()

            if event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    print("User resized window")

            #if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                #if event.button.button == sdl2.SDL_BUTTON_RIGHT:   
                    #refresh_screen()

            uiprocessor.dispatch([startgame], event)
            
            if NewGameClicked == 1:
                NewGameClicked = 0
                return 1

def draw_symbol(symbol, y, x):

    grid_table = screen_query()

    horizontal_margin = grid_table[0]
    vertical_margin = grid_table[1]
    square_size = grid_table[2]

    if symbol == "X":
        symbol = textures["cross"]
        
    elif symbol == "O":
        symbol = textures["nought"]
    
    draw_x = horizontal_margin + (int(x) * square_size) # horizontal draw location
    draw_y = vertical_margin + (int(y) * square_size) # vertical draw location

    # draw X or O at the correct grid location, scaled to screen size
    sdl2.SDL_BlitScaled(symbol, None, window_surface, sdl2.SDL_Rect(draw_x, draw_y, int(width * 0.219), int(height * 0.292)))

def draw_symbols(board):
    for row in range(3):
        for column in range(3):
            symbol = board[row][column]
            if board[row][column] != "-":
                draw_symbol(symbol, row, column)
    window.refresh()

def clear_screen():
    # draw background
    color = sdl2.ext.Color(0, 127, 0)
    sdl2.ext.fill(window_surface, color, (0, 0, width, height))

    # draw grid
    sdl2.SDL_BlitScaled(textures["grid"], None, window_surface, sdl2.SDL_Rect(0, 0, width, height))
    
def end_screen(ending, board):
    
    global NewGameClicked
    NewGameClicked = 0
    
    if ending == 1:
        end_type = textures["winner"]
        
    elif ending == 2:
        end_type = textures["tie"]
        
    elif ending == 3:
        end_type = textures["loser"]
    
    running = True

    sdl2.SDL_BlitScaled(end_type, None, window_surface, sdl2.SDL_Rect(0, 0, width, height)) # draw ending screen depending on how the game ended
    window.refresh()
    sleep(1) # small pause before buttons appear
    
    newgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("playagain.png"))
    newgame.position = int(width * 0.078), int(height * 0.667)
    quitgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("quit.png"))
    quitgame.position = int(width * 0.722), int(height * 0.667)
    
    spriterenderer.render((newgame, quitgame))
    window.refresh()
    
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
        
            uiprocessor.dispatch([newgame, quitgame], event)
            
            if NewGameClicked == 1:
                NewGameClicked = 0
                return 1
    
def restart(button, event):
    global NewGameClicked
    
    NewGameClicked = 1
    
def endgame(button, event):
    quit()

def refresh_screen(board):
    global height
    global width
    global res_index

    res_changed = 0

    if res_index == 1 and res_changed == 0:
        res_index = 2
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
    #sdl2.SDL_SetWindowSize(window, width, height)
    clear_screen()
    draw_symbols(board)
    window.refresh()

def screen_query():
    horizontal_margin = int(width * 0.165)
    vertical_margin = int(height * 0.053)
    square_size = int(width * 0.227)

    screen_table = [horizontal_margin, vertical_margin, square_size]

    return screen_table