import pygame
from pygame import Surface
from typing import List
from sys import exit
from ship import Ship
from sprite import Sprite

import random
from utils import *

import asyncio

pygame.init()

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

frame: Surface = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
# frame: Surface = pygame.display.set_mode((WIDTH,HEIGHT))
# frame: Surface = pygame.display.set_mode((WIDTH,HEIGHT), pygame.DOUBLEBUF, 32)

from assets import *

COORDINATE = List[int]
SIZE= COORDINATE

pygame.mixer.music.load(soundtrack_path)
clock = pygame.time.Clock()

# key handlers to control ship   
def keydown(event):
    if event.key == pygame.K_LEFT:
        my_ship.decrement_angle_vel()
    elif event.key == pygame.K_RIGHT:
        my_ship.increment_angle_vel()
    elif event.key == pygame.K_UP:
        my_ship.set_thrust(True, ship_thrust_sound)
    elif event.key == pygame.K_SPACE:
        missile_details = my_ship.shoot(missile_info)
        missile_group.add(Sprite(missile_details.position, missile_details.velocity, missile_details.angle, missile_details.angle_velocity, missile_image, missile_info, missile_sound))
        
def keyup(event):
    if event.key == pygame.K_LEFT:
        my_ship.increment_angle_vel()
    elif event.key == pygame.K_RIGHT:
        my_ship.decrement_angle_vel()
    elif event.key == pygame.K_UP:
        my_ship.set_thrust(False, ship_thrust_sound)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    
    if started:
        return
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if inwidth and inheight:
        started = True
        lives = 3
        score = 0
        pygame.mixer.music.play(loops=-1, fade_ms=500)
        

text = pygame.font.SysFont("arial", 22)

# @timer_decorator
def draw(frame: Surface): 
    global time, started, lives, score, rock_group
    
    # animate background
    time += 1
    wtime = (time * .25) % WIDTH
    frame.blit(nebula_image, (0,0))
    
    
    # Create continuous debris background
    frame.blit(debris_image, (wtime - WIDTH, 0) )
    frame.blit(debris_image, (wtime , 0))
   
    
    # draw UI
    frame.blit(text.render('Lives', True, (255,255,255)),(50,50))
    frame.blit(text.render("Score", True, (255,255,255)),(680,50))
    frame.blit(text.render(str(lives), True, (255,255,255)),(50,80))
    frame.blit(text.render(str(score), True, (255,255,255)),(680,80))
    
    # update ship and sprites
    my_ship.update()
    # draw ship and sprites
    frame.blit(*my_ship.draw())

    process_sprite_group(rock_group, frame)
    process_sprite_group(missile_group, frame)
    process_sprite_group(explosion_group, frame)
    score += rock_missile_group_collide(missile_group, rock_group)

    if group_collide(rock_group, my_ship):
        lives -= 1

    # draw splash screen if not started
    if not started:
        frame.blit(splash_image,
                        (
                            (WIDTH - splash_info.get_size()[0]) * .5,
                            (HEIGHT - splash_info.get_size()[1]) * .5
                        )
                    )
    
    if lives == 0:
        started = False
        rock_group = set()
        pygame.mixer.music.fadeout(1500)


#process sprite group helper function
def process_sprite_group(the_set: set[Sprite], canvas: Surface):
    for the_object in the_set.copy():
        canvas.blit(*the_object.draw())   
        if the_object.update():
            the_set.discard(the_object)
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if len(rock_group) <= 2:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [
            random.random() * .6 - .3, 
            random.random() * .6 - .3
            ]
        rock_avel = random.random() * .2 - .1
        new_asteroid_image = asteroid_image.subsurface((0, 0, *asteroid_image.get_size()))
        new_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, new_asteroid_image, asteroid_info)
        if dist(new_rock.pos, my_ship.pos) > 100:
            rock_group.add(new_rock)
        else:
            rock_spawner()
        
        
def group_collide(group, other_object):
    for obj in set(group):
        if obj.collide(other_object):
            group.discard(obj)
            centered_explosion_pos = [other_object.pos_center[0] - explosion_info.get_center()[0], other_object.pos_center[1] - explosion_info.get_center()[1]]
            explosion_group.add(Sprite(centered_explosion_pos, other_object.vel, 0, 0, explosion_image, explosion_info, explosion_sound))
            return True
    return False

def rock_missile_group_collide(missile_group, rock_group):
    number = 0
    for rock in set(rock_group):
        if group_collide(missile_group, rock):
            rock_group.discard(rock)
            number += 1
    return number


# initialize ship and sprites

SPAWN_ROCK_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ROCK_EVENT, 2000)

my_ship = Ship([int(WIDTH * .5), int(HEIGHT * .5)], [0.0, 0.0], 0, ship_image_inactive, ship_image_active, ship_info)

rock_group: set[Sprite] = set()
missile_group: set[Sprite] = set()
explosion_group: set[Sprite] = set()

    
# Define the dimensions of each item

item_width,item_height = explosion_info.get_size()
# Create a variable to keep track of the current item index
random_explosion_pos = 0


async def main():

    global random_explosion_pos

    while True:
        # start_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                keydown(event)
            elif event.type == pygame.KEYUP:
                keyup(event)   
            elif event.type == SPAWN_ROCK_EVENT and started: # TODO: stop the timer
                rock_spawner()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                click(pos)

        draw(frame)

        # Draw random explosion
        # TODO: Organize this better
        explosion_image_frame = explosion_image.subsurface(
            (random_explosion_pos * (item_width), 0, item_width, item_height))
        frame.blit(explosion_image_frame, (0-(item_width * .5), 0 -(item_height*.5)))

        random_explosion_pos = (random_explosion_pos + 1) % 24
        
        clock.tick(60)
        pygame.display.update()
        
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())

