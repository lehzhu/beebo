import pygame
import sys
from collections import deque

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

# Move counters, penalties, trackers
RED_MOVES = 50
BLUE_MOVES = 50
font = pygame.font.Font(None, 36)
MOVE_PENALTY = 2 #MOVE PENALTY
checked_for_red_capture = set()
checked_for_blue_capture = set()

# Your grid initialization here
grid = [[WHITE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player1_pos = [3, 3]  # Starting position
player2_pos = [4, 4]  # Starting position

def flood_fill(x, y, grid, marked):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    stack = [(x, y)]

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in marked:
            continue

        marked.add((cx, cy))

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[ny][nx] == WHITE and (nx, ny) not in marked:
                    stack.append((nx, ny))

def check_capture(x, y, color, checked_set):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    stack = [(x, y)]
    visited = set()
    is_capture = True

    while stack:
        cx, cy = stack.pop()
        visited.add((cx, cy))

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy

            if nx < 0 or nx >= GRID_SIZE or ny < 0 or ny >= GRID_SIZE:
                is_capture = False
                continue

            next_tile = grid[ny][nx]

            if next_tile == WHITE and (nx, ny) not in visited:
                stack.append((nx, ny))
            elif next_tile != color:
                is_capture = False

    if is_capture:
        for cx, cy in visited:
            grid[cy][cx] = color
    checked_set.update(visited)
    return len(visited) if is_capture else 0


def draw_grid():
    # Draw vertical lines
    for i in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (i, 0), (i, HEIGHT))
    # Draw horizontal lines
    for i in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, i), (WIDTH, i))


# game logic
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
        # Event logic after key press
        elif event.type == pygame.KEYDOWN:
            # Positions upon next move
            next_x1, next_y1 = player1_pos
            next_x2, next_y2 = player2_pos

            # Player Red Movement
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d] and RED_MOVES > 0:
                if event.key == pygame.K_w:
                    next_y1 -= 1
                elif event.key == pygame.K_s:
                    next_y1 += 1
                elif event.key == pygame.K_a:
                    next_x1 -= 1
                elif event.key == pygame.K_d:
                    next_x1 += 1

                # Collision Check
                if 0 <= next_x1 < GRID_SIZE and 0 <= next_y1 < GRID_SIZE:
                    if grid[next_y1][next_x1] == BLUE:
                        RED_MOVES -= MOVE_PENALTY  # Apply penalty
                    else:
                        RED_MOVES -= 1  # Decrement move counter
                    # If no penalty, move as usual
                    player1_pos = next_x1, next_y1
                    grid[next_y1][next_x1] = RED

            # Player Blue Movement
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] and BLUE_MOVES > 0:
                if event.key == pygame.K_UP:
                    next_y2 -= 1
                elif event.key == pygame.K_DOWN:
                    next_y2 += 1
                elif event.key == pygame.K_LEFT:
                    next_x2 -= 1
                elif event.key == pygame.K_RIGHT:
                    next_x2 += 1

                # Collision Check
                if 0 <= next_x2 < GRID_SIZE and 0 <= next_y2 < GRID_SIZE:
                    if grid[next_y2][next_x2] == RED:
                        BLUE_MOVES -= MOVE_PENALTY  # Apply penalty
                    else:
                        BLUE_MOVES -= 1  # Decrement move counter if no penalty
                    # Move as usual
                    player2_pos = next_x2, next_y2
                    grid[next_y2][next_x2] = BLUE

    # Reset checked_for_capture sets
    checked_for_red_capture.clear()
    checked_for_blue_capture.clear()
    # Check for captures and add moves to move counters
    captured_tiles_red = 0  # Initialize counters for red's captured tiles
    captured_tiles_blue = 0  # Initialize counters for blue's captured tiles
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = grid[row][col]
            if color == WHITE:
                if (row, col) not in checked_for_red_capture:
                    captured_tiles_red += check_capture(row, col, RED, checked_for_red_capture)
                if (row, col) not in checked_for_blue_capture:
                    captured_tiles_blue += check_capture(row, col, BLUE, checked_for_blue_capture)

    # Add moves back to the move counter
    RED_MOVES += captured_tiles_red // 2
    BLUE_MOVES += captured_tiles_blue // 2

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

    draw_grid()
    pygame.display.flip()
    clock.tick(60)
