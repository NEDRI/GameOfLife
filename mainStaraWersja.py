import pygame
import random

print("pygame version:", pygame.ver)

WIDTH = 800
HEIGHT = 800
CELL_SIZE = 15
cols = WIDTH // CELL_SIZE
rows = HEIGHT // CELL_SIZE
FPS = 10

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

def draw_grid():
    for i in range(rows):
        for j in range(cols):
            color = (255, 20, 0) if grid[i][j] == 1 else (0, 0, 0)
            pygame.draw.rect(display, color,
                             (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))
    for i in range(rows):
        pygame.draw.line(display, (50, 50, 50), (0, i * CELL_SIZE),
                         (WIDTH, i * CELL_SIZE))
    for j in range(cols):
        pygame.draw.line(display, (50, 50, 50), (j * CELL_SIZE, 0),
                         (j * CELL_SIZE, HEIGHT))

def count_neighbors(x, y):
    total_neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0): 
                continue
            if 0 <= x + i < rows and 0 <= y + j < cols:
                total_neighbors += grid[x + i][y + j]
    return total_neighbors

def update_grid():
    global grid
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            neighbors = count_neighbors(i, j)

            if grid[i][j] == 1: 
                if neighbors < 2 or neighbors > 3:
                    new_grid[i][j] = 0 
            else: 
                if neighbors == 3:
                    new_grid[i][j] = 1  
    grid = new_grid

def draw_text():
    font = pygame.font.SysFont(None, 35)
    text = font.render(f"Generation: {generation}", True, (255, 255, 255))
    display.blit(text, (10, 10))
    
    controls = font.render("Press SPACE to pause/unpause", True, (255, 255, 255))
    display.blit(controls, (10, HEIGHT - 40))

running = True
paused = False
generation = 0

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

    display.fill((0, 0, 0))
    
    draw_grid()
    draw_text()
    
    if not paused:
        if generation < 100:
            update_grid()
            generation += 1
        else:
            paused = True
    
    pygame.display.flip()

pygame.quit()