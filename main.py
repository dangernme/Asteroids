import sys
from os.path import join
import pygame as pg
from settings import *
from spaceship import Spaceship
from asteroid import Asteroid
Vec = pg.math.Vector2
import random as rd

# TODO
# Collition circle of player ship is still outside of the ship

pg.init()
pg.font.init()
pg.joystick.init()
font = pg.font.SysFont('Comic Sans MS', TEXT_SIZE)
window = pg.display.set_mode(SIZE)
clock = pg.time.Clock()
pg.display.set_caption(TITLE)

rocket_refill_timer = pg.USEREVENT
player_repair_timer = pg.USEREVENT + 1

def draw(bg_image, player, active_rockets, asteroids):
    window.blit(bg_image, (TEXT_WIDTH, 0)) # Draw background
    
    player.draw()
    
    for rocket in active_rockets:
        rocket.draw()
    
    for asteroid in asteroids: 
        asteroid.draw()
    
    # Draw text area    
    pg.draw.rect(window, (50,50,50), pg.Rect(0,0, TEXT_WIDTH, HEIGHT))
                    
    window.blit(font.render(f"Max Speed {player.speed * 100:.0f}", False, TEXT_COLOR), (10, 5))
    window.blit(font.render(f"Health {player.health} %", False, TEXT_COLOR), (10, 35))
    
    if player.rockets == 0:
        window.blit(font.render(f"Rockets {player.rockets}", False, RED), (10, 65))
    else:
        window.blit(font.render(f"Rockets {player.rockets}", False, TEXT_COLOR), (10, 65))
        
    window.blit(font.render(f"Points {player.points}", False, TEXT_COLOR), (10, 95))
    pg.display.update()
    
def generate_new_asteroid(asteroids):
    random_start = rd.randint(0,4)
    if random_start == 0: # left
        asteroids.append(Asteroid(Vec(0, rd.randint(0, HEIGHT))))
    elif random_start == 1: # top
        asteroids.append(Asteroid(Vec(rd.randint(TEXT_WIDTH, WIDTH), 0)))
    elif(random_start == 2): #right
        asteroids.append(Asteroid(Vec(WIDTH, rd.randint(0, HEIGHT))))
    else: #bottom
        asteroids.append(Asteroid(Vec(rd.randint(TEXT_WIDTH, WIDTH), HEIGHT)))
    
def handle_asteroids(asteroids, player):
    for active_rocket in player.active_rockets:        
        for asteroid in asteroids:
            if pg.sprite.collide_circle(active_rocket, asteroid):
                asteroids.remove(asteroid)
                player.active_rockets.remove(active_rocket)
                player.points += 1
                generate_new_asteroid(asteroids)
                
def main():
    running = True
    pg.time.set_timer(rocket_refill_timer, ROCKET_REFILL_TIME)
    pg.time.set_timer(player_repair_timer, PLAYER_REPAIR_TIME)

    gamepad = pg.joystick.Joystick(0)
    gamepad.init()
    bg_image = pg.transform.scale(pg.image.load(join('assets', 'Background', 'Blue_Nebula_01.png')), \
        (WIDTH - TEXT_WIDTH, HEIGHT))
    
    player = Spaceship(Vec(TEXT_WIDTH + GAME_WIDTH // 2, HEIGHT // 2))
    asteroids = [Asteroid(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))),
                 Asteroid(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))),
                 Asteroid(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT))),
                 Asteroid(Vec(rd.randint(TEXT_WIDTH, WIDTH), rd.randint(0, HEIGHT)))]
        
    while running:
        clock.tick(FPS)
             
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
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

        player.update()
                
        for asteroid in asteroids:
            asteroid.update()
            if pg.sprite.collide_circle(player, asteroid):
                asteroids.remove(asteroid)
                player.health -= 10
                generate_new_asteroid(asteroids)
         
            
        for active_rocket in player.active_rockets:
            active_rocket.update()
            if active_rocket.pos.x < TEXT_WIDTH or active_rocket.pos.x > WIDTH or active_rocket.pos.y < 0 or active_rocket.pos.y > HEIGHT:
                player.active_rockets.remove(active_rocket)
        
        handle_asteroids(asteroids, player)
           
        draw(bg_image, player, player.active_rockets, asteroids)
        
    pg.joystick.quit()
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
