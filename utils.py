
import math
from pygame import transform

from constants import COORDINATE

# helper functions to handle 2d transformations

def angle_to_vector(angle: int, radius_offset: int = 1, starting_position: COORDINATE = [0,0]):
    """
    Converts an angle in degrees to a 2D unit vector.

    Args:
        angle (int): The angle in degrees.
        radius_offset (int, optional): The offset from the origin. Defaults to 1.
        starting_position (list, optional): The position where the vector starts. Defaults to [0,0].

    Returns:
        list: A list containing the x and y components of the unit vector.
    """
    sanitized_angle = angle * (math.pi / 180) * -1
    return [
        starting_position[0] + math.cos(sanitized_angle) * radius_offset, 
        starting_position[1] + math.sin(sanitized_angle) * radius_offset
        ]

def dist(p, q):
    
    """
    Computes the Euclidean distance between two points.

    Args:
        p (list): First point.
        q (list): Second point.

    Returns:
        float: The Euclidean distance between the two points.
    """
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def rot_center(image, angle):
    """
    Rotates an image around its center.

    This function takes an image and an angle, rotates the image by the given angle,
    and returns the rotated image while ensuring that the rotation is performed 
    around the center of the image.

    Args:
        image (Surface): The image to be rotated.
        angle (float): The angle (in degrees) by which to rotate the image.

    Returns:
        Surface: The rotated image, cropped to maintain the original image's center.
    """
    orig_rect = image.get_rect()
    rot_image = transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image