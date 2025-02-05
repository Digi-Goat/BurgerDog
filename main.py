import random, pygame

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

FPS = 60
clock = pygame.time.Clock()

PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3
STARTING_BURGER_VELOCITY = 0.5
BUFFER_DISTANCE = 100

score = 0
burger_points = 0
burgers_eaten = 0
player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY
boost_level = STARTING_BOOST_LEVEL
burger_velocity = STARTING_BURGER_VELOCITY

ORANGE = (246,170, 54)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font("WashYourHand.ttf", 32)

#NOTES:  text is a str, background_color is a tuple[int, int, int]
#NOTES:  **locations is basically a dictionary of str, tuple[int, int] or int
#NOTES:  this prep_text returns a tuple containing a Font object and a Rectangle object.
def prep_text(text : str, background_color : tuple[int, int, int], **locations):
    #TODO: create a text_to_return variable and assign font.render(text, True, background_color)
    #TODO: create a rect variable and assign text_to_return.get_rect()
    #TODO: create a for location in locations loop
    #TODO: for loop block start
        if location == "topleft":
            rect.topleft = locations["topleft"]
        elif location == "centerx":
            rect.centerx = locations["centerx"]
        # NOTE:  We'll add more later.
    #TODO: for loop block end
    #TODO: return (text_to_return, rect)
    pass #TODO: remove this when done.