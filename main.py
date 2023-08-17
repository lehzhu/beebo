import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
BOARD_SIZE = 8
TILE_SIZE = 64
WIDTH, HEIGHT = BOARD_SIZE * TILE_SIZE, BOARD_SIZE * TILE_SIZE
PLAYER1_COLOR = (255, 0, 0)
PLAYER2_COLOR = (0, 0, 255)
NECTAR_COLOR = (255, 255, 0)
BACKGROUND_COLOR = (220, 220, 220)
NEUTRAL_COLOR = (150, 150, 150)

# Initialize the display and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Beebo Conquest')
clock = pygame.time.Clock()

ownership = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
player_positions = {'P1': (1, 1), 'P2': (6, 6)}
nectar_points = [(random.randint(0, 7), random.randint(0, 7)) for _ in range(3)]


def draw_board():
    screen.fill(NEUTRAL_COLOR)

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            color = NEUTRAL_COLOR
            if ownership[y][x] == 'P1':
                color = PLAYER1_COLOR
            elif ownership[y][x] == 'P2':
                color = PLAYER2_COLOR

            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)

            if (y, x) in nectar_points:
                pygame.draw.circle(screen, NECTAR_COLOR, rect.center, TILE_SIZE // 4)

    # Drawing Beebo heads
    pygame.draw.circle(screen, (0, 0, 0), (
    player_positions['P1'][1] * TILE_SIZE + TILE_SIZE // 2, player_positions['P1'][0] * TILE_SIZE + TILE_SIZE // 2),
                       TILE_SIZE // 3)
    pygame.draw.circle(screen, (0, 0, 0), (
    player_positions['P2'][1] * TILE_SIZE + TILE_SIZE // 2, player_positions['P2'][0] * TILE_SIZE + TILE_SIZE // 2),
                       TILE_SIZE // 3)

    pygame.display.flip()


def move_player(player, direction):
    y, x = player_positions[player]

    if direction == "UP":
        y -= 1
    elif direction == "DOWN":
        y += 1
    elif direction == "LEFT":
        x -= 1
    elif direction == "RIGHT":
        x += 1

    # Ensure within bounds
    if 0 <= y < BOARD_SIZE and 0 <= x < BOARD_SIZE:
        player_positions[player] = (y, x)
        ownership[y][x] = player

        # Check for nectar
        if (y, x) in nectar_points:
            nectar_points.remove((y, x))
            # Add more power-ups or abilities here


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d):
                if event.key == pygame.K_w:
                    move_player('P1', 'UP')
                elif event.key == pygame.K_s:
                    move_player('P1', 'DOWN')
                elif event.key == pygame.K_a:
                    move_player('P1', 'LEFT')
                elif event.key == pygame.K_d:
                    move_player('P1', 'RIGHT')
            elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                if event.key == pygame.K_UP:
                    move_player('P2', 'UP')
                elif event.key == pygame.K_DOWN:
                    move_player('P2', 'DOWN')
                elif event.key == pygame.K_LEFT:
                    move_player('P2', 'LEFT')
                elif event.key == pygame.K_RIGHT:
                    move_player('P2', 'RIGHT')

    draw_board()
    clock.tick(10)

pygame.quit()
sys.exit()
