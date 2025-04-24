import pygame
import random
import time
from collections import deque
import heapq

# Dimensiones del laberinto (fila x columna)
ROWS, COLS = 10, 10
CELL_SIZE = 50
SELECTOR_AREA_HEIGHT = 60
BUTTON_AREA_HEIGHT = 60
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + SELECTOR_AREA_HEIGHT + BUTTON_AREA_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (150, 230, 150)
BUTTON_SELECTED_COLOR = (100, 149, 237)  # Azul para el seleccionado
BUTTON_TEXT_COLOR = (0, 0, 0)

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

# Posiciones de inicio y meta
def find_position(maze, target):
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == target:
                return (r, c)
    return None

# Modificar muros dinámicamente
def change_walls(maze, rat_pos, goal_pos):
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) != rat_pos and (r, c) != goal_pos and maze[r][c] not in ('S', 'G'):
                if random.random() < 0.1:
                    maze[r][c] = 1 if maze[r][c] == 0 else 0

# Búsqueda por profundidad (Andrés)
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
        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] != 1:
                stack.append(((nr, nc), path + [(nr, nc)]))
    return None

# Búsqueda por Amplitud (Camilo)
def bfs(maze, start, goal):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] != 1:
                next_pos = (nr, nc)
                if next_pos not in visited:
                    queue.append((next_pos, path + [next_pos]))
    return None

# Búsqueda A* 
def heuristic(a, b):
    # Distancia Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze, start, goal):
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, [start]))  # f, g, nodo, camino
    visited = set()

    while open_set:
        f, g, current, path = heapq.heappop(open_set)

        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)

        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] != 1:
                next_pos = (nr, nc)
                if next_pos not in visited:
                    new_g = g + 1
                    new_f = new_g + heuristic(next_pos, goal)
                    heapq.heappush(open_set, (new_f, new_g, next_pos, path + [next_pos]))
    return None

# funcion movimiento del queso
def move_goal(maze, rat_pos):
    empty_cells = [(r, c) for r in range(ROWS) for c in range(COLS)
                   if maze[r][c] == 0 and (r, c) != rat_pos]
    if empty_cells:
        r, c = random.choice(empty_cells)
        # Limpia la posición anterior del queso
        old_goal = find_position(maze, 'G')
        if old_goal:
            maze[old_goal[0]][old_goal[1]] = 0
        maze[r][c] = 'G'
        return (r, c)
    return find_position(maze, 'G')

# Dibuja el laberinto y la rata
def draw_maze(screen, maze, rata_img, queso_img, rat_pos):
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE, r * CELL_SIZE + SELECTOR_AREA_HEIGHT
            cell = maze[r][c]
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
            if cell == 1:
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
            elif cell == 'G':
                screen.blit(queso_img, (x, y))
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)
    # Dibuja la rata
    rx, ry = rat_pos[1] * CELL_SIZE, rat_pos[0] * CELL_SIZE + SELECTOR_AREA_HEIGHT
    screen.blit(rata_img, (rx, ry))

# Dibuja el botón "Iniciar"
def draw_button(screen, font, button_rect, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    text_surf = font.render("Iniciar", True, BUTTON_TEXT_COLOR)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

# Dibuja el selector de método de búsqueda
def draw_selector(screen, font, options, selected_idx, rects, hover_idx):
    for i, opt in enumerate(options):
        rect = rects[i]
        if i == selected_idx:
            pygame.draw.rect(screen, BUTTON_SELECTED_COLOR, rect)
        elif hover_idx[i]:
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text_surf = font.render(opt, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Laberinto con Métodos de Búsqueda y Botón")

    clock = pygame.time.Clock()
    rata_img = pygame.transform.scale(pygame.image.load("rata.png"), (CELL_SIZE, CELL_SIZE))
    queso_img = pygame.transform.scale(pygame.image.load("queso.png"), (CELL_SIZE, CELL_SIZE))

    font = pygame.font.SysFont(None, 24)

    # Configuración del botón "Iniciar"
    button_width, button_height = 120, 40
    button_x = (WIDTH - button_width) // 2
    button_y = ROWS * CELL_SIZE + SELECTOR_AREA_HEIGHT + (BUTTON_AREA_HEIGHT - button_height) // 2
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Configuración del selector de método (horizontal arriba)
    options = ["Profundidad", "Amplitud", "A*"]
    values = ["dfs", "bfs", "astar"]
    selected_idx = 0
    opt_width = 150
    spacing = 10
    start_x = (WIDTH - (opt_width * len(options) + spacing * (len(options) - 1))) // 2
    selector_y = (SELECTOR_AREA_HEIGHT - button_height) // 2
    rects = [pygame.Rect(start_x + i * (opt_width + spacing), selector_y, opt_width, button_height) for i in range(len(options))]

    rat_pos = find_position(maze_layout, 'S')
    goal_pos = find_position(maze_layout, 'G')

    last_change = time.time()
    change_interval = 4
    
    last_goal_move = time.time()
    goal_interval = 4

    # Parámetros de juego
    game_started = False
    path = None
    step = 0
    method_message = ""


    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        hover_button = button_rect.collidepoint(mouse_pos)
        hover_selector = [rect.collidepoint(mouse_pos) for rect in rects]

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif not game_started and e.type == pygame.MOUSEBUTTONDOWN:
                for i, hover in enumerate(hover_selector):
                    if hover:
                        selected_idx = i

                if hover_button:
                    game_started = True
                    method_message = f"Método {options[selected_idx]} ejecutándose..."

        screen.fill(WHITE)
        draw_selector(screen, font, options, selected_idx, rects, hover_selector)
        draw_maze(screen, maze_layout, rata_img, queso_img, rat_pos)

        if not game_started:
            draw_button(screen, font, button_rect, hover_button)
        else:
            # Mostrar el texto del método en el mismo lugar que el botón
            pygame.draw.rect(screen, WHITE, button_rect)  # Borra el botón anterior
            msg_surf = font.render(method_message, True, BLACK)
            msg_rect = msg_surf.get_rect(center=button_rect.center)
            screen.blit(msg_surf, msg_rect)

            current_time = time.time()
            if rat_pos != goal_pos:
                if current_time - last_change > change_interval:
                    change_walls(maze_layout, rat_pos, goal_pos)
                    last_change = current_time
                    path = None
                    step = 0

                if current_time - last_goal_move > goal_interval:
                    goal_pos = move_goal(maze_layout, rat_pos)
                    last_goal_move = current_time
                    path = None
                    step = 0

                method = values[selected_idx]
                if path is None or step >= len(path):
                    if method == "dfs":
                        path = dfs(maze_layout, rat_pos, goal_pos)
                    elif method == "bfs":
                        path = bfs(maze_layout, rat_pos, goal_pos)
                    elif method == "astar":
                        path = astar(maze_layout, rat_pos, goal_pos)
                    step = 0

                if path:
                    rat_pos = path[step]
                    step += 1
                    time.sleep(0.2)
            else:
                print("¡La rata ha llegado al objetivo!")
                time.sleep(2)
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
