import pygame
import socket
import pickle

pygame.init()

# Client configuration
server_ip = "127.0.0.1"
server_port = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

# Set up display
width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Multiplayer Snake Game - Client')

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

    # Initial snake position and movement
    x_snake, y_snake = width / 2, height / 2
    x_snake_change, y_snake_change = 0, 0

    # Snake body
    snake_list = []
    length_of_snake = 1

    while not game_over:
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

        # Send the snake position to the server
        snake_data = {'x': x_snake, 'y': y_snake}
        client.send(pickle.dumps(snake_data))

        # Receive updated game state from the server
        game_state_data = pickle.loads(client.recv(1024))
        if game_state_data is not None:
            # Extract relevant information from the received data
            x_snake = game_state_data['x']
            y_snake = game_state_data['y']
            snake_list = game_state_data['snake_list']

        game_display.fill(black)
        our_snake(snake_block, snake_list)

        pygame.display.update()

        # Snake speed
        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

# Start the game loop
game_loop()
