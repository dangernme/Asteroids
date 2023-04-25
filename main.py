import sys
from os.path import join
import pygame as pg
from settings import *
from spaceship import Spaceship
Vec = pg.math.Vector2


pg.init()
pg.font.init()
font = pg.font.SysFont('Comic Sans MS', TEXT_SIZE)
window = pg.display.set_mode(SIZE)
clock = pg.time.Clock()
pg.display.set_caption(TITLE)

def draw(bg_image, player, rocket):
    window.blit(bg_image, (TEXT_WIDTH, 0))
    if rocket is not None:
        rocket.draw()
    player.draw()
    pg.draw.rect(window, (50,50,50), pg.Rect(0,0, TEXT_WIDTH, HEIGHT))
            
    window.blit(font.render(f"Max Speed {player.acc_lim * 100}", False, TEXT_COLOR), (10, 5))
    window.blit(font.render(f"Health {player.health}", False, TEXT_COLOR), (10, 35))
    window.blit(font.render(f"Rockets {player.rockets}", False, TEXT_COLOR), (10, 65))

    pg.display.update()

def main():
    running = True

    bg_image = pg.transform.scale(pg.image.load(
        join('assets', 'Background', 'Blue_Nebula_01.png')), \
        (WIDTH - TEXT_WIDTH, HEIGHT))
    
    player = Spaceship(Vec(WIDTH // 2, HEIGHT // 2))

    rocket = None
    while running:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL:
                    rocket = player.fire()

        player.update()
        if rocket is not None:
            rocket.update()
        draw(bg_image, player, rocket)
        
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
