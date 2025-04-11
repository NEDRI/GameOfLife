import pygame
import random
import json
import os

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

grid = [[0 for _ in range(cols)] for _ in range(rows)]

# Add green fields (team 3)
for _ in range(20):  # Spawn 20 random green fields
    x, y = random.randint(0, rows-1), random.randint(0, cols-1)
    grid[x][y] = 3

generation = 0
scores = []

def draw_grid():
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                color = (255, 20, 0)  # Red
            elif grid[i][j] == 2:
                color = (55, 255, 252)  # Cyan
            elif grid[i][j] == 3:
                color = (0, 255, 0)  # Green
            else:
                color = (0, 0, 0)  # Black
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
    total_team3 = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x + i >= 0 and x + i < rows and y + j >= 0 and y + j < cols:
                if grid[(x + i) % rows][(y + j) % cols] == 1:
                    total_team1 += 1
                elif grid[(x + i) % rows][(y + j) % cols] == 2:
                    total_team2 += 1
                elif grid[(x + i) % rows][(y + j) % cols] == 3:
                    total_team3 += 1
    return total_team1, total_team2, total_team3

def update_grid():
    global grid, scores
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            neighbors_team1, neighbors_team2, neighbors_team3 = count_neighbors(i, j)

            if grid[i][j] == 1: 
                if neighbors_team1 < 2 or neighbors_team1 > 3:
                    new_grid[i][j] = 0
            elif grid[i][j] == 2:  
                if neighbors_team2 < 2 or neighbors_team2 > 3:
                    new_grid[i][j] = 0
            elif grid[i][j] == 3:  # Green field
                if neighbors_team1 >= 1:  # If red team interacts
                    new_grid[i][j] = 1
                    scores.append(('RED', generation))
                elif neighbors_team2 >= 1:  # If cyan team interacts
                    new_grid[i][j] = 2
                    scores.append(('CYA', generation))
            else:  # Empty cell
                if neighbors_team1 == 3:
                    new_grid[i][j] = 1
                elif neighbors_team2 == 3:
                    new_grid[i][j] = 2
    grid = new_grid

def show_end_screen():
    global scores
    display.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 50)
    
    # Determine winner
    team1_score = len([s for s in scores if s[0] == 'RED'])
    team2_score = len([s for s in scores if s[0] == 'CYA'])
    winner = 'RED' if team1_score > team2_score else 'CYA'
    
    # Show winner
    winner_text = font.render(f"Winner: Team {winner}", True, (255, 255, 255))
    display.blit(winner_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
    
    # Input box for nickname
    input_box = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 20, 100, 40)
    font_small = pygame.font.SysFont(None, 30)
    nickname = ''
    active = True
    
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(nickname) > 0:
                        # Save score
                        with open('scores.json', 'a') as f:
                            json.dump({'nick': nickname[:3], 'team': winner, 'score': max(team1_score, team2_score)}, f)
                            f.write('\n')
                        active = False
                elif event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                else:
                    if len(nickname) < 3 and event.unicode.isalpha():
                        nickname += event.unicode.upper()
        
        # Draw input box
        pygame.draw.rect(display, (255, 255, 255), input_box, 2)
        text_surface = font_small.render(nickname, True, (255, 255, 255))
        display.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        prompt = font_small.render("Enter nickname (3 letters):", True, (255, 255, 255))
        display.blit(prompt, (WIDTH//2 - 120, HEIGHT//2 - 20))
        
        pygame.display.flip()
        clock.tick(30)

def draw_text(remaining_team1, remaining_team2):
    global generation
    font = pygame.font.SysFont(None, 35)
    text = font.render(f"Generation: {generation}", True, (255, 255, 255))
    display.blit(text, (10, 10))
    
    controls = font.render("SPACE: Pause  R: Restart", True, (255, 255, 255))
    display.blit(controls, (10, HEIGHT - 40))

    remaining_text = font.render(f"Team 1: {remaining_team1} | Team 2: {remaining_team2}", True, (255, 255, 255))
    display.blit(remaining_text, (10, 50))
    
    # Show top scores if any
    if scores:
        top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
        for idx, (team, score) in enumerate(top_scores):
            score_text = font.render(f"{idx+1}. {team}: {score}", True, (255, 255, 255))
            display.blit(score_text, (WIDTH - 200, 10 + idx * 30))

def select_initial_positions(team):
    selected_positions = []
    remaining_choices = 9  
    while len(selected_positions) < 9:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    x, y = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
                    if (x, y) not in selected_positions and grid[x][y] == 0:
                        selected_positions.append((x, y))
                        grid[x][y] = team
                        display.fill((0, 0, 0))
                        draw_grid()
                        if team == 1:
                            draw_text(9 - len(selected_positions), 9 - len(team2_positions))
                        else:
                            draw_text(9 - len(team1_positions), 9 - len(selected_positions))
                        pygame.display.flip()
                        pygame.time .delay(100) 
                        remaining_choices -= 1  
    return selected_positions


display.fill((0, 0, 0))
draw_grid()
draw_text(9, 9)  
pygame.display.flip()

running = True
paused = False
game_started = False

team1_positions = select_initial_positions(1)
team2_positions = select_initial_positions(2)

game_started = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:  # Restart game
                grid = [[0 for _ in range(cols)] for _ in range(rows)]
                # Add new green fields
                for _ in range(20):
                    x, y = random.randint(0, rows-1), random.randint(0, cols-1)
                    grid[x][y] = 3
                generation = 0
                game_started = False
                team1_positions = select_initial_positions(1)
                team2_positions = select_initial_positions(2)
                game_started = True

    if game_started and not paused:
        update_grid()
        generation += 1
        display.fill((0, 0, 0))
        draw_grid()
        draw_text(0, 0)
        pygame.display.flip()
        
        if generation >= 40:  # End game after 40 generations
            game_started = False
            show_end_screen()

pygame.quit()