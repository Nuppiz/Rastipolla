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
sdl2.SDL_BlitSurface(textures["splash"], None, window_surface, None)

def start_screen():
    global NewGameClicked
    NewGameClicked = 0
    
    startgame = uifactory.from_image(sdl2.ext.BUTTON, res_path.get_path("start.png"))
    startgame.position = 220, 270
    
    spriterenderer.render((startgame))
    
    startgame.click += restart
    
    running = True
    
    while running:
        window.refresh()
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                quit()
        
            uiprocessor.dispatch([startgame], event)
            
            if NewGameClicked == 1:
                NewGameClicked = 0
                return 1

def draw_symbol(symbol, x, y):
    
    if symbol == 1:
        symbol = textures["cross"]
        
    elif symbol == 2:
        symbol = textures["nought"]
    
    draw_x = 105 + (int(x) * 145) # horizontal draw location
    draw_y = 25 + (int(y) * 145) # vertical draw location

    sdl2.SDL_BlitSurface(symbol, None, window_surface, sdl2.SDL_Rect(draw_x, draw_y)) # draw X or O at the correct grid location

def clear_screen():
    # draw background
    color = sdl2.ext.Color(0, 127, 0)
    sdl2.ext.fill(window_surface, color, (0, 0, width, height))

    # draw grid
    sdl2.SDL_BlitSurface(textures["grid"], None, window_surface, None)
    
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