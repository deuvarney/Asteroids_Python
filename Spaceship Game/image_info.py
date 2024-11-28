from constants import COORDINATE, SIZE

class ImageInfo:
    """
    Class that stores metadata about an image, including its center coordinates,
    size, radius, lifespan, and whether it is animated or not.
    """

    def __init__(self, center: COORDINATE, size: SIZE, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self) -> COORDINATE:
        """
        Returns the center coordinates of the image.
        """
        return self.center

    def get_size(self) -> SIZE:
        """
        Returns the size of the image.
        """
        return self.size

    def get_radius(self) -> int:
        """
        Returns the radius of the image.
        """
        return self.radius

    def get_lifespan(self) -> float:
        """
        Returns the lifespan of the image.
        """
        return self.lifespan

    def get_animated(self) -> bool:
        """
        Returns whether the image is animated or not.
        """
        return self.animated
