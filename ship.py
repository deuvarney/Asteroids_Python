from pygame import Surface, mixer
from image_info import ImageInfo
from constants import *
from utils import angle_to_vector
from sprite import Sprite_Image_Pos, Sprite_Pos_Details, Sprite

class Ship(Sprite):
    """
    A class representing the ship object in the game.

    This class extends the Sprite class and provides additional
    methods for updating the ship's position and shooting missiles.
    """
    def __init__(self, pos: COORDINATE, vel: VELOCITY, angle: int, image: Surface, image_active: Surface, info: ImageInfo):
        """
        Initializes an instance of the Ship class.

        Args:
            pos (list): The initial position of the ship.
            vel (list): The initial velocity of the ship.
            angle (int): The initial angle of the ship (in degrees).
            image (pygame.Surface): The image of the ship.
            image_active (pygame.Surface): The image of the ship when it is thrusting.
            info (ImageInfo): An object containing metadata about the ship's image.
        """
        updated_pos = [
            pos[0] - (info.get_center()[0]),
            pos[1] - (info.get_center()[1]),
        ]
        super().__init__(updated_pos, vel, angle, 0, image, info, None, 1)
        self.thrust = False
        self.image_active_orig = image_active
        self.force_redraw = False
    
    def draw(self) -> Sprite_Image_Pos:
        """
        Draws the ship on the screen.

        If the ship is thrusting, this method draws the ship's active image. Otherwise, it draws the
        ship's original image. If the ship's angle or angle velocity has changed, or if the ship's
        thrust state has changed, this method forces a redraw of the ship.

        Returns:
            Sprite_Image_Pos: A named tuple containing the ship's image and position.
        """
        if self.angle_vel != 0 or self.force_redraw:
            s_image = self.image_active_orig if self.thrust else self.original_image
            self.image = self.get_rotated_image(s_image)

            if self.force_redraw:
                self.force_redraw = False
        return Sprite_Image_Pos(self.image, self.pos)
    
    def update(self) -> bool:
        """
        Updates the ship's position and velocity.

        If the ship is thrusting, this method updates the ship's velocity by adding a constant speed
        in the forward direction. The ship's velocity is also reduced by a friction factor.

        Returns:
            bool: A flag indicating whether the ship should be removed from the game.
        """
        super().update()

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * SHIP_THRUST_MULTIPLIER
            self.vel[1] += acc[1] * SHIP_THRUST_MULTIPLIER
            
        self.vel[0] *= SHIP_VELOCITY_MULTIPLIER
        self.vel[1] *= SHIP_VELOCITY_MULTIPLIER
        return False

    def set_thrust(self, on: bool, sound: mixer.Sound) -> None:
        """
        Sets the ship's thrust state.

        If the ship is thrusting, this method plays a sound effect. If the ship is not thrusting, this
        method stops the sound effect. This method also forces a redraw of the ship.

        Args:
            on (bool): A flag indicating whether the ship should be thrusting.
            sound (pygame.mixer.Sound): The sound effect to play when the ship is thrusting.
        """
        self.thrust = on
        self.force_redraw = True
        if on:
            sound.play(fade_ms=SHIP_THRUST_FADE_IN_TIME)
        else:
            sound.fadeout(SHIP_THRUST_FADE_OUT_TIME)
       
    def increment_angle_vel(self) -> None:
        """
        Increments the ship's angle velocity by 1 degree per frame.

        This method is called when the ship is rotating clockwise.
        """
        self.angle_vel -= SHIP_TURN_SPEED
        
    def decrement_angle_vel(self) -> None:
        """
        Decrements the ship's angle velocity by 1 degree per frame.

        This method is called when the ship is rotating counterclockwise.
        """
        self.angle_vel += SHIP_TURN_SPEED
        
    def shoot(self, missile_info: ImageInfo) -> Sprite_Pos_Details:
        """
        Calculates and returns the position and velocity details for a missile shot from the ship.

        This method computes the forward direction vector based on the ship's current angle, and
        determines the starting position and velocity of a missile to be shot. The missile's position
        is offset based on the ship's position and image center, and its velocity is calculated by
        adding a constant speed in the forward direction to the ship's current velocity.

        Returns:
            Sprite_Pos_Details: An object containing the position, velocity, angle, and angle velocity
                                of the missile.
        """
        forward = angle_to_vector(self.angle)
        centered_x, centered_y = self.pos_center
        
        centered_missile_pos = [centered_x - (missile_info.center[0]),
                        centered_y - (missile_info.center[1]) ]
        
        adjusted_missile_pos = angle_to_vector(
            self.angle, 
            int(self.image_size[0] * .5), 
            centered_missile_pos
        )

        missile_vel = [
            self.vel[0] + MISSILE_SPEED * forward[0],
            self.vel[1] + MISSILE_SPEED * forward[1]
            ]
        return Sprite_Pos_Details(position=adjusted_missile_pos, velocity=missile_vel, angle=self.angle, angle_velocity=0)
    
   