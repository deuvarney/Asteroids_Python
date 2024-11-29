import random
from typing import Set

import pygame
from pygame import Surface
from sprite import Sprite
from ship import Ship
from utils import *
from constants import WIDTH, HEIGHT


import asyncio

pygame.init()
frame = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

from assets import *

SPAWN_ROCK_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ROCK_EVENT, 2000)

class AsteroidsGame:
    def __init__(self):
        self.frame: Surface = frame
        self.clock = pygame.time.Clock()
        
        # Game state variables
        self.score = 0
        self.lives = 3
        self.time = 0
        self.started = False
        
        # Load assets
        pygame.mixer.music.load(soundtrack_path)
        
        # Initialize ship and groups
        self.my_ship = Ship([int(WIDTH * .5), int(HEIGHT * .5)], [0.0, 0.0], 0, ship_image_inactive, ship_image_active, ship_info)
        self.rock_group: set[Sprite] = set()
        self.missile_group: set[Sprite] = set()
        self.explosion_group: set[Sprite] = set()

        # Set up the rock spawning timer
        SPAWN_ROCK_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_ROCK_EVENT, 2000)

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
                self.lives = 3
                self.score = 0
                pygame.mixer.music.play(loops=-1, fade_ms=500)

    def draw(self):
        self.time += 1
        wtime = (self.time * .25) % WIDTH
        self.frame.blit(nebula_image, (0, 0))
        self.frame.blit(debris_image, (wtime - WIDTH, 0))
        self.frame.blit(debris_image, (wtime, 0))

        text = pygame.font.SysFont("arial", 22)
        self.frame.blit(text.render('Lives', True, (255, 255, 255)), (50, 50))
        self.frame.blit(text.render("Score", True, (255, 255, 255)), (680, 50))
        self.frame.blit(text.render(str(self.lives), True, (255, 255, 255)), (50, 80))
        self.frame.blit(text.render(str(self.score), True, (255, 255, 255)), (680, 80))

        self.my_ship.update()
        self.frame.blit(*self.my_ship.draw())

        self.process_sprite_group(self.rock_group)
        self.process_sprite_group(self.missile_group)
        self.process_sprite_group(self.explosion_group)

        self.score += self.rock_missile_group_collide()

        if self.group_collide(self.rock_group, self.my_ship):
            self.lives -= 1

        if not self.started:
            self.frame.blit(splash_image,
                            ((WIDTH - splash_info.get_size()[0]) * .5,
                             (HEIGHT - splash_info.get_size()[1]) * .5))

        if self.lives == 0:
            self.started = False
            self.rock_group = set()
            pygame.mixer.music.fadeout(1500)

    def process_sprite_group(self, the_set: set[Sprite]):
        for the_object in the_set.copy():
            self.frame.blit(*the_object.draw())
            if the_object.update():
                the_set.discard(the_object)

    def rock_spawner(self):
        if len(self.rock_group) <= 2:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            rock_vel = [
                random.random() * .6 - .3,
                random.random() * .6 - .3
            ]
            rock_avel = random.random() * .2 - .1
            new_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image.subsurface((0, 0, *asteroid_image.get_size())), asteroid_info)
            if dist(new_rock.pos, self.my_ship.pos) > 100:
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
        number = 0
        for rock in set(self.rock_group):
            if self.group_collide(self.missile_group, rock):
                self.rock_group.discard(rock)
                number += 1
        return number

    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)
                elif event.type == pygame.KEYUP:
                    self.handle_keyup(event)
                elif event.type == SPAWN_ROCK_EVENT and self.started:
                    self.rock_spawner()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.handle_mouseclick(pos)

            self.draw()

            self.clock.tick(60)
            pygame.display.update()

            await asyncio.sleep(0)

if __name__ == "__main__":
    game = AsteroidsGame()
    asyncio.run(game.run())