import pygame
from pygame.locals import *
from sys import exit

# implementation of Spaceship - program template for RiceRocks

import math
import random

pygame.init()

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

frame = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
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


# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
#nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")
nebula_image = pygame.image.load("images/nebula_blue.f2013.png").convert()

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
#splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
splash_image = pygame.image.load("images/splash.png").convert()

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
#ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

#Real
#ship_image = pygame.image.load("images/double_ship.png").convert_alpha()
#ship_image = pygame.transform.rotate(ship_image, -50)

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
#missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
missile_image = pygame.image.load("images/shot2.png").convert()

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
#asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
ship_image = pygame.image.load("images/asteroid_blue.png").convert()
asteroid_image = pygame.image.load("images/asteroid_blue.png").convert()

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
#explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image = pygame.image.load("images/explosion_alpha.png").convert()

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg

#SOUNDS IN SIMPLE GUI

#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack = pygame.mixer.music.load("sound/soundtrack.mp3");
#missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound = pygame.mixer.Sound("sound/missile_sound.ogg")
missile_sound.set_volume(.5)
#ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound = pygame.mixer.Sound("sound/thrust.ogg");
#explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound = pygame.mixer.Sound("sound/explosion.ogg");

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,frame):
        global ship_image
        #if self.thrust:
        
        
        if(self.angle_vel) != 0:
            print "self.pos", self.pos
            print "self.vel", self.vel
            print "self.angle", self.angle
            print
            #ship_image = pygame.image.load("images/double_ship.png").convert_alpha()
            ship_image = pygame.transform.rotate(ship_image, self.angle)
            self.image = ship_image
            
            self.image = rot_center(self.image, self.angle)
            #self.image = pygame.transform.rotate(self.image, self.angle)
            #self.image = self.image.get_rect(center = old_center)
            
            #self.image = pygame.transform.rotate(self.image, self.angle)
        
        frame.blit(self.image, self.pos)#, ((0,0),(self.image_center[0]*2, self.image_center[1]*2)))
                                         
            #canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,self.pos, self.image_size, self.angle)
        #else:
            
            #canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        #self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        #self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
       # if self.thrust:
        #    acc = angle_to_vector(self.angle)
         #   self.vel[0] += acc[0] * .1
          #  self.vel[1] += acc[1] * .1
            
        #self.vel[0] *= .99
        #self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            #ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.stop()
       
    def increment_angle_vel(self):
        self.angle_vel += 1#.05
        
    def decrement_angle_vel(self):
        self.angle_vel -= 1#.05
        
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        #a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, 
                              (self.image_center[0] + (self.image_size[0] *self.age), self.image_center[1]), 
                              (self.image_size[0],self.image_size[1]),
                              (self.pos[0], self.pos[1]),
                              (self.image_size[0] , self.image_size[1]),
                              self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

        #if self.animated == True:
            
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        
        self.age += 1
        if self.age >= self.lifespan:
            return True
        return False
    
    def collide(self, other_object):
        if dist(self.pos, other_object.pos) <= self.radius + other_object.radius:
            return True
        return False
  
        
# key handlers to control ship   
def keydown(event):
    if event.key == pygame.K_LEFT:
        my_ship.decrement_angle_vel()
    elif event.key == pygame.K_RIGHT:
        my_ship.increment_angle_vel()
    elif event.key == pygame.K_UP:
        my_ship.set_thrust(True)
    elif event.key == pygame.K_SPACE:
        my_ship.shoot()
        
def keyup(event):
    if event.key == pygame.K_LEFT:
        my_ship.increment_angle_vel()
    elif event.key == pygame.K_RIGHT:
        my_ship.decrement_angle_vel()
    elif event.key == pygame.K_UP:
        my_ship.set_thrust(False)
        
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
        soundtrack.rewind()
        soundtrack.play()
        

text = pygame.font.SysFont("arial", 22)
#def draw(canvas):
def draw(frame): 
    global time, started, lives, score, rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    #canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    frame.blit(nebula_image, (0,0))
    
    
    frame.blit(debris_image, (wtime - WIDTH, 0) )
     #canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    frame.blit(debris_image, (wtime , 0))
    #canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
   

    
    # draw UI
    
    frame.blit(text.render("Lives", True, (255,255,255)),(50,50))
    #canvas.draw_text("Lives", [50, 50], 22, "White")
    frame.blit(text.render("Score", True, (255,255,255)),(680,50))
    #canvas.draw_text("Score", [680, 50], 22, "White")
    frame.blit(text.render(str(lives), True, (255,255,255)),(50,80))
    #canvas.draw_text(str(lives), [50, 80], 22, "White")
    frame.blit(text.render(str(score), True, (255,255,255)),(680,80))
    #canvas.draw_text(str(score), [680, 80], 22, "White")
    
    pygame.draw.rect(frame, (255,255,255), Rect(
                                                (WIDTH/2 - 45 ,HEIGHT/2 -45), 
                                                 ( 90, 90 ) )
                     )
    
    # draw ship and sprites
    my_ship.draw(frame)
    #a_rock.draw(canvas)
    #a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    #a_rock.update()
    #a_missile.update()
    '''
    
    process_sprite_group(rock_group, canvas)
    
    process_sprite_group(missile_group, canvas)
    
    process_sprite_group(explosion_group, canvas)
    if group_collide(rock_group, my_ship):
        lives -= 1
    
    score += group_group_collide(missile_group, rock_group)
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    if lives == 0:
        started = False
        rock_group = set()
        soundtrack.pause()
'''
#process sprite group helper function
def process_sprite_group(the_set, canvas):
    for the_object in set(the_set):
        the_object.draw(canvas)
        if the_object.update():
            the_set.discard(the_object)    
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if len(rock_group) <= 6 and started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1
        #rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))
        new_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        if dist(new_rock.pos, my_ship.pos) > 100:
            rock_group.add(new_rock)
        else:
            rock_spawner()
        
        
def group_collide(group, other_object):
    for obj in set(group):
        if obj.collide(other_object):
            group.discard(obj)
            explosion_group.add(Sprite(other_object.pos, other_object.vel, 0, 0, explosion_image, explosion_info, explosion_sound))
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

#my_ship = Ship([WIDTH / 2 , HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
my_ship = Ship([(WIDTH / 2) -asteroid_info.center[0], (HEIGHT / 2) -asteroid_info.center[1]], [0, 0], 0, ship_image, asteroid_info)

#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
#frame.set_keyup_handler(keyup)
#frame.set_keydown_handler(keydown)
#frame.set_mouseclick_handler(click)
#frame.set_draw_handler(draw)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:

            keydown(event)
        elif event.type == pygame.KEYUP:

            keyup(event)    
         
        
        #elif event.type == pygame.MOUSEBUTTONUP:
         #   pos = pygame.mouse.get_pos()
         #   click(pos)
    draw(frame)
    pygame.display.update()

#timer = simplegui.create_timer(2000.0, rock_spawner)

# get things rolling
#timer.start()
#frame.start()
