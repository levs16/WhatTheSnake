import pygame
import time
import random

pygame.init()

# Set up display
width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Snake properties
snake_block = 10
snake_speed = 15

# Fonts
font = pygame.font.SysFont(None, 40)

# Snake function
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_display, green, [x[0], x[1], snake_block, snake_block])

# Game loop
def game_loop():
    game_over = False
    game_close = False

    # Initial snake position and movement
    x_snake, y_snake = width / 2, height / 2
    x_snake_change, y_snake_change = 0, 0

    # Snake body
    snake_list = []
    length_of_snake = 1

    # Food position
    food_x, food_y = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            game_display.fill(black)
            game_over_text = font.render("Game Over! Press Q-Quit or C-Play Again", True, red)
            game_display.blit(game_over_text, [width / 6, height / 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_snake_change = -snake_block
                    y_snake_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_snake_change = snake_block
                    y_snake_change = 0
                elif event.key == pygame.K_UP:
                    y_snake_change = -snake_block
                    x_snake_change = 0
                elif event.key == pygame.K_DOWN:
                    y_snake_change = snake_block
                    x_snake_change = 0

        # Update snake position
        x_snake += x_snake_change
        y_snake += y_snake_change

        # Check if snake hits the walls
        if x_snake >= width or x_snake < 0 or y_snake >= height or y_snake < 0:
            game_close = True

        game_display.fill(black)
        pygame.draw.rect(game_display, white, [food_x, food_y, snake_block, snake_block])
        snake_head = []
        snake_head.append(x_snake)
        snake_head.append(y_snake)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check if snake eats food
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)

        pygame.display.update()

        # Check if snake eats food, generate new food
        if x_snake == food_x and y_snake == food_y:
            food_x, food_y = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        pygame.display.update()

        # Snake speed
        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

game_loop()

# NOTICE: client.py is the only thing for now, there is no servr-side as for now! But it sure will be there soon! Stay tuned for updates :3
