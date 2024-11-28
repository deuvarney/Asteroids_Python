from dataclasses import dataclass
from typing import Optional
from pygame import Surface, mixer
from image_info import ImageInfo
from constants import COORDINATE, VELOCITY, WIDTH, HEIGHT
from utils import rot_center, dist


@dataclass
class Sprite_Pos_Details:
    position: COORDINATE
    velocity: VELOCITY
    angle: int = 0
    angle_velocity: int = 0

class Sprite:

    def __init__(self, pos: COORDINATE, vel: VELOCITY, ang: int, ang_vel: int, image: Surface, info: ImageInfo, sound: Optional[mixer.Sound] = None):
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
            sound.play()

    def draw(self, canvas: Surface) -> None:
        if self.animated:
            image_part = self.original_image.subsurface((self.age * (self.image_size[0]), 0, self.image_size[0], self.image_size[1]))
            if self.angle:
                image_part = rot_center(image_part, self.angle)
            canvas.blit(image_part,self.pos)
        else:
            if self.angle:
                self.image = rot_center(self.original_image, self.angle)
            canvas.blit(
                self.image,
                self.pos
            )
            
    def update(self) -> bool:
        # update angle
        self.angle = (self.angle +  round(self.angle_vel * 10)) % 360
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
            
        
        self.age += 1
        if self.age >= self.lifespan:
            return True
        return False
    
    def collide(self, other_object: 'Sprite') -> bool:
        if dist(self.pos_center, other_object.pos_center) <= self.radius + other_object.radius:
            return True
        return False
    
    @property
    def pos_center(self) -> COORDINATE:
        return [self.pos[0] + self.image_center[0], self.pos[1] + self.image_center[1]]
