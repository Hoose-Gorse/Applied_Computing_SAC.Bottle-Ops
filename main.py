import pygame as pg
from sys import exit

SCREENRECT = pg.Rect(0, 0, 1925, 1025) #last two numbers are width and length
clock = pg.time.Clock()

#test_surface = pg.image.load('')
pg.display.set_caption("Bottle Ops")

def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()


def load_sound(file):
    """because pygame can be compiled without mixer."""
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print(f"Warning, unable to load, {file}")
    return None

def main():
    if pg.get_sdl_version()[0] == 2: #sound stuff
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None
        
    while True: #main game loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        bestdepth = pg.display.mode_ok(SCREENRECT.size, 0, 32)
        screen = pg.display.set_mode(SCREENRECT.size, 0, bestdepth)        
        screen.blit(test_surface, (0,0))
        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pg.quit()
