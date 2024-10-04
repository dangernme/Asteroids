import sys
from os.path import join
import random as rd
import logging
import pygame as pg
from settings import *
import spaceship
import munition
import asteroid_medium
import asteroid_small
import medi
import helpers
Vec = pg.math.Vector2

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='asteroids.log', filemode='w', level=logging.DEBUG)
class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        pg.mixer.init()
        pg.mixer.fadeout(10)
        pg.display.set_icon(pg.image.load(join('assets', 'Ships', 'Ship Full health.png')))
        pg.display.set_caption(TITLE)

        # General variables
        self.small_font = pg.font.SysFont('Comic Sans MS', SMALL_TEXT_SIZE)
        self.medium_font = pg.font.SysFont('Comic Sans MS', MEDIUM_TEXT_SIZE)
        self.large_font = pg.font.SysFont('Comic Sans MS', LARGE_TEXT_SIZE)
        self.window = pg.display.set_mode(SIZE)
        self.clock = pg.time.Clock()
        self.bg_image = pg.image.load(join('assets', 'background.png'))
        self.bg_image = pg.transform.scale(self.bg_image, (WIDTH - TEXT_WIDTH, HEIGHT))
        self.game_over = False
        self.game_over_sound_played = False

        # Timers
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

        # Sound
        if MUSIC:
            pg.mixer.music.load(join('assets', 'Sounds', "space_chase.mp3"))
            pg.mixer.music.play(-1, 0.0)
            pg.mixer.music.set_volume(0.5)
        self.crash_sound = pg.mixer.Sound(join('assets', 'Sounds', "crash.wav"))
        self.crash_sound.set_volume(0.1)
        self.game_over_sound = pg.mixer.Sound(join('assets', 'Sounds', "game_over.wav"))
        self.game_over_sound.set_volume(0.6)
        self.ding_sound = pg.mixer.Sound(join('assets', 'Sounds', "ding.wav"))
        self.ding_sound.set_volume(0.1)

    def update(self, player, asteroids):
        player.update()
        if player.health <= 0:
            self.game_over = True

        for active_rocket in player.active_rockets:
            active_rocket.update()
            if active_rocket.pos.x < TEXT_WIDTH or active_rocket.pos.x > WIDTH or active_rocket.pos.y < 0 or active_rocket.pos.y > HEIGHT:
                player.active_rockets.remove(active_rocket)

        self.handle_asteroids(asteroids, player, self.crash_sound)
        if len(asteroids) == 0:
            self.game_over = True


    def draw(self, player, active_rockets, asteroids, spawned_munition, spawed_medis):
        self.window.blit(self.bg_image, (TEXT_WIDTH, 0))

        player.draw()

        for rocket in active_rockets:
            rocket.draw()

        for asteroid in asteroids:
            asteroid.draw()

        for muni in spawned_munition:
            muni.draw()

        for medis in spawed_medis:
            medis.draw()

        # Text area
        pg.draw.rect(self.window, (50,50,50), pg.Rect(0,0, TEXT_WIDTH, HEIGHT))

        self.window.blit(self.medium_font.render(f"Points {player.points}", False, TEXT_COLOR), (10, 10))
        self.window.blit(self.medium_font.render(f"Time {((GAME_TIME / 1000) - pg.time.get_ticks() / 1000) + 0.1:.0f}", False, TEXT_COLOR), (10, 40))

        # Health bar
        bar_width = 700
        h_width = helpers.scale_range(player.health, 0, 100, 0, bar_width - 4)
        pg.draw.rect(self.window, BLUE, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - bar_width // 2, 10, bar_width, 20))
        pg.draw.rect(self.window, GREEN, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - (bar_width // 2) + 2, 12, h_width, 16))
        self.window.blit(self.small_font.render('Health', False, RED), (TEXT_WIDTH + (GAME_WIDTH // 2), 10))

        # Munition bar
        h_width = helpers.scale_range(player.rockets, 0, MAX_SHIP_ROCKETS, 0, bar_width - 4)
        pg.draw.rect(self.window, BLUE, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - bar_width // 2, HEIGHT - 30, bar_width, 20))
        pg.draw.rect(self.window, GREEN, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - (bar_width // 2) + 2, HEIGHT - 28, h_width, 16))
        self.window.blit(self.small_font.render('Rockets', False, RED), (TEXT_WIDTH + (GAME_WIDTH // 2), HEIGHT - 30))

        pg.display.update()

    def generate_new_asteroid(self, asteroids, asteroid):
        if ASTEROIDS_RESPAWN:
            random_start = rd.randint(0,4)

            if random_start == 0: # left
                asteroids.append(helpers.generate_asteroid(asteroid, Vec(0, rd.randint(0, HEIGHT))))
            elif random_start == 1: # top
                asteroids.append(helpers.generate_asteroid(asteroid, Vec(rd.randint(TEXT_WIDTH, WIDTH), 0)))
            elif random_start == 2: #right
                asteroids.append(helpers.generate_asteroid(asteroid, Vec(WIDTH, rd.randint(0, HEIGHT))))
            else: #bottom
                asteroids.append(helpers.generate_asteroid(asteroid, Vec(rd.randint(TEXT_WIDTH, WIDTH), HEIGHT)))

    def handle_asteroids(self, asteroids, player, _crash_sound):
        for active_rocket in player.active_rockets:
            for asteroid in asteroids:
                if pg.sprite.collide_circle(active_rocket, asteroid):
                    logging.info('Rocket hit asteroid at %s', active_rocket.pos)
                    _crash_sound.play()
                    self.generate_new_asteroid(asteroids, asteroid)
                    asteroids.remove(asteroid)
                    player.active_rockets.remove(active_rocket)
                    player.points += 1

        for asteroid in asteroids:
            asteroid.update()
            if pg.sprite.collide_circle(player, asteroid):
                logging.info('Player hit asteroid at %s', player.pos)
                _crash_sound.play()
                asteroids.remove(asteroid)
                player.health -= asteroid.damage
                self.generate_new_asteroid(asteroids, asteroid)

    def handle_game_over(self, player):
        pg.mixer.music.stop()
        if not self.game_over_sound_played:
            logging.info("Game over")
            self.game_over_sound.play()
            self.game_over_sound_played = True
        bonus_points = player.health // 15
        self.window.blit(self.large_font.render("Game Over", False, RED), (500, 200))
        self.window.blit(self.large_font.render(f"Points:{player.points} ", False, RED), (540, 300))
        self.window.blit(self.large_font.render(f"Health:{player.health} Bonus:{bonus_points} ", False, RED), (300, 400))
        self.window.blit(self.large_font.render(f"Total Points:{player.points + bonus_points} ", False, RED), (420, 500))
        pg.display.update()

    def init_gamepad(self):
        if pg.joystick.get_count() == 1:
            logging.info("Gamepad detected")
            gamepad = pg.joystick.Joystick(0)
            gamepad.init()

    def close(self):
        pg.joystick.quit()
        pg.mixer.quit()
        pg.quit()
        sys.exit()

    def run(self):
        running = True

        self.init_gamepad()

        player = spaceship.Spaceship(Vec(TEXT_WIDTH + GAME_WIDTH // 2, HEIGHT // 2))
        asteroids = []
        spawned_munition = []
        spawned_medis = []

        for _ in range(NUM_MEDIUM_ASTEROIDS):
            asteroids.append(asteroid_medium.AsteroidMedium(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))))

        for _ in range(NUM_SMALL_ASTEROIDS):
            asteroids.append(asteroid_small.AsteroidSmall(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))))

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    break
                if not self.game_over:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_LCTRL:
                            player.fire()
                    if event.type == pg.JOYBUTTONDOWN:
                        if event.button == BUTTON_A:
                            player.fire()
                    if event.type == self.rocket_refill_timer:
                        player.rockets += 1
                    if event.type == self.player_heal_timer and player.health < 100:
                        player.health += 1
                    if event.type == self.munition_respawn_timer and len(spawned_munition) < MAX_SPAWNED_MUNITION:
                        spawned_munition.append(munition.Munition(Vec(rd.randint(TEXT_WIDTH + 100, WIDTH - 100), rd.randint(100, HEIGHT -100))))
                    if event.type == self.medi_respawn_timer and len(spawned_medis) < MAX_SPAWNED_MEDIS:
                        spawned_medis.append(medi.Medi(Vec(rd.randint(TEXT_WIDTH + 100, WIDTH - 100), rd.randint(100, HEIGHT -100))))
                    if event.type == self.game_end_timer:
                        self.game_over = True

            if not self.game_over:
                self.update(player, asteroids)

                for muni in spawned_munition.copy():
                    if pg.sprite.collide_circle(player, muni):
                        self.ding_sound.play()
                        logging.info("Munition collected at %s", player.pos)
                        if player.rockets + muni.amount > MAX_SHIP_ROCKETS:
                            player.rockets += MAX_SHIP_ROCKETS - player.rockets
                        else:
                            player.rockets += muni.amount
                            spawned_munition.remove(muni)

                for medis in spawned_medis.copy():
                    if pg.sprite.collide_circle(player, medis):
                        self.ding_sound.play()
                        logging.info("Medis collected at %s", player.pos)
                        if player.health + medis.healh > 100:
                            player.health += 100 - player.health
                        else:
                            player.health += medis.healh
                            spawned_medis.remove(medis)

                self.draw(player, player.active_rockets, asteroids, spawned_munition, spawned_medis)

            else:
                self.handle_game_over(player)

            self.clock.tick(FPS)
        self.close()
