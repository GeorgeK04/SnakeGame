import pygame as pg
import os
import sys
from random import randrange

# Constants
WINDOW_SIZE = 800
TITLE_SIZE = 50
RANGE = (TITLE_SIZE // 2, WINDOW_SIZE - TITLE_SIZE // 2, TITLE_SIZE)
TIME_STEP = 110
BLACK = (0, 0, 0)

# Function to get a random position
def get_random_position():
    return [randrange(*RANGE), randrange(*RANGE)]

# Initialize Pygame
pg.init()

# Set up the display
screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pg.display.set_caption("Snake Game")

# Load images
background_image = pg.image.load(os.path.join('Assets', 'background.png')).convert()
background_image = pg.transform.scale(background_image, (WINDOW_SIZE, WINDOW_SIZE))

food_image = pg.image.load(os.path.join('Assets', 'insect.png')).convert_alpha()
food_image = pg.transform.scale(food_image, (TITLE_SIZE, TITLE_SIZE))

# Initialize game variables
snake = pg.Rect([0, 0, TITLE_SIZE - 2, TITLE_SIZE - 2])
snake.center = get_random_position()

length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, TIME_STEP

# Initialize food_rect
food_rect = snake.copy()
food_rect.center = get_random_position()

# Initialize score variables
score = 0
font = pg.font.Font(None, 36)  # You can adjust the font size as needed

clock = pg.time.Clock()
dirs = {pg.K_w: (0, -TITLE_SIZE), pg.K_s: (0, TITLE_SIZE), pg.K_a: (-TITLE_SIZE, 0), pg.K_d: (TITLE_SIZE, 0)}

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN and event.key in dirs:
            snake_dir = dirs[event.key]

    screen.fill(BLACK)

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Check borders and self-eating
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if (
        snake.left < 0
        or snake.right > WINDOW_SIZE
        or snake.top < 0
        or snake.bottom > WINDOW_SIZE
        or self_eating
    ):
        # Reset upon losing
        snake.center, food_rect.center = get_random_position(), get_random_position()
        length, snake_dir, score = 1, (0, 0), 0
        segments = [snake.copy()]

    # Check food position
    if snake.center == food_rect.center:
        food_rect.center = get_random_position()
        length += 1
        score += 1

    # Draw food image
    screen.blit(food_image, food_rect.topleft)

    # Draw snake
    [pg.draw.rect(screen, (255, 0, 0), segment) for segment in segments]

    # Move snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]

    # Draw score on the screen
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pg.display.flip()
    clock.tick(60)
