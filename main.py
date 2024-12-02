import random
from typing import Set

import pygame
from pygame import Surface
from sprite import Sprite
from ship import Ship
from utils import *
from constants import *
import asyncio

# TODO: LOOK INTO HOW TO FIX THESE IMPORTS
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

from assets import *

SPAWN_ROCK_EVENT = pygame.USEREVENT + 1

class AsteroidsGame:
    def __init__(self):
        self.screen: Surface = screen
        self.clock = pygame.time.Clock()
        
        # Game state variables
        self.score = INITIAL_SCORE
        self.lives = INITIAL_LIVES
        self.time = 0
        self.started = False

        # Display timers
        self.time = 0
        self.wtime = 0
        
        # Load assets
        pygame.mixer.music.load(soundtrack_path)

        ship_position = [int(WIDTH * .5), int(HEIGHT * .5)]
        ship_velocity = [0.0, 0.0]
        ship_angle = 0
        
        # Initialize ship and groups
        self.my_ship = Ship(ship_position, ship_velocity, ship_angle, ship_image_inactive, ship_image_active, ship_info)
        self.rock_group: set[Sprite] = set()
        self.missile_group: set[Sprite] = set()
        self.explosion_group: set[Sprite] = set()

    def handle_keydown(self, event):
        if event.key == pygame.K_LEFT:
            self.my_ship.decrement_angle_vel()
        elif event.key == pygame.K_RIGHT:
            self.my_ship.increment_angle_vel()
        elif event.key == pygame.K_UP:
            self.my_ship.set_thrust(True, ship_thrust_sound)
        elif event.key == pygame.K_SPACE:
            missile_details = self.my_ship.shoot(missile_info)
            self.missile_group.add(Sprite(missile_details.position, missile_details.velocity, missile_details.angle, missile_details.angle_velocity, missile_image, missile_info, missile_sound))

    def handle_keyup(self, event):
        if event.key == pygame.K_LEFT:
            self.my_ship.increment_angle_vel()
        elif event.key == pygame.K_RIGHT:
            self.my_ship.decrement_angle_vel()
        elif event.key == pygame.K_UP:
            self.my_ship.set_thrust(False, ship_thrust_sound)

    def handle_mouseclick(self, pos):
        if not self.started:
            center = [WIDTH / 2, HEIGHT / 2]
            size = splash_info.get_size()
            inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
            inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
            if inwidth and inheight:
                self.started = True
                self.lives = INITIAL_LIVES
                self.score = INITIAL_SCORE
                pygame.mixer.music.play(loops=-1, fade_ms=SOUNDTRACK_FADE_IN_TIME)
                # Start up the rock spawning timer
                pygame.time.set_timer(SPAWN_ROCK_EVENT, SPAWN_ROCK_EVENT_INTERVAL)

    def update(self):

        self.time += 1
        # Update display offset for debris based on time and width
        self.wtime = (self.time * DEBRIS_SCROLL_SPEED) % WIDTH

        self.my_ship.update()

        if self.group_collide(self.rock_group, self.my_ship):
            self.lives -= 1

        

        if self.lives == 0 and self.started:
            self.started = False
            self.rock_group = set()
            pygame.mixer.music.fadeout(SOUNDTRACK_FADE_OUT_TIME)

            # Stop up the rock spawning timer
            pygame.time.set_timer(SPAWN_ROCK_EVENT, 0)
        
        self.score += self.rock_missile_group_collide()

    def draw(self):
        
        self.screen.blit(nebula_image, (0, 0)) 
        self.screen.blit(debris_image, (self.wtime - WIDTH, 0)) # Debris offset image
        self.screen.blit(debris_image, (self.wtime, 0)) # Debris image

        text = pygame.font.SysFont("arial", 22)
        self.screen.blit(text.render('Lives', True, (255, 255, 255)), (50, 50))
        self.screen.blit(text.render("Score", True, (255, 255, 255)), (680, 50))
        self.screen.blit(text.render(str(self.lives), True, (255, 255, 255)), (50, 80))
        self.screen.blit(text.render(str(self.score), True, (255, 255, 255)), (680, 80))

        
        self.screen.blit(*self.my_ship.draw())

        self.process_sprite_group(self.rock_group)
        self.process_sprite_group(self.missile_group)
        self.process_sprite_group(self.explosion_group)

        if not self.started:
            self.screen.blit(splash_image,
                            ((WIDTH - splash_info.get_size()[0]) * .5,
                             (HEIGHT - splash_info.get_size()[1]) * .5))


    def process_sprite_group(self, the_set: set[Sprite]):
        for the_object in the_set.copy():
            self.screen.blit(*the_object.draw())
            if the_object.update():
                the_set.discard(the_object)

    def asteroid_spawner(self):
        if len(self.rock_group) <= ASTEROID_SPAWN_MIN_COUNT:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            rock_vel = [
                random.random() * ASTEROID_VELOCITY_MULTIPLIER - ASTEROID_VELOCITY_ADJUSTMENT,
                random.random() * ASTEROID_VELOCITY_MULTIPLIER - ASTEROID_VELOCITY_ADJUSTMENT
            ]
            rock_acc_vel = random.random() * ASTEROID_ACC_MULTIPLIER - ASTEROID_ACC_ADJUSTMENT
            new_rock = Sprite(rock_pos, rock_vel, 0, rock_acc_vel, asteroid_image.subsurface((0, 0, *asteroid_image.get_size())), asteroid_info)
            if dist(new_rock.pos, self.my_ship.pos) > ASTEROID_SPAWN_MIN_DISTANCE:
                self.rock_group.add(new_rock)

    def group_collide(self, group: Set[Sprite], other_object: Sprite):
        for obj in set(group):
            if obj.collide(other_object):
                group.discard(obj)
                centered_explosion_pos = [other_object.pos_center[0] - explosion_info.get_center()[0], other_object.pos_center[1] - explosion_info.get_center()[1]]
                self.explosion_group.add(Sprite(centered_explosion_pos, other_object.vel, 0, 0, explosion_image, explosion_info, explosion_sound))
                return True
        return False

    def rock_missile_group_collide(self):
        collisions_count = 0
        for rock in set(self.rock_group):
            if self.group_collide(self.missile_group, rock):
                self.rock_group.discard(rock)
                collisions_count += 1
        return collisions_count

    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)
                elif event.type == pygame.KEYUP:
                    self.handle_keyup(event)
                elif event.type == SPAWN_ROCK_EVENT:
                    self.asteroid_spawner()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.handle_mouseclick(pos)

            self.update()
            self.draw()

            self.clock.tick(FPS)
            pygame.display.update()

            await asyncio.sleep(0)

if __name__ == "__main__":
    game = AsteroidsGame()
    asyncio.run(game.run())