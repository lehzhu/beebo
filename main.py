import pygame
import sys

# Constants
SCREEN_SIZE = 500
GRID_SIZE = 8
CELL_SIZE = SCREEN_SIZE // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
NEUTRAL = (128, 128, 128)

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Beebo Strategic Game")

clock = pygame.time.Clock()

# Initialize game state
grid = [[NEUTRAL for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player1_pos = (0, 0)
player2_pos = (7, 7)
grid[0][0] = RED
grid[7][7] = BLUE
current_player = RED

def draw_grid():
    for x in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_SIZE))
    for y in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_SIZE, y))

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            x1, y1 = player1_pos
            if event.key == pygame.K_w and y1 > 0:
                y1 -= 1
            elif event.key == pygame.K_s and y1 < GRID_SIZE - 1:
                y1 += 1
            elif event.key == pygame.K_a and x1 > 0:
                x1 -= 1
            elif event.key == pygame.K_d and x1 < GRID_SIZE - 1:
                x1 += 1
            player1_pos = x1, y1
            grid[y1][x1] = RED

            x2, y2 = player2_pos
            if event.key == pygame.K_UP and y2 > 0:
                y2 -= 1
            elif event.key == pygame.K_DOWN and y2 < GRID_SIZE - 1:
                y2 += 1
            elif event.key == pygame.K_LEFT and x2 > 0:
                x2 -= 1
            elif event.key == pygame.K_RIGHT and x2 < GRID_SIZE - 1:
                x2 += 1
            player2_pos = x2, y2
            grid[y2][x2] = BLUE


    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = grid[row][col]
            pygame.draw.rect(screen, color, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    draw_grid()

    pygame.display.flip()
    clock.tick(60)
