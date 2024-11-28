
import math
from pygame import transform


# helper functions to handle 2d transformations
def angle_to_vector(angle):
    
    """
    Converts an angle in degrees to a 2D unit vector.

    This function takes an angle in degrees, converts it to radians, and then computes
    the corresponding unit vector in 2D space. The angle is assumed to be measured 
    clockwise from the positive x-axis.

    Args:
        ang (float): The angle in degrees.

    Returns:
        list: A list containing the x and y components of the unit vector.
    """
    sanitized_angle = angle * (math.pi / 180) * -1
    return [math.cos(sanitized_angle), math.sin(sanitized_angle)]

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