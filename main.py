import random
import pygame

pygame.init()

# Window setup
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

# Game setup
FPS = 60
clock = pygame.time.Clock()

PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3
BURGER_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

# Game variables
score = 0
burger_points = 0
burgers_eaten = 0
player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY
boost_level = STARTING_BOOST_LEVEL
burger_velocity = STARTING_BURGER_VELOCITY

# Colors
ORANGE = (246, 170, 54)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load assets
font = pygame.font.Font("assets/WashYourHand.ttf", 32)
bark_sound = pygame.mixer.Sound("assets/bark_sound.wav")
miss_sound = pygame.mixer.Sound("assets/miss_sound.wav")
pygame.mixer.music.load("assets/bd_background_music.wav")

player_image_right = pygame.image.load("assets/dog_right.png")
player_image_left = pygame.image.load("assets/dog_left.png")
burger_image = pygame.image.load("assets/burger.png")

# Player setup
player_image = player_image_left
player_rect = player_image.get_rect()
player_rect.centerx = WINDOW_WIDTH // 2
player_rect.bottom = WINDOW_HEIGHT

# Burger setup
burger_rect = burger_image.get_rect()
burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - burger_rect.width), -BUFFER_DISTANCE)

# Start music
pygame.mixer.music.play(-1)

# HUD text variables
points_text, score_text, eaten_text, lives_text, boost_text, game_over_text, continue_text = None, None, None, None, None, None, None


def prep_text(text, color, **locations):
    rendered_text = font.render(text, True, color)
    rect = rendered_text.get_rect()
    for loc, value in locations.items():
        setattr(rect, loc, value)
    return rendered_text, rect


def check_quit():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


def move_player():
    global player_velocity, player_image
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_velocity
        player_image = player_image_left
    if keys[pygame.K_RIGHT] and player_rect.right < WINDOW_WIDTH:
        player_rect.x += player_velocity
        player_image = player_image_right
    if keys[pygame.K_UP] and player_rect.top > 100:
        player_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += player_velocity
    engage_boost(keys)


def engage_boost(keys):
    global player_velocity, boost_level
    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = PLAYER_BOOST_VELOCITY
        boost_level -= 1
    else:
        player_velocity = PLAYER_NORMAL_VELOCITY


def move_burger():
    global burger_points
    burger_rect.y += burger_velocity
    burger_points = int(burger_velocity * (WINDOW_HEIGHT - burger_rect.y + 100))


def handle_miss():
    global player_lives
    if burger_rect.y > WINDOW_HEIGHT:
        player_lives -= 1
        miss_sound.play()
        reset_burger()


def reset_burger():
    global burger_velocity, boost_level
    burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - burger_rect.width), -BUFFER_DISTANCE)
    burger_velocity = STARTING_BURGER_VELOCITY
    player_rect.centerx = WINDOW_WIDTH // 2
    player_rect.bottom = WINDOW_HEIGHT
    boost_level = STARTING_BOOST_LEVEL


def check_collisions():
    global score, burgers_eaten, burger_velocity, boost_level
    if player_rect.colliderect(burger_rect):
        score += burger_points
        burgers_eaten += 1
        bark_sound.play()
        reset_burger()
        burger_velocity += BURGER_ACCELERATION
        boost_level = min(boost_level + 25, STARTING_BOOST_LEVEL)


def update_hud():
    global points_text, score_text, eaten_text, lives_text, boost_text
    points_text, points_rect = prep_text(f"Burger Points: {burger_points}", ORANGE, topleft=(10, 10))
    score_text, score_rect = prep_text(f"Score: {score}", ORANGE, topleft=(10, 50))
    eaten_text, eaten_rect = prep_text(f"Burgers Eaten: {burgers_eaten}", ORANGE, centerx=WINDOW_WIDTH // 2, y=50)
    lives_text, lives_rect = prep_text(f"Lives: {player_lives}", ORANGE, topright=(WINDOW_WIDTH - 10, 10))
    boost_text, boost_rect = prep_text(f"Boost: {boost_level}", ORANGE, topright=(WINDOW_WIDTH - 10, 50))

    return [points_text, points_rect, score_text, score_rect, eaten_text, eaten_rect, lives_text, lives_rect,
            boost_text, boost_rect]


def check_game_over():
    global game_over_text, continue_text, is_paused, score, burgers_eaten, player_lives, boost_level, burger_velocity, running
    if player_lives == 0:
        # Prepare game over text
        game_over_text = font.render(f"FINAL SCORE: {score}", True, ORANGE)
        continue_text = font.render("Press any key to play again", True, ORANGE)

        # Display the game over text and continue prompt
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        # Draw game over text and continue prompt without clearing the game screen
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)

        # Keep the player and burger on screen
        display_surface.blit(player_image, player_rect)
        display_surface.blit(burger_image, burger_rect)

        pygame.display.update()
        pygame.mixer.music.stop()

        # Pause the game until user input
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Reset the game and resume
                    score = 0
                    burgers_eaten = 0
                    player_lives = PLAYER_STARTING_LIVES
                    boost_level = STARTING_BOOST_LEVEL
                    burger_velocity = STARTING_BURGER_VELOCITY
                    pygame.mixer.music.play(-1)
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False


def display_hud(hud_elements):
    display_surface.fill(BLACK)
    for i in range(0, len(hud_elements), 2):
        display_surface.blit(hud_elements[i], hud_elements[i + 1])
    pygame.draw.line(display_surface, WHITE, (0, 100), (WINDOW_WIDTH, 100), 3)
    display_surface.blit(player_image, player_rect)
    display_surface.blit(burger_image, burger_rect)


def handle_clock():
    pygame.display.update()
    clock.tick(FPS)


running = True
while running:
    check_quit()
    if player_lives > 0:
        move_player()
        move_burger()
        handle_miss()
        check_collisions()
        check_game_over()
        hud_elements = update_hud()
        display_hud(hud_elements)
    else:
        check_game_over()  # Make sure the game over screen shows if player is out of lives

    handle_clock()

pygame.quit()