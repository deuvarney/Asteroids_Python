import pygame
from image_info import ImageInfo
from constants import WIDTH, HEIGHT

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = pygame.image.load("images/debris2_blue.png")
debris_image = pygame.transform.scale(debris_image, (WIDTH, HEIGHT))



# nebula images - nebula_brown.png, nebula_blue.f2013.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = pygame.image.load("images/nebula_blue.f2013.png").convert_alpha()

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = pygame.image.load("images/splash.png").convert_alpha()

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = pygame.image.load("images/double_ship.png").convert_alpha()
ship_image_inactive = ship_image.subsurface((0, 0, *ship_info.get_size()))
ship_image_active = ship_image.subsurface((ship_info.get_size()[0], 0, *ship_info.get_size()))


# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 75)
missile_image = pygame.image.load("images/shot2.png").convert_alpha()

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = pygame.image.load("images/asteroid_blue.png").convert_alpha()

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = pygame.image.load("images/explosion_alpha.png").convert_alpha()

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg

#SOUNDS

# pygame.mixer.music.load("sound/soundtrack.mp3")
soundtrack_path="sound/soundtrack.mp3"

missile_sound = pygame.mixer.Sound("sound/missile_sound.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = pygame.mixer.Sound("sound/thrust.ogg")
explosion_sound = pygame.mixer.Sound("sound/explosion.ogg")