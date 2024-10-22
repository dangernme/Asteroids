from os.path import join
from numpy import interp
import pygame as pg
from settings import *

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

            high_score_file = 'high_score.txt'
            try:
                with open(high_score_file, 'r', encoding='utf-8') as file:
                    high_score = int(file.read().strip())
            except FileNotFoundError:
                high_score = 0

            if player.points + bonus_points > high_score:
                high_score = player.points + bonus_points
                with open(high_score_file, 'w', encoding='utf-8') as file:
                    file.write(str(high_score))

            game_over_text = self.large_font.render("Game Over", True, RED)
            points_text = self.large_font.render(f"Points:{player.points} ", True, RED)
            health_text = self.large_font.render(f"Health:{player.health}% Bonus:{bonus_points} ", True, RED)
            total_points_text = self.large_font.render(f"Total Points:{player.points + bonus_points} ", True, RED)
            high_score_text = self.large_font.render(f"High Score:{high_score} ", True, RED)
            surface.blit(game_over_text, (CENTER - game_over_text.get_width() // 2, 200))
            surface.blit(points_text, (CENTER - points_text.get_width() // 2, 300))
            surface.blit(health_text, (CENTER - health_text.get_width() // 2, 400))
            surface.blit(total_points_text, (CENTER - total_points_text.get_width() // 2, 500))
            surface.blit(high_score_text, (CENTER - high_score_text.get_width() // 2, 600))
            pg.draw.rect(surface, (50,50,50), pg.Rect(0,0, TEXT_WIDTH, HEIGHT))
        else:
            # Text area
            pg.draw.rect(surface, (50,50,50), pg.Rect(0,0, TEXT_WIDTH, HEIGHT))
            surface.blit(self.medium_font.render(f"Points {player.points}", True, TEXT_COLOR), (10, 10))
            surface.blit(self.medium_font.render(f"Time {((GAME_TIME / 1000) - pg.time.get_ticks() / 1000) + 0.1:.0f}", True, TEXT_COLOR), (10, 40))
            if player.shield_active:
                surface.blit(self.small_font.render('Shield active', True, RED), (10, 70))
            if player.burst_fire_active:
                surface.blit(self.small_font.render('Burst fire active', True, RED), (10, 90))

            bar_width = int(GAME_WIDTH * 0.5)
            # Health bar
            h_width = int(interp(player.health, [0, 100], [0, bar_width - 4]))
            pg.draw.rect(surface, BLUE, pg.Rect(CENTER - bar_width // 2, 10, bar_width, 20))
            pg.draw.rect(surface, GREEN, pg.Rect(CENTER - (bar_width // 2) + 2, 12, h_width, 16))
            surface.blit(self.small_font.render('Health', True, RED), (CENTER, 10))

            # Munition bar
            h_width = int(interp(player.rockets_amount, [0, 100], [0, bar_width - 4]))
            pg.draw.rect(surface, BLUE, pg.Rect(CENTER - bar_width // 2, HEIGHT - 30, bar_width, 20))
            pg.draw.rect(surface, GREEN, pg.Rect(CENTER - (bar_width // 2) + 2, HEIGHT - 28, h_width, 16))
            surface.blit(self.small_font.render('Rockets', True, RED), (CENTER, HEIGHT - 30))
