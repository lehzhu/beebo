import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 800
INFO_PANEL_HEIGHT = 100
SCREEN_HEIGHT = HEIGHT + INFO_PANEL_HEIGHT
CELL_SIZE = 100
GRID_SIZE = WIDTH // CELL_SIZE

RED = (244, 67, 54)
BLUE = (111, 168, 220)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen and clock
pygame.init()
screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Beebo Game')
clock = pygame.time.Clock()

# Load assets
playerRed_image = pygame.image.load('assets/redcater.jpg')
playerRed = pygame.transform.scale(playerRed_image, (CELL_SIZE, CELL_SIZE))
playerBlue_image = pygame.image.load('assets/bluecater.jpg')
playerBlue = pygame.transform.scale(playerBlue_image, (CELL_SIZE, CELL_SIZE))
playerRed_angle = 0
playerBlue_angle = 0

# Initialize move counter
RED_MOVES = 50
BLUE_MOVES = 50
font = pygame.font.Font(None, 36)

# Your grid initialization here
grid = [[WHITE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

player1_pos = [3, 3]  # Starting position
player2_pos = [4, 4]  # Starting position

while True:
    screen.fill(WHITE)

    # Draw grid lines
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))  # Vertical lines
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))  # Horizontal lines

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Player 1 Movement
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d] and RED_MOVES > 0:
                x1, y1 = player1_pos
                if event.key == pygame.K_w and y1 > 0:
                    y1 -= 1
                    player1_angle = 270
                elif event.key == pygame.K_s and y1 < GRID_SIZE - 1:
                    y1 += 1
                    player1_angle = 90
                elif event.key == pygame.K_a and x1 > 0:
                    x1 -= 1
                    player1_angle = 180
                elif event.key == pygame.K_d and x1 < GRID_SIZE - 1:
                    x1 += 1
                    player1_angle = 0
                player1_pos = x1, y1
                grid[y1][x1] = RED
                RED_MOVES -= 1  # Decrement player 1 move counter

            # Player 2 Movement
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] and BLUE_MOVES > 0:
                x2, y2 = player2_pos
                if event.key == pygame.K_UP and y2 > 0:
                    y2 -= 1
                    player2_angle = 270
                elif event.key == pygame.K_DOWN and y2 < GRID_SIZE - 1:
                    y2 += 1
                    player2_angle = 90
                elif event.key == pygame.K_LEFT and x2 > 0:
                    x2 -= 1
                    player2_angle = 180
                elif event.key == pygame.K_RIGHT and x2 < GRID_SIZE - 1:
                    x2 += 1
                    player2_angle = 0
                player2_pos = x2, y2
                grid[y2][x2] = BLUE
                BLUE_MOVES -= 1  # Decrement player 2 move counter

    # Drawing the board and assets
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = grid[row][col]
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    rotated_red_grape = pygame.transform.rotate(playerRed, playerRed_angle)
    rotated_green_grape = pygame.transform.rotate(playerBlue, playerBlue_angle)
    screen.blit(rotated_red_grape, (player1_pos[0] * CELL_SIZE, player1_pos[1] * CELL_SIZE))
    screen.blit(rotated_green_grape, (player2_pos[0] * CELL_SIZE, player2_pos[1] * CELL_SIZE))

    # Draw move counter
    red_text = font.render('Red Moves: ' + str(RED_MOVES), True, BLACK)
    blue_text = font.render('Blue Moves: ' + str(BLUE_MOVES), True, BLACK)
    screen.blit(red_text, (10, HEIGHT + 10))
    screen.blit(blue_text, (WIDTH - 200, HEIGHT + 10))

    pygame.display.flip()
    clock.tick(60)
