import sys
from os.path import join
import random as rd
import pygame as pg
from settings import *
from hud import Hud
from spaceship import Spaceship
from munition import Munition
from asteroid_a1 import AsteroidA1
from asteroid_a3 import AsteroidA3
from asteroid_d3 import AsteroidD3
from medi import Medi
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
        self.screen = pg.display.set_mode(SIZE)

        # General variables
        self.player = Spaceship()
        self.other_sprites = pg.sprite.Group()
        self.active_rockets = pg.sprite.Group()
        self.clock = pg.time.Clock()
        self.bg_image = pg.image.load(join('assets', 'background.png'))
        self.bg_image = pg.transform.scale(self.bg_image, (WIDTH - TEXT_WIDTH, HEIGHT))
        self.game_over = False
        self.muni_amount = 0
        self.medi_amount = 0
        self.hud = Hud()

        if pg.joystick.get_count() == 1:
            self.gamepad = pg.joystick.Joystick(0)
            self.gamepad.init()

        self.init_timers()
        self.init_sound()


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
        self.ding_sound = pg.mixer.Sound(join('assets', 'Sounds', "ding.wav"))
        self.pew_sound = pg.mixer.Sound(join('assets', 'Sounds', "pew.wav"))
        if MUSIC:
            pg.mixer.music.play(-1, 0.0)
            pg.mixer.music.set_volume(0.5)

        self.pew_sound.set_volume(0.1)
        self.crash_sound.set_volume(0.1)
        self.ding_sound.set_volume(0.1)

    def generate_new_asteroid(self, asteroid):
        if ASTEROIDS_RESPAWN:
            random_start = rd.randint(0,4)

            if random_start == 0: # left
                self.other_sprites.add(helpers.generate_asteroid(asteroid, Vec(0, rd.randint(0, HEIGHT))))
            elif random_start == 1: # top
                self.other_sprites.add(helpers.generate_asteroid(asteroid, Vec(rd.randint(TEXT_WIDTH, WIDTH), 0)))
            elif random_start == 2: #right
                self.other_sprites.add(helpers.generate_asteroid(asteroid, Vec(WIDTH, rd.randint(0, HEIGHT))))
            else: #bottom
                self.other_sprites.add(helpers.generate_asteroid(asteroid, Vec(rd.randint(TEXT_WIDTH, WIDTH), HEIGHT)))

    def close(self):
        pg.joystick.quit()
        pg.mixer.quit()
        pg.quit()
        sys.exit()

    def timer_handler(self, events):
        for event in events:
            if event.type == self.rocket_refill_timer:
                self.player.rockets_amount += 1
            if event.type == self.player_heal_timer and self.player.health < 100:
                self.player.health += 1
            if event.type == self.munition_respawn_timer and self.muni_amount < MAX_SPAWNED_MUNITION + MAX_SPAWNED_MEDIS:
                self.other_sprites.add(Munition(Vec(rd.randint(TEXT_WIDTH + 100, WIDTH - 100), rd.randint(100, HEIGHT -100))))
                self.muni_amount +=1
            if event.type == self.medi_respawn_timer and self.medi_amount < MAX_SPAWNED_MEDIS + MAX_SPAWNED_MUNITION:
                self.other_sprites.add(Medi(Vec(rd.randint(TEXT_WIDTH + 100, WIDTH - 100), rd.randint(100, HEIGHT -100))))
                self.medi_amount += 1
            if event.type == self.game_end_timer:
                self.game_over = True

    def input_event_handler(self, events):
        self.player.acceleration = Vec(0, 0)
        keys = pg.key.get_pressed()
        axis_x = self.gamepad.get_axis(0)
        axis_y = self.gamepad.get_axis(1)

        if keys[pg.K_LEFT] or axis_x < -0.5:
            self.player.turn_left()
        if keys[pg.K_RIGHT] or axis_x > 0.5:
            self.player.turn_right()
        if keys[pg.K_UP] or axis_y < -0.5:
            self.player.accelerate()
        if keys[pg.K_DOWN] or axis_y > 0.5:
            self.player.brake()
        else:
            self.player.decelerate()

        for event in events:
            if event.type == pg.QUIT:
                return False

            if not self.game_over:
                if event.type == pg.KEYDOWN and event.key == pg.K_LCTRL:
                    self.fire()
                if event.type == pg.JOYBUTTONDOWN and event.button == BUTTON_A:
                    self.fire()

        return True

    def fire(self):
        if self.player.rockets_amount > 0 and len(self.active_rockets) < MAX_ACTIVE_ROCKETS:
            self.player.rockets_amount -= 1
            self.pew_sound.play()
            self.active_rockets.add(Rocket(self.player.rect.center, self.player.direction.copy()))

    def check_player_collision(self):
        player_collided = pg.sprite.spritecollide(self.player, self.other_sprites, False)
        if player_collided:
            for item in player_collided:
                if isinstance(item, Munition):
                    self.ding_sound.play()
                    if self.player.rockets_amount + item.amount > MAX_SHIP_ROCKETS:
                        self.player.rockets_amount += MAX_SHIP_ROCKETS - self.player.rockets_amount
                    else:
                        self.player.rockets_amount += item.amount

                    self.other_sprites.remove(item)
                    self.muni_amount -= 1

                if isinstance(item, Medi):
                    self.ding_sound.play()
                    if self.player.health + item.health > 100:
                        self.player.health += 100 - self.player.health
                    else:
                        self.player.health += item.health

                    self.other_sprites.remove(item)
                    self.medi_amount -= 1

                if isinstance(item, (AsteroidA1, AsteroidA3, AsteroidD3)):
                    for collided_asteroid in player_collided:
                        self.crash_sound.play()
                        self.generate_new_asteroid(collided_asteroid)
                        self.player.health -= collided_asteroid.damage
                        self.other_sprites.remove(collided_asteroid)

    def chec_rockets_collision(self):
        rocket_collided = pg.sprite.groupcollide(self.active_rockets, self.other_sprites, False, False)
        if rocket_collided:
            for rocket, collided_asteroids in rocket_collided.items():
                for collided_asteroid in collided_asteroids:
                    if isinstance(collided_asteroid, (AsteroidA1, AsteroidA3, AsteroidD3)):
                        self.crash_sound.play()
                        self.generate_new_asteroid(collided_asteroid)
                        self.player.points += collided_asteroid.points
                        self.other_sprites.remove(collided_asteroid)
                        self.active_rockets.remove(rocket)

    def run(self):
        running = True

        for _ in range(NUM_ASTEROIDSA1):
            self.other_sprites.add(AsteroidA1(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))))

        for _ in range(NUM_ASTEROIDSA3):
            self.other_sprites.add(AsteroidA3(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))))

        for _ in range(NUM_ASTEROIDSD3):
            self.other_sprites.add(AsteroidD3(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))))

        while running:
            events = pg.event.get()
            running = self.input_event_handler(events)
            self.timer_handler(events)

            if not self.game_over:
                self.player.update()
                if self.player.health <= 0:
                    self.game_over = True
                self.other_sprites.update()
                self.active_rockets.update()

                for rocket in self.active_rockets:
                    if rocket.pos.x < TEXT_WIDTH or rocket.pos.x > WIDTH or rocket.pos.y < 0 or rocket.pos.y > HEIGHT:
                        self.active_rockets.remove(rocket)

                self.check_player_collision()
                self.chec_rockets_collision()

                self.screen.blit(self.bg_image, (TEXT_WIDTH, 0))
                self.active_rockets.draw(self.screen)
                self.other_sprites.draw(self.screen)
                self.player.draw(self.screen)
                if DEBUG_MODE:
                    for rocket in self.active_rockets:
                        rocket.draw(self.screen)
                    for sprite in self.other_sprites:
                        sprite.draw(self.screen)

            self.hud.draw(self.screen, self.player, self.game_over)

            pg.display.flip()

            self.clock.tick(FPS)

        self.close()
