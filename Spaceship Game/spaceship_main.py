import pygame
from pygame.locals import *
from typing import List
from pygame import Surface
from sys import exit

# implementation of Spaceship - program template for RiceRocks

import math
import random

# from timer_decorator import timer_decorator

pygame.init()

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

# COORDINATE_TUPLE = tuple[int, int]
COORDINATE = List[int]
SIZE= COORDINATE



# frame: Surface = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
frame: Surface = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class ImageInfo:
    def __init__(self, center: COORDINATE, size: SIZE, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
#debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
#debris_image = pygame.image.load("images/debris2_blue.png").convert_alpha()
debris_image = pygame.image.load("images/debris2_blue.png")
debris_image = pygame.transform.scale(debris_image, (WIDTH, HEIGHT))

#dbRect = back


# nebula images - nebula_brown.png, nebula_blue.f2013.png
nebula_info = ImageInfo([400, 300], [800, 600])
#nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")
nebula_image = pygame.image.load("images/nebula_blue.f2013.png").convert()

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
#splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
splash_image = pygame.image.load("images/splash.png").convert_alpha()

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
#ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
# ship_image = pygame.image.load("images/double_ship.png").convert()
ship_image = pygame.image.load("images/double_ship.png").convert_alpha()
ship_image_inactive = ship_image.subsurface((0, 0, *ship_info.get_size()))
ship_image_active = ship_image.subsurface((ship_info.get_size()[0], 0, *ship_info.get_size()))


# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 75)
#missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
missile_image = pygame.image.load("images/shot2.png").convert_alpha()

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
#asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
# ship_image = pygame.image.load("images/asteroid_blue.png").convert()
asteroid_image = pygame.image.load("images/asteroid_blue.png").convert_alpha()

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
#explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image = pygame.image.load("images/explosion_alpha.png").convert()

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg

#SOUNDS IN SIMPLE GUI

#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
# soundtrack = pygame.mixer.music.load("sound/soundtrack.mp3")
pygame.mixer.music.load("sound/soundtrack.mp3")
#missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound = pygame.mixer.Sound("sound/missile_sound.ogg")
missile_sound.set_volume(.5)
#ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound = pygame.mixer.Sound("sound/thrust.ogg")
#explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound = pygame.mixer.Sound("sound/explosion.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    nu = ang * (math.pi / 180) * -1
    return [math.cos(nu), math.sin(nu)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

# Ship class
class Ship:

    def __init__(self, pos: COORDINATE, vel: COORDINATE, angle: int, image: Surface, image_active: Surface, info: ImageInfo):
        # self.pos = [pos[0], pos[1]]
        self.pos = [
            pos[0] - (info.get_center()[0]),
            pos[1] - (info.get_center()[1]),
        ]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_orig = image
        self.image_active_orig = image_active
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.force_redraw = False
    
    @property
    def centered_position(self):
        return [self.pos[0] + self.image_center[0], self.pos[1] + self.image_center[1]]
    
    # def collide(self, other_object: 'Sprite'):
    #     if dist(self.centered_position, other_object.centered_position) <= self.radius + other_object.radius:
    #         return True
    #     return False
    
    def draw(self, frame):
        
        if(self.angle_vel or self.force_redraw) != 0:
            s_image = ship_image_active if self.thrust else ship_image_inactive
            self.image = rot_center(s_image, self.angle)

            if self.force_redraw:
                self.force_redraw = False
        
        frame.blit(self.image, self.pos)

    def update(self):
        # update angle
        # print("self.angle before:", self.angle)
        # self.angle += self.angle_vel
        self.angle = (self.angle + self.angle_vel) % 360
        # print("self.angle after:", self.angle)
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            # print("acc", acc, self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .98
        self.vel[1] *= .98

    def set_thrust(self, on):
        self.thrust = on
        self.force_redraw = True
        if on:
            #ship_thrust_sound.rewind()
            ship_thrust_sound.play(fade_ms=1000)
        else:
            ship_thrust_sound.fadeout(1000)
       
    def increment_angle_vel(self):
        self.angle_vel -= 2
        
    def decrement_angle_vel(self):
        self.angle_vel += 2
        
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        # missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_pos = [self.pos[0] + self.image_center[0] - (missile_info.center[0]),
                        self.pos[1] + self.image_center[1] - (missile_info.center[1]) ]
        # print("forward", forward, self.angle)


        # missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_vel = [
            self.vel[0] + 6 * forward[0],
            self.vel[1] + 6 * forward[1]
            ]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
    
    
# Sprite class
class Sprite:

    def __init__(self, pos: COORDINATE, vel: COORDINATE, ang: int, ang_vel: int, image: Surface, info: ImageInfo, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.original_image = image.copy()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            # sound.rewind()
            sound.play()
   
    def draw(self, canvas: Surface):
        if self.animated:
            image_part = self.original_image.subsurface((self.age * (self.image_size[0]), 0, self.image_size[0], self.image_size[1]))
            if self.angle:
                image_part = rot_center(image_part, self.angle)
            canvas.blit(
                image_part,
                self.pos,
                # self.image_size
            )
        else:
            # canvas.blit(self.image, self.image_center, self.image_size,
            #               self.pos, self.image_size, self.angle)

            # print(f"Sprite pos: {self.pos}")
            # print(f"Sprite image_size: {self.image_size}")
            # print(f"Sprite image: {self.image}")
            # print("")
            if self.angle:
                self.image = rot_center(self.original_image, self.angle)
            canvas.blit(
                self.image,
                self.pos,
                # self.image_size
            )

        #if self.animated == True:
            
    def update(self):
        # update angle
        self.angle = (self.angle +  round(self.angle_vel * 10)) % 360
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
            
        
        self.age += 1
        if self.age >= self.lifespan:
            return True
     # print the position of the sprite
            # canvas.blit(self.image, self.pos)
        return False
    
    def collide(self, other_object: 'Sprite'):
        if dist(self.centered_position, other_object.centered_position) <= self.radius + other_object.radius:
            return True
        return False
    
    @property
    def centered_position(self):
        return [self.pos[0] + self.image_center[0], self.pos[1] + self.image_center[1]]
  
        
# key handlers to control ship   
def keydown(event):
    if event.key == pygame.K_LEFT:
        my_ship.decrement_angle_vel()
    elif event.key == pygame.K_RIGHT:
        my_ship.increment_angle_vel()
    elif event.key == pygame.K_UP:
        my_ship.set_thrust(True) # TODO: Find better implementation instead of passing in the frame
    elif event.key == pygame.K_SPACE:
        my_ship.shoot()
        
def keyup(event):
    if event.key == pygame.K_LEFT:
        my_ship.increment_angle_vel()
    elif event.key == pygame.K_RIGHT:
        my_ship.decrement_angle_vel()
    elif event.key == pygame.K_UP:
        my_ship.set_thrust(False) # TODO: Find better implementation instead of passing in the frame
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        pygame.mixer.music.play(loops=-1, fade_ms=500)
        

text = pygame.font.SysFont("arial", 22)

# @timer_decorator
def draw(frame): 
    global time, started, lives, score, rock_group
    
    # animiate background
    time += 1
    wtime = (time * .25) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    #canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    frame.blit(nebula_image, (0,0))
    
    
    # TODO IS this being drawn twice?
    frame.blit(debris_image, (wtime - WIDTH, 0) )
    frame.blit(debris_image, (wtime , 0))
   

    
    # draw UI
    frame.blit(text.render('Lives', True, (255,255,255)),(50,50))
    frame.blit(text.render("Score", True, (255,255,255)),(680,50))
    frame.blit(text.render(str(lives), True, (255,255,255)),(50,80))
    frame.blit(text.render(str(score), True, (255,255,255)),(680,80))
    
    # draw ship and sprites
    my_ship.draw(frame)
    
    # update ship and sprites
    my_ship.update()

    process_sprite_group(rock_group, frame)
    process_sprite_group(missile_group, frame)
    process_sprite_group(explosion_group, frame)
    score += group_group_collide(missile_group, rock_group)

    if group_collide(rock_group, my_ship):
        lives -= 1

    # draw splash screen if not started
    if not started:
        # print("Not started: WIDTH", (WIDTH - splash_info.get_size()[0]) * .5)
        # print("Not started: HEIGHT", (HEIGHT - splash_info.get_size()[1]) * .5)
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
        the_object.draw(canvas)
        if the_object.update():
            the_set.discard(the_object)    
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if len(rock_group) <= 2:# and started:
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
        
        
def group_collide(group, other_object):
    for obj in set(group):
        if obj.collide(other_object):
            group.discard(obj)
            centered_explostion_pos = [other_object.centered_position[0] - explosion_info.get_center()[0], other_object.centered_position[1] - explosion_info.get_center()[1]]
            explosion_group.add(Sprite(centered_explostion_pos, other_object.vel, 0, 0, explosion_image, explosion_info, explosion_sound))
            return True
    return False

def group_group_collide(missile_group, rock_group):
    number = 0
    for rock in set(rock_group):
        if group_collide(missile_group, rock):
            rock_group.discard(rock)
            number += 1
    return number

# initialize stuff
#frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites

SPAWN_ROCK_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ROCK_EVENT, 2000)

my_ship = Ship([WIDTH / 2 , HEIGHT / 2], [0, 0], 0, ship_image_inactive, ship_image_active, ship_info)

rock_group: set[Sprite] = set()
missile_group: set[Sprite] = set()
explosion_group: set[Sprite] = set()

    
# Define the dimensions of each item

item_width = 128
item_height = 128
# Create a variable to keep track of the current item index
current_party_idx = 0

# import time

while True:

    # start_time = time.time()
    for event in pygame.event.get():
        if event.type == QUIT:
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
        explostion_image_part = explosion_image.subsurface(
            (current_party_idx * (item_width), 0, item_width, item_height))
        frame.blit(explostion_image_part, (0-(item_width/2), 0 -(item_height/2)))

        current_party_idx = (current_party_idx + 1) % 24
        clock.tick(60)
        pygame.display.update()
    
    # end_time = time.time()
    # print(f"Function  took {end_time - start_time} seconds to execute.")


