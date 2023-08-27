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
MOVE_PENALTY = 2  # MOVE PENALTY
checked_for_red_capture = set()
checked_for_blue_capture = set()

# Your grid initialization here
grid = [[WHITE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player1_pos = [3, 3]  # Starting position
player2_pos = [4, 4]  # Starting position


def flood_fill(x, y, grid, marked, exclude_colors):
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in marked or grid[cy][cx] in exclude_colors:
            continue

        marked.add((cx, cy))

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                stack.append((nx, ny))


def check_for_capture(player_color):
    global RED_MOVES, BLUE_MOVES

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == WHITE:
                marked = set()
                flood_fill(x, y, grid, marked, [player_color])

                touches_edge = any(x == 0 or x == GRID_SIZE - 1 or y == 0 or y == GRID_SIZE - 1 for x, y in marked)
                if not touches_edge:
                    color = None
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                            neighbor_color = grid[ny][nx]
                            if neighbor_color in [RED, BLUE]:
                                if color is None:
                                    color = neighbor_color
                                elif color != neighbor_color:
                                    color = None
                                    break

                    if color is not None and color == player_color:
                        for cx, cy in marked:
                            grid[cy][cx] = color

                        if color == RED:
                            RED_MOVES += len(marked) // 1
                        else:
                            BLUE_MOVES += len(marked) // 1


def check_for_opponent_capture(player_color, opponent_color):
    global RED_MOVES, BLUE_MOVES
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] != opponent_color:
                continue

            marked = set()
            flood_fill(x, y, grid, marked, {player_color, WHITE})

            touches_edge = any(
                x == 0 or x == GRID_SIZE - 1 or y == 0 or y == GRID_SIZE - 1 for x, y in marked
            )

            if not touches_edge:
                # At this point, we know that opponent squares are completely enclosed
                for cx, cy in marked:
                    grid[cy][cx] = player_color

                if player_color == RED:
                    RED_MOVES += len(marked)
                else:
                    BLUE_MOVES += len(marked)


def count_tiles(color):
    return sum(row.count(color) for row in grid)


def draw_restart_button():
    button_color = (0, 128, 0)
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40)
    pygame.draw.rect(screen, button_color, button_rect)

    button_text = font.render("Restart", True, WHITE)
    screen.blit(button_text, (button_rect.x + 15, button_rect.y + 10))

    return button_rect


def draw_grid():
    # Draw vertical lines
    for i in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (i, 0), (i, HEIGHT))
    # Draw horizontal lines
    for i in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, i), (WIDTH, i))


def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = grid[row][col]
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    rotated_red = pygame.transform.rotate(playerRed, playerRed_angle)
    rotated_blue = pygame.transform.rotate(playerBlue, playerBlue_angle)
    screen.blit(rotated_red, (player1_pos[0] * CELL_SIZE, player1_pos[1] * CELL_SIZE))
    screen.blit(rotated_blue, (player2_pos[0] * CELL_SIZE, player2_pos[1] * CELL_SIZE))

last_player1_pos = None
last_player2_pos = None

# game logic
def main_game_loop():
    global player1_pos, last_player1_pos, player2_pos, last_player2_pos
    global RED_MOVES, BLUE_MOVES
    while True:
        screen.fill(WHITE)

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
                        grid[next_y1][next_x1] = RED
                        player1_pos = next_x1, next_y1

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
                        grid[next_y2][next_x2] = BLUE
                        player2_pos = next_x2, next_y2
        # Capture code
        if player1_pos != last_player1_pos:  # if RED moved
            check_for_capture(RED)
            check_for_opponent_capture(RED, BLUE)
            last_player1_pos = player1_pos  # Update last known position

        if player2_pos != last_player2_pos:  # if BLUE moved
            check_for_capture(BLUE)
            check_for_opponent_capture(BLUE, RED)
            last_player2_pos = player2_pos  # Update last known position

        # End screen
        if RED_MOVES <= 0 and BLUE_MOVES <= 0:  # All moves are depleted
            red_score = count_tiles(RED)
            blue_score = count_tiles(BLUE)

            screen.fill(WHITE)  # Wipe the screen

            if red_score > blue_score:
                victory_text = font.render("Red Wins!", True, BLACK)
            elif blue_score > red_score:
                victory_text = font.render("Blue Wins!", True, BLACK)
            else:
                victory_text = font.render("It's a Tie!", True, BLACK)

            screen.blit(victory_text,
                        (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2))

            button_rect = draw_restart_button()

            pygame.display.flip()
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if button_rect.collidepoint(mouse_pos):
                            waiting_for_restart = False
                            # Initialize game state here for restarting
                            # For example, reset all your global variables

                            main_game_loop()  # Start a new game by calling your main loop function

        draw_board()
        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))  # Vertical lines
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))  # Horizontal lines
        # Draw move counter
        red_text = font.render('Red Moves: ' + str(RED_MOVES), True, BLACK)
        blue_text = font.render('Blue Moves: ' + str(BLUE_MOVES), True, BLACK)
        screen.blit(red_text, (10, HEIGHT + 10))
        screen.blit(blue_text, (WIDTH - 200, HEIGHT + 10))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_game_loop()
