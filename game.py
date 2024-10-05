import sys
from os.path import join
import random as rd
import pygame as pg
from settings import *
import spaceship
import munition
import asteroid_medium
import asteroid_small
import medi
from rocket import Rocket
import helpers
Vec = pg.math.Vector2

class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        pg.mixer.init()
        pg.mixer.fadeout(10)
        pg.display.set_icon(pg.image.load(join('assets', 'Ships', 'Ship Full health.png')))
        pg.display.set_caption(TITLE)

        # General variables
        self.player = spaceship.Spaceship(Vec(TEXT_WIDTH + GAME_WIDTH // 2, HEIGHT // 2))
        self.all_sprites = pg.sprite.Group()
        self.active_rockets = pg.sprite.Group()
        self.small_font = pg.font.SysFont('Comic Sans MS', SMALL_TEXT_SIZE)
        self.medium_font = pg.font.SysFont('Comic Sans MS', MEDIUM_TEXT_SIZE)
        self.large_font = pg.font.SysFont('Comic Sans MS', LARGE_TEXT_SIZE)
        self.window = pg.display.set_mode(SIZE)
        self.clock = pg.time.Clock()
        self.bg_image = pg.image.load(join('assets', 'background.png'))
        self.bg_image = pg.transform.scale(self.bg_image, (WIDTH - TEXT_WIDTH, HEIGHT))
        self.game_over = False
        self.game_over_sound_played = False
        self.muni_amount = 0
        self.medi_amount = 0

        self.init_timers()
        self.init_sound()
        self.init_gamepad()

    def init_timers(self):
        self.rocket_refill_timer = pg.USEREVENT
        self.player_heal_timer = pg.USEREVENT + 1
        self.munition_respawn_timer = pg.USEREVENT + 2
        self.medi_respawn_timer = pg.USEREVENT + 3
        self.game_end_timer = pg.USEREVENT + 4

        pg.time.set_timer(self.rocket_refill_timer, ROCKET_REFILL_TIME)
        pg.time.set_timer(self.player_heal_timer, PLAYER_REPAIR_TIME)
        pg.time.set_timer(self.munition_respawn_timer, MUNITION_RESPAWN_TIME)
        pg.time.set_timer(self.medi_respawn_timer, MEDI_RESPAWN_TIME)
        pg.time.set_timer(self.game_end_timer, GAME_TIME)

    def init_sound(self):
        pg.mixer.music.load(join('assets', 'Sounds', "space_chase.mp3"))
        self.crash_sound = pg.mixer.Sound(join('assets', 'Sounds', "crash.wav"))
        self.game_over_sound = pg.mixer.Sound(join('assets', 'Sounds', "game_over.wav"))
        self.ding_sound = pg.mixer.Sound(join('assets', 'Sounds', "ding.wav"))
        self.pew_sound = pg.mixer.Sound(join('assets', 'Sounds', "pew.wav"))
        if MUSIC:
            pg.mixer.music.play(-1, 0.0)
            pg.mixer.music.set_volume(0.5)

        self.pew_sound.set_volume(0.1)
        self.crash_sound.set_volume(0.1)
        self.game_over_sound.set_volume(0.6)
        self.ding_sound.set_volume(0.1)

    def draw_hud(self):
        # Text area
        pg.draw.rect(self.window, (50,50,50), pg.Rect(0,0, TEXT_WIDTH, HEIGHT))

        self.window.blit(self.medium_font.render(f"Points {self.player.points}", False, TEXT_COLOR), (10, 10))
        self.window.blit(self.medium_font.render(f"Time {((GAME_TIME / 1000) - pg.time.get_ticks() / 1000) + 0.1:.0f}", False, TEXT_COLOR), (10, 40))

        # Health bar
        bar_width = 700
        h_width = helpers.scale_range(self.player.health, 0, 100, 0, bar_width - 4)
        pg.draw.rect(self.window, BLUE, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - bar_width // 2, 10, bar_width, 20))
        pg.draw.rect(self.window, GREEN, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - (bar_width // 2) + 2, 12, h_width, 16))
        self.window.blit(self.small_font.render('Health', False, RED), (TEXT_WIDTH + (GAME_WIDTH // 2), 10))

        # Munition bar
        h_width = helpers.scale_range(self.player.rockets_amount, 0, MAX_SHIP_ROCKETS, 0, bar_width - 4)
        pg.draw.rect(self.window, BLUE, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - bar_width // 2, HEIGHT - 30, bar_width, 20))
        pg.draw.rect(self.window, GREEN, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - (bar_width // 2) + 2, HEIGHT - 28, h_width, 16))
        self.window.blit(self.small_font.render('Rockets', False, RED), (TEXT_WIDTH + (GAME_WIDTH // 2), HEIGHT - 30))

    def generate_new_asteroid(self, asteroid):
        if ASTEROIDS_RESPAWN:
            random_start = rd.randint(0,4)

            if random_start == 0: # left
                self.all_sprites.add(helpers.generate_asteroid(asteroid, Vec(0, rd.randint(0, HEIGHT))))
            elif random_start == 1: # top
                self.all_sprites.add(helpers.generate_asteroid(asteroid, Vec(rd.randint(TEXT_WIDTH, WIDTH), 0)))
            elif random_start == 2: #right
                self.all_sprites.add(helpers.generate_asteroid(asteroid, Vec(WIDTH, rd.randint(0, HEIGHT))))
            else: #bottom
                self.all_sprites.add(helpers.generate_asteroid(asteroid, Vec(rd.randint(TEXT_WIDTH, WIDTH), HEIGHT)))

    def handle_game_over(self, player):
        pg.mixer.music.stop()
        if not self.game_over_sound_played:
            self.game_over_sound.play()
            self.game_over_sound_played = True
        bonus_points = player.health // 15
        self.window.blit(self.large_font.render("Game Over", False, RED), (500, 200))
        self.window.blit(self.large_font.render(f"Points:{player.points} ", False, RED), (540, 300))
        self.window.blit(self.large_font.render(f"Health:{player.health} Bonus:{bonus_points} ", False, RED), (300, 400))
        self.window.blit(self.large_font.render(f"Total Points:{player.points + bonus_points} ", False, RED), (420, 500))

    def init_gamepad(self):
        if pg.joystick.get_count() == 1:
            gamepad = pg.joystick.Joystick(0)
            gamepad.init()

    def close(self):
        pg.joystick.quit()
        pg.mixer.quit()
        pg.quit()
        sys.exit()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            # Fire rocket
            if (event.type == pg.KEYDOWN and event.key == pg.K_LCTRL) or (event.type == pg.JOYBUTTONDOWN and event.button == BUTTON_A):
                if self.player.rockets_amount > 0 and len(self.active_rockets) < MAX_ACTIVE_ROCKETS:
                    self.player.rockets_amount -= 1
                    self.pew_sound.play()
                    self.active_rockets.add(Rocket(self.player.pos.copy(), self.player.direction.copy()))

            if event.type == self.rocket_refill_timer:
                self.player.rockets_amount += 1
            if event.type == self.player_heal_timer and self.player.health < 100:
                self.player.health += 1
            if event.type == self.munition_respawn_timer and self.muni_amount < MAX_SPAWNED_MUNITION + MAX_SPAWNED_MEDIS:
                self.all_sprites.add(munition.Munition(Vec(rd.randint(TEXT_WIDTH + 100, WIDTH - 100), rd.randint(100, HEIGHT -100))))
                self.muni_amount +=1
            if event.type == self.medi_respawn_timer and self.medi_amount < MAX_SPAWNED_MEDIS + MAX_SPAWNED_MUNITION:
                self.all_sprites.add(medi.Medi(Vec(rd.randint(TEXT_WIDTH + 100, WIDTH - 100), rd.randint(100, HEIGHT -100))))
                self.medi_amount += 1
            if event.type == self.game_end_timer:
                self.game_over = True

        return True

    def run(self):
        running = True

        for _ in range(NUM_MEDIUM_ASTEROIDS):
            self.all_sprites.add(asteroid_medium.Asteroid1(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))))

        for _ in range(NUM_SMALL_ASTEROIDS):
            self.all_sprites.add(asteroid_small.Asteroid3(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))))

        while running:
            if self.game_over:
                self.handle_game_over(self.player)

            running = self.event_handler()

            self.player.update()
            if self.player.health <= 0:
                self.game_over = True
            self.all_sprites.update()
            self.active_rockets.update()

            for rocket in self.active_rockets:
                if rocket.pos.x < TEXT_WIDTH or rocket.pos.x > WIDTH or rocket.pos.y < 0 or rocket.pos.y > HEIGHT:
                    self.active_rockets.remove(rocket)

            player_collided = pg.sprite.spritecollide(self.player, self.all_sprites, False)
            if player_collided:
                for item in player_collided:
                    if isinstance(item, munition.Munition):
                        self.ding_sound.play()
                        if self.player.rockets_amount + item.amount > MAX_SHIP_ROCKETS:
                            self.player.rockets_amount += MAX_SHIP_ROCKETS - self.player.rockets_amount
                        else:
                            self.player.rockets_amount += item.amount

                        self.all_sprites.remove(item)
                        self.muni_amount -= 1

                    if isinstance(item, medi.Medi):
                        self.ding_sound.play()
                        if self.player.health + item.healh > 100:
                            self.player.health += 100 - self.player.health
                        else:
                            self.player.health += item.healh

                        self.all_sprites.remove(item)
                        self.medi_amount -= 1

            rocket_collided = pg.sprite.groupcollide(self.active_rockets, self.all_sprites, True, True)
            if rocket_collided:
                for item in rocket_collided:
                    if isinstance(item, (asteroid_medium.Asteroid1, asteroid_small.Asteroid3)):
                        self.crash_sound.play()
                        self.generate_new_asteroid(item)
                        self.player.points += 1


            self.window.blit(self.bg_image, (TEXT_WIDTH, 0))
            self.all_sprites.draw(self.window)
            self.player.draw(self.window)
            self.active_rockets.draw(self.window)
            self.draw_hud()

            pg.display.flip()

            self.clock.tick(FPS)

        self.close()
