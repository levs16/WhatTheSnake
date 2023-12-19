import pygame
import socket
import pickle
import sys

pygame.init()

# Set up display
width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Multiplayer Snake Game - Client')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Fonts
font_large = pygame.font.SysFont(None, 60)
font_medium = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 30)

# Function to display text on the screen
def display_text(text, font, color, position):
    text_surface = font.render(text, True, color)
    game_display.blit(text_surface, position)

# Function to handle the start screen
def start_screen():
    nickname_input = input("Enter your nickname: ")
    server_ip_input = input("Enter the server IP: ")
    color_input = input("Enter your preferred color (e.g., red, green, blue): ")

    return nickname_input, server_ip_input, color_input

# Get user inputs for nickname, server IP, and color
nickname, server_ip, preferred_color = start_screen()

# Convert color string to a pygame color
try:
    player_color = pygame.Color(preferred_color)
except ValueError:
    print("Invalid color. Using default color (green).")
    player_color = pygame.Color("green")

# Client configuration
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, 5555))  # Assuming the server port is fixed at 5555

# Set up display
width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Multiplayer Snake Game - Client')

# Snake properties
snake_block = 10
snake_speed = 15

# Fonts
font = pygame.font.SysFont(None, 40)

# Snake function with nickname display
def our_snake(snake_list, nickname):
    for x in snake_list:
        pygame.draw.rect(game_display, player_color, [x[0], x[1], snake_block, snake_block])
        nickname_text = font.render(nickname, True, player_color)
        game_display.blit(nickname_text, [x[0] - 5, x[1] - 15])

# Game loop
def game_loop():
    waiting_for_players = True
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

        if waiting_for_players:
            game_display.fill(black)
            display_text("Waiting for more players to join...", font_large, white, (100, height / 2 - 30))
            pygame.display.update()

            # Receive updated game state from the server
            game_state_data = pickle.loads(client.recv(1024))
            if game_state_data is not None:
                # Extract relevant information from the received data
                players_data = game_state_data['players']
                if len(players_data) > 1:
                    waiting_for_players = False

        else:
            # Send the snake position and nickname to the server
            snake_data = {'x': x_snake, 'y': y_snake, 'snake_list': snake_list, 'nickname': nickname}
            client.send(pickle.dumps(snake_data))

            # Receive updated game state from the server
            game_state_data = pickle.loads(client.recv(1024))
            if game_state_data is not None:
                # Extract relevant information from the received data
                players_data = game_state_data['players']
                for player_id, player_data in players_data.items():
                    x_snake = player_data['x']
                    y_snake = player_data['y']
                    snake_list = player_data['snake_list']

            game_display.fill(black)
            our_snake(snake_list, nickname)

            pygame.display.update()

            # Snake speed
            pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    sys.exit()

# Start the game loop
game_loop()
