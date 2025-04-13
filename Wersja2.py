import pygame
import random

print("pygame version:", pygame.ver)

WIDTH = 800
HEIGHT = 800
CELL_SIZE = 15
cols = WIDTH // CELL_SIZE
rows = HEIGHT // CELL_SIZE
FPS = 5

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

grid = [[0 for _ in range(cols)] for _ in range(rows)]

generation = 0
total_team1_units = 0
total_team2_units = 0

def draw_grid():
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                color = (255, 20, 0)  # Red - Team 1
            elif grid[i][j] == 2:
                color = (55, 255, 252)  # Cyan - Team 2
            elif grid[i][j] == 3:
                color = (0, 255, 0)  # Green - Team 3
            else:
                color = (0, 0, 0)  # Black - Empty
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
                cell = grid[(x + i) % rows][(y + j) % cols]
                if cell == 1:
                    total_team1 += 1
                elif cell == 2:
                    total_team2 += 1
                elif cell == 3:
                    total_team3 += 1
    return total_team1, total_team2, total_team3

def update_grid():
    global grid, total_team1_units, total_team2_units
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            neighbors_team1, neighbors_team2, neighbors_team3 = count_neighbors(i, j)

            if grid[i][j] == 1:  # Team 1
                if neighbors_team1 < 2 or neighbors_team1 > 3:
                    new_grid[i][j] = 0
                    total_team1_units -= 1
            elif grid[i][j] == 2:  # Team 2
                if neighbors_team2 < 2 or neighbors_team2 > 3:
                    new_grid[i][j] = 0
                    total_team2_units -= 1
            elif grid[i][j] == 3:  # Team 3
                # Green boxes don't interact with each other
                # But disappear when interacting with teams
                if neighbors_team1 > 0 or neighbors_team2 > 0:
                    new_grid[i][j] = 0  # Remove the green box
                    spawn_count = 0
                    for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
                        if spawn_count >= 2:
                            break
                        nx, ny = (i + dx) % rows, (j + dy) % cols
                        if new_grid[nx][ny] == 0:
                            new_grid[nx][ny] = 1 if neighbors_team1 > neighbors_team2 else 2
                            spawn_count += 1
            else:  # Dead cell
                if neighbors_team1 == 3:
                    new_grid[i][j] = 1
                    total_team1_units += 1
                elif neighbors_team2 == 3:
                    new_grid[i][j] = 2 
                    total_team2_units += 1
                # Removed green box creation rule
    grid = new_grid

def draw_text(remaining_team1, remaining_team2):
    global generation 
    font = pygame.font.SysFont(None, 35)
    text = font.render(f"Generation: {generation}", True, (255, 255, 255))
    display.blit(text, (10, 10))
    
    controls = font.render("Press SPACE to pause/unpause", True, (255, 255, 255))
    display.blit(controls, (10, HEIGHT - 40))

    if remaining_team1 > 0:
        remaining_text = font.render(f"Team 1 chose left: {remaining_team1}", True, (255, 255, 255))
    else:
        remaining_text = font.render(f"Team 2 chose left: {remaining_team2}", True, (255, 255, 255))
    
    display.blit(remaining_text, (10, 50))

def select_initial_positions(team, placement_complete):
    selected_positions = []  
    remaining_choices = 10  
    remaining_choices = 10  
    while len(selected_positions) < 10:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    x, y = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
                    if (x, y) not in selected_positions and grid[x][y] == 0 and not placement_complete[team] and not game_started:
                        selected_positions.append((x, y))
                        grid[x][y] = team
                        display.fill((0, 0, 0))
                        draw_grid()
                        draw_text(10 - len(selected_positions), remaining_choices - 1) 
                        pygame.display.flip()
                        pygame.time .delay(100) 
                        remaining_choices -= 1  
                        if len(selected_positions) == 10:
                            placement_complete[team] = True 
    return selected_positions

def read_scores():
    """Read scores from the scores.txt file."""
    scores = []
    try:
        with open("scores.txt", "r") as file:
            for line in file:
                nickname, score = line.split()
                scores.append((nickname, int(score)))
    except FileNotFoundError:
        pass  # If the file doesn't exist, return an empty list
    return scores

def write_score(nickname, score):
    """Write a new score to the scores.txt file."""
    with open("scores.txt", "a") as file:
        file.write(f"{nickname} {score}\n")

def display_scores():
    """Display the top scores."""
    scores = read_scores()
    scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score, descending
    top_scores = scores[:5]  # Get top 5 scores
    return top_scores

def display_end_game_results(nickname): 
    global game_started  # Ensure game_started is accessible
    display.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 55)
    result_text = f"Team 1 Units: {total_team1_units} | Team 2 Units: {total_team2_units}"
    winner_text = "Winner: " + ("Team 1" if total_team1_units > total_team2_units else "Team 2" if total_team2_units > total_team1_units else "It's a Tie!")

    team1_units = sum(row.count(1) for row in grid)  
    team2_units = sum(row.count(2) for row in grid)  
    result_text = f"Team 1 Units: {team1_units} | Team 2 Units: {team2_units}"
    winner_text = "Winner: " + ("Team 1" if team1_units > team2_units else "Team 2" if team2_units > team1_units else "It's a Tie!")
    
    result_surface = font.render(result_text, True, (255, 255, 255))
    winner_surface = font.render(winner_text, True, (255, 255, 255))
    
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
    
    pygame.draw.rect(display, (255, 0, 0), exit_button)
    pygame.draw.rect(display, (0, 255, 0), restart_button)
    
    exit_button_text = font.render("Exit", True, (0, 0, 0))
    restart_button_text = font.render("Restart", True, (0, 0, 0))
    
    display.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT // 2 - 50))
    display.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 2 + 10))
    display.blit(exit_button_text, (exit_button.x + 70, exit_button.y + 10))

    restart_text_x = restart_button.x + (restart_button.width - restart_button_text.get_width()) // 2
    restart_text_y = restart_button.y + (restart_button.height - restart_button_text.get_height()) // 2
    display.blit(restart_button_text, (restart_text_x, restart_text_y))
    
    pygame.display.flip()
    
    waiting_for_exit = True
    while waiting_for_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if exit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                    elif restart_button.collidepoint(event.pos):
                        reset_game()
                        waiting_for_exit = False
                        return  # Exit the results screen

def generate_green_fields():
    """Generate 100 random green fields at game start"""
    green_count = 0
    while green_count < 100:
        x = random.randint(0, rows-1)
        y = random.randint(0, cols-1)
        if grid[x][y] == 0:
            grid[x][y] = 3  # Team 3 (green)
            green_count += 1

def reset_game():
    global grid, generation, total_team1_units, total_team2_units, game_started, paused
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    generation = 0
    total_team1_units = 0
    total_team2_units = 0
    game_started = False
    paused = False
    generate_green_fields()  # Generate green fields before drawing screen
    draw_start_screen()

def draw_start_screen():
    display.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 55)
    title = font.render("Game of Life", True, (255, 255, 255))
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
    pygame.draw.rect(display, (0, 255, 0), start_button)
    button_text = font.render("Start", True, (0, 0, 0))
    display.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
    display.blit(button_text, (start_button.x + 50, start_button.y + 25))
    pygame.display.flip()
    return start_button

start_button = draw_start_screen()

running = True
paused = False
game_started = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()
                if start_button.collidepoint(pos):
                    display.fill((0, 0, 0))  
                    draw_grid()  
                    pygame.display.flip()  

                    generate_green_fields()  # Generate green fields before player selection
                    placement_complete = {1: False, 2: False}

                    team1_positions = select_initial_positions(1, placement_complete) 
                    team2_positions = select_initial_positions(2, placement_complete)

                    game_started = True

    if game_started and not paused:
        update_grid()
        generation += 1
        if generation > 25:  # Changed from >= to > to allow generation 25 to complete
            running = False
            # Calculate final score (total units)
            final_score = total_team1_units + total_team2_units
            
            # Display end game results
            display_end_game_results("")  # Pass empty string for nickname
            pygame.display.flip()
            
            # Get nickname input
            nickname = ""
            input_active = True
            while input_active and len(nickname) < 3:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and len(nickname) >= 3:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            nickname = nickname[:-1]
                        elif len(nickname) < 3 and event.unicode.isalpha():
                            nickname += event.unicode.upper()
            
            write_score(nickname, final_score)
            display_end_game_results(nickname)
        display.fill((0, 0, 0))
        draw_grid()
        draw_text(0, 0)
        pygame.display.flip()

pygame.quit()
