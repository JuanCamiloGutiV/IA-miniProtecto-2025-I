import pygame
import networkx as nx

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
    
    rata = pygame.image.load("rata.png")
    rata = pygame.transform.scale(rata, (CELL_SIZE, CELL_SIZE))
    
    queso = pygame.image.load("queso.png")
    queso = pygame.transform.scale(queso, (CELL_SIZE, CELL_SIZE))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_maze(screen, maze_layout, rata,queso)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
