from os.path import join
import pygame as pg
from settings import *
import helpers

class Hud():
    def __init__(self):
        self.small_font = pg.font.SysFont('Comic Sans MS', SMALL_TEXT_SIZE)
        self.medium_font = pg.font.SysFont('Comic Sans MS', MEDIUM_TEXT_SIZE)
        self.large_font = pg.font.SysFont('Comic Sans MS', LARGE_TEXT_SIZE)
        self.game_over_sound = pg.mixer.Sound(join('assets', 'Sounds', "game_over.wav"))
        self.game_over_sound.set_volume(0.6)
        self.game_over_sound_played = False

    def draw(self, surface, player, game_over):
        if game_over:
            if not self.game_over_sound_played:
                pg.mixer.music.stop()
                self.game_over_sound.play()
                self.game_over_sound_played = True
            bonus_points = player.health // 15
            surface.blit(self.large_font.render("Game Over", True, RED), (500, 200))
            surface.blit(self.large_font.render(f"Points:{player.points} ", True, RED), (540, 300))
            surface.blit(self.large_font.render(f"Health:{player.health} Bonus:{bonus_points} ", True, RED), (300, 400))
            surface.blit(self.large_font.render(f"Total Points:{player.points + bonus_points} ", True, RED), (420, 500))
            pg.draw.rect(surface, (50,50,50), pg.Rect(0,0, TEXT_WIDTH, HEIGHT))
        else:
            # Text area
            pg.draw.rect(surface, (50,50,50), pg.Rect(0,0, TEXT_WIDTH, HEIGHT))
            surface.blit(self.medium_font.render(f"Points {player.points}", True, TEXT_COLOR), (10, 10))
            surface.blit(self.medium_font.render(f"Time {((GAME_TIME / 1000) - pg.time.get_ticks() / 1000) + 0.1:.0f}", True, TEXT_COLOR), (10, 40))

            bar_width = int(GAME_WIDTH * 0.5)
            # Health bar
            h_width = int(helpers.interp(player.health, [0, 100], [0, bar_width - 4]))
            pg.draw.rect(surface, BLUE, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - bar_width // 2, 10, bar_width, 20))
            pg.draw.rect(surface, GREEN, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - (bar_width // 2) + 2, 12, h_width, 16))
            surface.blit(self.small_font.render('Health', True, RED), (TEXT_WIDTH + (GAME_WIDTH // 2), 10))

            # Munition bar
            h_width = int(helpers.interp(player.rockets_amount, [0, 100], [0, bar_width - 4]))
            pg.draw.rect(surface, BLUE, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - bar_width // 2, HEIGHT - 30, bar_width, 20))
            pg.draw.rect(surface, GREEN, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - (bar_width // 2) + 2, HEIGHT - 28, h_width, 16))
            surface.blit(self.small_font.render('Rockets', True, RED), (TEXT_WIDTH + (GAME_WIDTH // 2), HEIGHT - 30))
