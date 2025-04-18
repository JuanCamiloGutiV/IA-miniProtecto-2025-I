import pygame
import networkx as nx
import random
import time

# Dimensiones del laberinto (fila x columna)
ROWS, COLS = 10, 10
CELL_SIZE = 50  # Tamaño de cada celda en píxeles
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)


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

def change_walls(maze):
    
    for row in range(ROWS):
        for col in range(COLS):
            # Solo cambiar celdas que no sean la rata o el queso
            if maze[row][col] != 'S' and maze[row][col] != 'G':
                if random.random() < 0.1:
                    maze[row][col] = 1 if maze[row][col] == 0 else 0  # Cambiar entre pared y pasaje
                    
def draw_maze(screen, maze, rata,queso):
    for row in range(ROWS):
        for col in range(COLS):
            cell = maze[row][col]
            x, y = col * CELL_SIZE, row * CELL_SIZE

            if cell == 1:
                color = BLACK  # Pared
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))  
            elif cell == 'S':
                color = WHITE
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE)) 
                screen.blit(rata, (x, y))  
            elif cell == 'G':
                color = WHITE  # Queso
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                screen.blit(queso, (x, y))  
            else:
                color = WHITE  # Espacio vacío
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))  

            # Dibuja borde alrededor de la celda
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Laberinto dinámico")

    clock = pygame.time.Clock()
    running = True
    
    rata = pygame.image.load("rata.png")  # Asegúrate de tener este archivo en la carpeta del proyecto
    rata = pygame.transform.scale(rata, (CELL_SIZE, CELL_SIZE))
    
    queso = pygame.image.load("queso.png")  # Asegúrate de tener este archivo en la carpeta del proyecto
    queso = pygame.transform.scale(queso, (CELL_SIZE, CELL_SIZE))
    
    last_change_time = time.time()  # Tiempo inicial para el cambio de paredes
    change_interval = 5
    # Bucle principal del juego
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
 
        # funcion cooldown de cambio
        if time.time() - last_change_time > change_interval:
            change_walls(maze_layout)
            last_change_time = time.time()  
            
        draw_maze(screen, maze_layout, rata, queso)

        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main()
