import sys
from os.path import join
import logging
import pygame as pg
from settings import *
import spaceship
import munition
import asteroid_medium
import asteroid_small
import medi
Vec = pg.math.Vector2
import random as rd
import helpers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='asteroids.log', filemode='w', level=logging.DEBUG)

pg.init()
pg.font.init()
pg.mixer.init()
pg.display.set_icon(pg.image.load(join('assets', 'Ships', 'Ship Full health.png')))
pg.display.set_caption(TITLE)

# General variables
small_font = pg.font.SysFont('Comic Sans MS', SMALL_TEXT_SIZE)
medium_font = pg.font.SysFont('Comic Sans MS', MEDIUM_TEXT_SIZE)
large_font = pg.font.SysFont('Comic Sans MS', LARGE_TEXT_SIZE)
window = pg.display.set_mode(SIZE)
clock = pg.time.Clock()
bg_image = pg.image.load(join('assets', 'background.png'))
bg_image = pg.transform.scale(bg_image, (WIDTH - TEXT_WIDTH, HEIGHT))
game_over = False
game_over_sound_played = False

# Timers
rocket_refill_timer = pg.USEREVENT
player_repair_timer = pg.USEREVENT + 1
munition_respawn_timer = pg.USEREVENT + 2
medi_respawn_timer = pg.USEREVENT + 3
game_end_timer = pg.USEREVENT + 4

pg.time.set_timer(rocket_refill_timer, ROCKET_REFILL_TIME)
pg.time.set_timer(player_repair_timer, PLAYER_REPAIR_TIME)
pg.time.set_timer(munition_respawn_timer, MUNITION_RESPAWN_TIME)
pg.time.set_timer(medi_respawn_timer, MEDI_RESPAWN_TIME)
pg.time.set_timer(game_end_timer, GAME_TIME)

# Sound
pg.mixer.music.load(join('assets', 'Sounds', "space_chase.mp3"))
pg.mixer.music.play(-1, 0.0)
pg.mixer.music.set_volume(0.5)
crash_sound = pg.mixer.Sound(join('assets', 'Sounds', "crash.wav"))
crash_sound.set_volume(0.1)
game_over_sound = pg.mixer.Sound(join('assets', 'Sounds', "game_over.wav"))
game_over_sound.set_volume(0.6)

def update(player, asteroids):
    global game_over
    player.update()
    if player.health <= 0:
        game_over = True
        
    for active_rocket in player.active_rockets:
        active_rocket.update()
        if active_rocket.pos.x < TEXT_WIDTH or active_rocket.pos.x > WIDTH or active_rocket.pos.y < 0 or active_rocket.pos.y > HEIGHT:
            player.active_rockets.remove(active_rocket)
            
    handle_asteroids(asteroids, player, crash_sound)
    if len(asteroids) == 0:
        game_over = True
    
    
def draw(player, active_rockets, asteroids, spawned_munition, spawed_medis):
    window.blit(bg_image, (TEXT_WIDTH, 0))
    
    player.draw()
    
    for rocket in active_rockets:
        rocket.draw()
    
    for asteroid in asteroids: 
        asteroid.draw()
        
    for munition in spawned_munition:
        munition.draw()
        
    for medis in spawed_medis:
        medis.draw()
    
    # Text area    
    pg.draw.rect(window, (50,50,50), pg.Rect(0,0, TEXT_WIDTH, HEIGHT))
                            
    window.blit(medium_font.render(f"Points {player.points}", False, TEXT_COLOR), (10, 10))
    window.blit(medium_font.render(f"Time {((GAME_TIME / 1000) - pg.time.get_ticks() / 1000) + 0.1:.0f}", False, TEXT_COLOR), (10, 40))

    # Health bar    
    bar_width = 700
    h_width = helpers.scale_range(player.health, 0, 100, 0, bar_width - 4)
    pg.draw.rect(window, BLUE, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - bar_width // 2, 10, bar_width, 20)) 
    pg.draw.rect(window, GREEN, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - (bar_width // 2) + 2, 12, h_width, 16)) 
    window.blit(small_font.render(f"Health", False, RED), (TEXT_WIDTH + (GAME_WIDTH // 2), 10))
    
    # Munition bar
    h_width = helpers.scale_range(player.rockets, 0, MAX_SHIP_ROCKETS, 0, bar_width - 4)
    pg.draw.rect(window, BLUE, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - bar_width // 2, HEIGHT - 30, bar_width, 20)) 
    pg.draw.rect(window, GREEN, pg.Rect(TEXT_WIDTH + (GAME_WIDTH // 2) - (bar_width // 2) + 2, HEIGHT - 28, h_width, 16)) 
    window.blit(small_font.render(f"Rockets", False, RED), (TEXT_WIDTH + (GAME_WIDTH // 2), HEIGHT - 30))
        
    pg.display.update()
        
def generate_new_asteroid(asteroids, asteroid):
    if ASTEROIDS_RESPAWN:
        random_start = rd.randint(0,4)

        if random_start == 0: # left
            asteroids.append(helpers.generate_asteroid(asteroid, Vec(0, rd.randint(0, HEIGHT))))
        elif random_start == 1: # top
            asteroids.append(helpers.generate_asteroid(asteroid, Vec(rd.randint(TEXT_WIDTH, WIDTH), 0)))
        elif(random_start == 2): #right
            asteroids.append(helpers.generate_asteroid(asteroid, Vec(WIDTH, rd.randint(0, HEIGHT))))
        else: #bottom
            asteroids.append(helpers.generate_asteroid(asteroid, Vec(rd.randint(TEXT_WIDTH, WIDTH), HEIGHT)))
    
def handle_asteroids(asteroids, player, crash_sound):
    for active_rocket in player.active_rockets:        
        for asteroid in asteroids:
            if pg.sprite.collide_circle(active_rocket, asteroid):
                logging.info(f"Rocket hit asteroid at {active_rocket.pos}")
                crash_sound.play()
                generate_new_asteroid(asteroids, asteroid)
                asteroids.remove(asteroid)
                player.active_rockets.remove(active_rocket)
                player.points += 1
                
    for asteroid in asteroids:
        asteroid.update()
        if pg.sprite.collide_circle(player, asteroid):
            logging.info(f"Player hit asteroid at {player.pos}")
            crash_sound.play()
            asteroids.remove(asteroid)
            player.health -= asteroid.damage
            generate_new_asteroid(asteroids, asteroid)
      
def handle_game_over(player):
    global game_over_sound_played
    
    pg.mixer.music.stop()
    if not game_over_sound_played:
        logging.info(f"Game over")
        game_over_sound.play()
        game_over_sound_played = True
    bonus_points = player.health // 15
    window.blit(large_font.render(f"Game Over", False, RED), (500, 200))
    window.blit(large_font.render(f"Points:{player.points} ", False, RED), (540, 300))
    window.blit(large_font.render(f"Health:{player.health} Bonus:{bonus_points} ", False, RED), (300, 400))
    window.blit(large_font.render(f"Total Points:{player.points + bonus_points} ", False, RED), (420, 500))
    pg.display.update()    
    
def main():
    global game_over
    running = True

    # Sound
    pg.mixer.fadeout(10)
    ding_sound = pg.mixer.Sound(join('assets', 'Sounds', "ding.wav"))
    ding_sound.set_volume(0.1)

    if pg.joystick.get_count() == 1:
        logging.info("Gamepad detected")
        gamepad = pg.joystick.Joystick(0)
        gamepad.init()

    
    player = spaceship.Spaceship(Vec(TEXT_WIDTH + GAME_WIDTH // 2, HEIGHT // 2))
    asteroids = []
    spawned_munition = []
    spawned_medis = []
    
    for _ in range(NUM_MEDIUM_ASTEROIDS):
        asteroids.append(asteroid_medium.Asteroid_Medium(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))))
        
    for _ in range(NUM_SMALL_ASTEROIDS):
        asteroids.append(asteroid_small.Asteroid_Small(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))))
        
    while running:             
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            if not game_over: 
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LCTRL:
                        player.fire()
                if event.type == pg.JOYBUTTONDOWN:
                    if event.button == BUTTON_A:
                        player.fire()
                if event.type == rocket_refill_timer:
                    player.rockets += 1
                if event.type == player_repair_timer and player.health < 100:
                    player.health += 1
                if event.type == munition_respawn_timer and len(spawned_munition) < MAX_SPAWNED_MUNITION:
                    spawned_munition.append(munition.Munition(Vec(rd.randint(TEXT_WIDTH + 100, WIDTH - 100), rd.randint(100, HEIGHT -100))))
                if event.type == medi_respawn_timer and len(spawned_medis) < MAX_SPAWNED_MEDIS:
                    spawned_medis.append(medi.Medi(Vec(rd.randint(TEXT_WIDTH + 100, WIDTH - 100), rd.randint(100, HEIGHT -100))))
                if event.type == game_end_timer:
                    game_over = True
                
        if not game_over:  
            update(player, asteroids)

            for muni in spawned_munition:
                if pg.sprite.collide_circle(player, muni):
                    ding_sound.play()
                    logging.info(f"Munition collected at {player.pos}")
                    if player.rockets + muni.amount > MAX_SHIP_ROCKETS:
                        player.rockets += MAX_SHIP_ROCKETS - player.rockets
                    else:
                        player.rockets += muni.amount
                        spawned_munition.remove(muni)
                        
            for medis in spawned_medis:
                if pg.sprite.collide_circle(player, medis):
                    ding_sound.play()
                    logging.info(f"Medis collected at {player.pos}")
                    if player.health + medis.healh > 100:
                        player.health += 100 - player.health
                    else:
                        player.health += medis.healh
                        spawned_medis.remove(medis)
            
            draw(player, player.active_rockets, asteroids, spawned_munition, spawned_medis)
            
        else:
            handle_game_over(player)

        clock.tick(FPS) 
        
    pg.joystick.quit()
    pg.mixer.quit()
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
