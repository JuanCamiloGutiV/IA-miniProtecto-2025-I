import pygame
import networkx as nx
import random
import time

# Dimensiones del laberinto (fila x columna)
ROWS, COLS = 10, 10
CELL_SIZE = 50
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Laberinto inicial
maze_layout = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 'G'],
    [1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    ['S', 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def find_position(maze, target):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == target:
                return (row, col)
    return None

def change_walls(maze):
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] != 'S' and maze[row][col] != 'G':
                if random.random() < 0.1:
                    maze[row][col] = 1 if maze[row][col] == 0 else 0

def dfs(maze, start, goal):
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)
        row, col = current

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                if maze[new_row][new_col] != 1:
                    stack.append(((new_row, new_col), path + [(new_row, new_col)]))

    return None

def draw_maze(screen, maze, rata_img, queso_img, rat_pos):
    for row in range(ROWS):
        for col in range(COLS):
            cell = maze[row][col]
            x, y = col * CELL_SIZE, row * CELL_SIZE

            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

            if cell == 1:
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
            elif cell == 'G':
                screen.blit(queso_img, (x, y))
            elif cell == 'S':
                pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

    # Dibuja la rata en su posición actual
    rat_x, rat_y = rat_pos[1] * CELL_SIZE, rat_pos[0] * CELL_SIZE
    screen.blit(rata_img, (rat_x, rat_y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Laberinto con DFS dinámico")

    clock = pygame.time.Clock()
    rata_img = pygame.image.load("rata.png")
    rata_img = pygame.transform.scale(rata_img, (CELL_SIZE, CELL_SIZE))
    queso_img = pygame.image.load("queso.png")
    queso_img = pygame.transform.scale(queso_img, (CELL_SIZE, CELL_SIZE))

    rat_pos = find_position(maze_layout, 'S')
    last_change_time = time.time()
    change_interval = 5  # Cambia paredes cada 5 segundos
    step_index = 0
    path = dfs(maze_layout, rat_pos, find_position(maze_layout, 'G'))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Si es momento de cambiar paredes
        if time.time() - last_change_time > change_interval:
            change_walls(maze_layout)
            last_change_time = time.time()
            # Recalcular camino
            path = dfs(maze_layout, rat_pos, find_position(maze_layout, 'G'))
            step_index = 0

        # Mover a la rata un paso a la vez
        if path and step_index < len(path):
            rat_pos = path[step_index]
            step_index += 1
            time.sleep(0.2)  # Velocidad de movimiento

        screen.fill(WHITE)
        draw_maze(screen, maze_layout, rata_img, queso_img, rat_pos)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
