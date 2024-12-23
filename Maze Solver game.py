import pygame
import sys
import heapq

# Initialize pygame
pygame.init()

# Constants
GRID_SIZE = 25  # Increased the number of grid cells
CELL_SIZE = 24  # Increased cell size
WIDTH = GRID_SIZE * CELL_SIZE  # Width depends on the grid size and cell size
HEIGHT = GRID_SIZE * CELL_SIZE + 120  # Increased the height for more space for instructions and UI elements
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
DARK_BLUE = (50, 50, 255)
LIGHT_GRAY = (230, 230, 230)  # A lighter gray for the bottom section

# Font for instructions
font = pygame.font.SysFont('Arial', 16)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")

# Maze grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
start = (0, 0)
end = (GRID_SIZE - 1, GRID_SIZE - 1)
selecting_start = False
selecting_end = False
solving = False
path = None

def draw_grid():
    # Draw the background grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = WHITE
            if grid[y][x] == 1:
                color = BLACK
            elif (x, y) == start:
                color = GREEN
            elif (x, y) == end:
                color = RED
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search():
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and grid[neighbor[1]][neighbor[0]] == 0:
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

def draw_path(path):
    for x, y in path:
        pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_progress(current, closed_set):
    for x, y in closed_set:
        pygame.draw.rect(screen, YELLOW, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the current node being processed
    if current:
        pygame.draw.rect(screen, DARK_BLUE, (current[0] * CELL_SIZE, current[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def reset_game():
    global grid, start, end, solving, path, selecting_start, selecting_end
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Clear the grid
    start = (0, 0)  # Reset start point
    end = (GRID_SIZE - 1, GRID_SIZE - 1)  # Reset end point
    solving = False  # Stop solving
    path = None  # Clear path
    selecting_start = False  # Reset selection mode
    selecting_end = False  # Reset selection mode

def main():
    global start, end, selecting_start, selecting_end, solving, path
    clock = pygame.time.Clock()
    running = True
    closed_set = set()
    current_node = None

    while running:
        screen.fill(WHITE)
        draw_grid()

        if solving:
            if path:
                draw_path(path)
            draw_progress(current_node, closed_set)

        # Draw the instructions with more space at the bottom
        pygame.draw.rect(screen, LIGHT_GRAY, (0, HEIGHT - 120, WIDTH, 120))  # Draw a light gray area at the bottom
        draw_text("Left-click to place walls", 10, HEIGHT - 100)
        draw_text("Right-click to remove walls", 10, HEIGHT - 80)
        draw_text("Press SPACE to solve", 10, HEIGHT - 60)
        draw_text("Press R to reset", 10, HEIGHT - 40)  # Added the reset instruction
        draw_text(f"Start: {start}  End: {end}", WIDTH - 230, HEIGHT - 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE

                if event.button == 1:  # Left click to place walls
                    grid[grid_y][grid_x] = 1
                elif event.button == 3:  # Right click to remove walls
                    grid[grid_y][grid_x] = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Solve the maze
                    solving = True
                    path = a_star_search()
                elif event.key == pygame.K_b:  # Set start point
                    selecting_start = True
                    selecting_end = False
                elif event.key == pygame.K_e:  # Set end point
                    selecting_end = True
                    selecting_start = False
                elif event.key == pygame.K_r:  # Reset the game
                    reset_game()

            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if selecting_start:
                    start = (grid_x, grid_y)
                    selecting_start = False
                elif selecting_end:
                    end = (grid_x, grid_y)
                    selecting_end = False

        # Show the A* algorithm progress
        if solving:
            current_node = None
            if path is None:
                # If there's no path, show message
                draw_text("No path found!", WIDTH // 2 - 60, HEIGHT // 2, RED)
            pygame.display.flip()
            clock.tick(10)  # Slow down the update for better visualization

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()