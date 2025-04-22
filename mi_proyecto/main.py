import pygame
import random
import time

# Dimensiones del laberinto (fila x columna)
ROWS, COLS = 10, 10
CELL_SIZE = 50
BUTTON_AREA_HEIGHT = 60
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE + BUTTON_AREA_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (150, 230, 150)
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

# Búsqueda por profundidad (Hecha por Andrés)
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
# Busqueda por profundidad

# Dibuja el laberinto y la rata
def draw_maze(screen, maze, rata_img, queso_img, rat_pos):
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE, r * CELL_SIZE
            cell = maze[r][c]
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
            if cell == 1:
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
            elif cell == 'G':
                screen.blit(queso_img, (x, y))
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)
    # Dibuja la rata
    rx, ry = rat_pos[1] * CELL_SIZE, rat_pos[0] * CELL_SIZE
    screen.blit(rata_img, (rx, ry))

# Dibuja el botón "Iniciar"
def draw_button(screen, font, button_rect, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    text_surf = font.render("Iniciar", True, BUTTON_TEXT_COLOR)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Laberinto con DFS dinámico y Botón")

    clock = pygame.time.Clock()
    rata_img = pygame.transform.scale(pygame.image.load("rata.png"), (CELL_SIZE, CELL_SIZE))
    queso_img = pygame.transform.scale(pygame.image.load("queso.png"), (CELL_SIZE, CELL_SIZE))

    font = pygame.font.SysFont(None, 36)
    # Definición del rectángulo del botón
    button_width, button_height = 120, 40
    button_x = (WIDTH - button_width) // 2
    button_y = ROWS * CELL_SIZE + (BUTTON_AREA_HEIGHT - button_height) // 2
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    rat_pos = find_position(maze_layout, 'S')
    goal_pos = find_position(maze_layout, 'G')

    last_change = time.time()
    change_interval = 5

    # Parámetros de juego
    game_started = False
    path = None
    step = 0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        hover_button = button_rect.collidepoint(mouse_pos)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif not game_started and e.type == pygame.MOUSEBUTTONDOWN:
                if hover_button:
                    game_started = True
            # No alteramos lógica de búsqueda en profundidad

        screen.fill(WHITE)
        # Siempre dibujar el laberinto y la rata en su posición inicial
        draw_maze(screen, maze_layout, rata_img, queso_img, rat_pos)

        if not game_started:
            draw_button(screen, font, button_rect, hover_button)
        else:
            # Lógica del juego una vez iniciado
            current_time = time.time()
            if rat_pos != goal_pos:
                # Cambia el laberinto periódicamente
                if current_time - last_change > change_interval:
                    change_walls(maze_layout, rat_pos, goal_pos)
                    last_change = current_time
                    path = None
                    step = 0

                # Calcula o recalcula ruta con DFS
                if path is None or step >= len(path):
                    path = dfs(maze_layout, rat_pos, goal_pos)
                    step = 0

                # Avanza si hay ruta
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
