import sys
from os.path import join
import pygame as pg
from settings import *
from spaceship import Spaceship
Vec = pg.math.Vector2

pg.init()
window = pg.display.set_mode(SIZE)
clock = pg.time.Clock()
pg.display.set_caption(TITLE)

def draw(bg_image, player):
    window.blit(bg_image, (0, 0))
    window.blit(player.image, (player.pos.x - int(player.image.get_width() / 2), player.pos.y - int(player.image.get_height() / 2)))

    pg.display.update()

def main():
    running = True

    bg_image = pg.transform.scale(pg.image.load(
        join('assets', 'Background', 'Blue_Nebula_01.png')), \
        (WIDTH, HEIGHT))

    player = Spaceship(Vec(WIDTH // 2, HEIGHT // 2))

    while running:
        clock.tick(FPS)
        player.update()
        draw(bg_image, player)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
