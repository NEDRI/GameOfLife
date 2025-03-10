import pygame
import random

print("pygame version:", pygame.ver)

WIDTH = 600
HEIGHT = 600
CELL_SIZE = 15
cols = WIDTH // CELL_SIZE
rows = HEIGHT // CELL_SIZE
FPS = 10

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

grid = []
for i in range(rows):
    grid.append([random.choice([0, 1, 2]) for _ in range(cols)])

def draw_grid():
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                color = (255, 20, 0)  
            elif grid[i][j] == 2:
                color = (55, 255, 252)  
            else:
                color = (0, 0, 0) 
            pygame.draw.rect(display, color,
                            (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))
    for i in range(rows):
        pygame.draw.line(display, (50, 50, 50), (0, i * CELL_SIZE),
                        (WIDTH, i * CELL_SIZE))
    for j in range(cols):
        pygame.draw.line(display, (50, 50, 50), (j * CELL_SIZE, 0),
                        (j * CELL_SIZE, HEIGHT))

def count_neighbors(x, y):
    total_team1 = 0
    total_team2 = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x + i >= 0 and x + i < rows and y + j >= 0 and y + j < cols:
                if grid[(x + i) % rows][(y + j) % cols] == 1:
                    total_team1 += 1
                elif grid[(x + i) % rows][(y + j) % cols] == 2:
                    total_team2 += 1
    return total_team1, total_team2

def update_grid():
    global grid
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            neighbors_team1, neighbors_team2 = count_neighbors(i, j)

            if grid[i][j] == 1:  
                if neighbors_team1 < 2 or neighbors_team1 > 3:
                    new_grid[i][j] = 0
            elif grid[i][j] == 2:  
                if neighbors_team2 < 2 or neighbors_team2 > 3:  
                    new_grid[i][j] = 0
            else:  
                if neighbors_team1 == 3:
                    new_grid[i][j] = 1
                elif neighbors_team2 == 3:
                    new_grid[i][j] = 2 
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
        update_grid()
        generation += 1
    
    pygame.display.flip()

pygame.quit()