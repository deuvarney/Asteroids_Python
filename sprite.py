from dataclasses import dataclass
from typing import NamedTuple, Optional
from pygame import Surface, mixer
from image_info import ImageInfo
from constants import COORDINATE, VELOCITY, WIDTH, HEIGHT
from utils import rot_center, dist


@dataclass
class Sprite_Pos_Details:
    """
    A dataclass representing the position and velocity details for a sprite.

    Attributes:
        position (COORDINATE): The position coordinates of the sprite.
        velocity (VELOCITY): The velocity coordinates of the sprite.
        angle (int, optional): The angle of the sprite in degrees. Defaults to 0.
        angle_velocity (int, optional): The angle velocity of the sprite in degrees per frame. Defaults to 0.
    """
    position: COORDINATE
    velocity: VELOCITY
    angle: int = 0
    angle_velocity: int = 0

class Sprite_Image_Pos(NamedTuple):
    """
    A NamedTuple representing an image and its position.

    Attributes:
        image (Surface): The image associated with the sprite.
        position (COORDINATE): The position coordinates of the sprite.
    """
    image: Surface
    position: COORDINATE

class Sprite:
    """
    A class representing a sprite, which is an object that appears on the screen with a certain image and position.

    Attributes:
        pos (COORDINATE): The position coordinates of the sprite.
        vel (VELOCITY): The velocity coordinates of the sprite.
        angle (int): The angle of the sprite in degrees.
        angle_vel (int): The angle velocity of the sprite in degrees per frame.
        image (Surface): The image associated with the sprite.
        info (ImageInfo): An object containing metadata about the image, including its center coordinates,
            size, radius, lifespan, and whether it is animated or not.
        sound (Optional[mixer.Sound]): An optional sound to play when the sprite is initialized.
    """

    def __init__(self, pos: COORDINATE, vel: VELOCITY, ang: int, ang_vel: int, image: Surface, info: ImageInfo, sound: Optional[mixer.Sound] = None, angle_vel_multi: int = 10):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.angle_velocity_multiplier = angle_vel_multi
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

    def get_rotated_image(self, image: Optional[Surface] = None) -> Surface:
        """
        Returns the image associated with the sprite, rotated by the angle of the sprite.

        Args:
            image (Surface, optional): The image to be rotated. Defaults to None.

        Returns:
            Surface: The rotated image.
        """
        if image is None:
            image = self.image
        return rot_center(image, self.angle)

    def draw(self) -> Sprite_Image_Pos:
        """
        Draws the sprite on the screen.

        Returns:
            Sprite_Image_Pos: A NamedTuple containing the image and position of the sprite.
        """
        if self.animated:
            image_part = self.original_image.subsurface((self.age * (self.image_size[0]), 0, self.image_size[0], self.image_size[1]))
            if self.angle:
                image_part = rot_center(image_part, self.angle)
            return Sprite_Image_Pos(image_part, self.pos)
        else:
            if self.angle:
                self.image = rot_center(self.original_image, self.angle)
            return Sprite_Image_Pos(self.image, self.pos)
            
    def update(self) -> bool:
        """
        Updates the sprite's position and angle.

        Returns:
            bool: True if the sprite's lifespan has expired, False otherwise.
        """
        # update angle
        self.angle = (self.angle +  round(self.angle_vel * self.angle_velocity_multiplier)) % 360
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
            
        
        self.age += 1
        if self.age >= self.lifespan:
            return True
        return False
    
    def collide(self, other_object: 'Sprite') -> bool:
        """
        Checks if the sprite has collided with another object.

        Args:
            other_object (Sprite): The other object to check for collision.

        Returns:
            bool: True if a collision has occurred, False otherwise.
        """
        if dist(self.pos_center, other_object.pos_center) <= self.radius + other_object.radius:
            return True
        return False
    
    @property
    def pos_center(self) -> COORDINATE:
        """
        Returns the position of the center of the sprite.

        Returns:
            COORDINATE: The position coordinates of the center of the sprite.
        """
        return [self.pos[0] + self.image_center[0], self.pos[1] + self.image_center[1]]
