import sdl2.ext
import sdl2.sdlimage

from time import sleep

# initialize  SDL2 objects & variables
sdl2.ext.init()
res_path        = sdl2.ext.Resources(__file__, ".")
width           = 640
height          = 480
window          = sdl2.ext.Window("Noughts and Crosses", size=(width, height))
window_surface  = window.get_surface()
factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
spriterenderer = factory.create_sprite_render_system(window)
uifactory = sdl2.ext.UIFactory(factory)
uiprocessor = sdl2.ext.UIProcessor()
window.show()

# load textures
grid = sdl2.ext.load_image(res_path.get_path("grid.png"))
cross = sdl2.ext.load_image(res_path.get_path("cross.png"))
nought = sdl2.ext.load_image(res_path.get_path("nought.png"))
winner = sdl2.ext.load_image(res_path.get_path("youwon.png"))
loser = sdl2.ext.load_image(res_path.get_path("youlost.png"))
tie = sdl2.ext.load_image(res_path.get_path("tie.png"))

# set transparencies
sdl2.SDL_SetColorKey(grid, sdl2.SDL_TRUE, 0xFF00FF)
sdl2.SDL_SetColorKey(cross, sdl2.SDL_TRUE, 0xFF00FF)
sdl2.SDL_SetColorKey(nought, sdl2.SDL_TRUE, 0xFF00FF)
sdl2.SDL_SetColorKey(winner, sdl2.SDL_TRUE, 0xFF00FF)
sdl2.SDL_SetColorKey(loser, sdl2.SDL_TRUE, 0xFF00FF)
sdl2.SDL_SetColorKey(tie, sdl2.SDL_TRUE, 0xFF00FF)

# draw background
color = sdl2.ext.Color(0, 127, 0)
sdl2.ext.fill(window_surface, color, (0, 0, width, height))

# draw grid
sdl2.SDL_BlitSurface(grid, None, window_surface, None)

def draw_cross(x, y):
    
    draw_x = 105 + (int(x) * 145) # horizontal draw location
    draw_y = 25 + (int(y) * 145) # vertical draw location

    sdl2.SDL_BlitSurface(cross, None, window_surface, sdl2.SDL_Rect(draw_x, draw_y)) # draw X at the correct grid location

def draw_nought(x, y):
    
    draw_x = 105 + (int(x) * 145) # horizontal draw location
    draw_y = 25 + (int(y) * 145) # vertical draw location

    sdl2.SDL_BlitSurface(nought, None, window_surface, sdl2.SDL_Rect(draw_x, draw_y)) # draw O at the correct grid location

def clear_screen():
    sdl2.ext.fill(window_surface, color, (0, 0, width, height))
    sdl2.SDL_BlitSurface(grid, None, window_surface, None)
    
def end_screen(ending, board):
    
    global NewGameClicked
    NewGameClicked = 0
    
    if ending == 1:
        end_type = winner
        
    elif ending == 2:
        end_type = tie
        
    elif ending == 3:
        end_type = loser
    
    running = True

    sdl2.SDL_BlitSurface(end_type, None, window_surface, None) # draw ending screen depending on how the game ended
    window.refresh()
    sleep(1) # small pause before buttons appear
    
    newgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("playagain.png"))
    newgame.position = 50, 320
    quitgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("quit.png"))
    quitgame.position = 462, 320
    
    spriterenderer.render((newgame, quitgame))
    window.refresh()
    
    newgame.click += restart
    quitgame.click += endgame
    
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                quit()
        
            uiprocessor.dispatch([newgame, quitgame], event)
            
            if NewGameClicked == 1:
                NewGameClicked = 0
                return 1
    
def restart(button, event):
    global NewGameClicked
    
    NewGameClicked = 1
    
def endgame(button, event):
    quit()