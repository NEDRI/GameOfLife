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
                color = (255, 20, 0)
            elif grid[i][j] == 2:
                color = (55, 255, 252)
            elif grid[i][j] == 3:
                color = (0, 255, 0)
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

            if grid[i][j] == 1:
                if neighbors_team1 < 2 or neighbors_team1 > 3:
                    new_grid[i][j] = 0
                    total_team1_units -= 1
            elif grid[i][j] == 2:
                if neighbors_team2 < 2 or neighbors_team2 > 3:
                    new_grid[i][j] = 0
                    total_team2_units -= 1
            elif grid[i][j] == 3:
                if neighbors_team1 > 0 or neighbors_team2 > 0:
                    new_grid[i][j] = 0
                    spawn_count = 0
                    for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
                        if spawn_count >= 2:
                            break
                        nx, ny = (i + dx) % rows, (j + dy) % cols
                        if new_grid[nx][ny] == 0:
                            new_grid[nx][ny] = 1 if neighbors_team1 > neighbors_team2 else 2
                            spawn_count += 1
            else:
                if neighbors_team1 == 3:
                    new_grid[i][j] = 1
                    total_team1_units += 1
                elif neighbors_team2 == 3:
                    new_grid[i][j] = 2 
                    total_team2_units += 1
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
                if event.button == 1:
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
    """Read scores from file and return sorted list of (nickname, score) tuples"""
    scores = []
    try:
        with open("scores.txt", "r") as file:
            for line in file:
                try:
                    nickname, score = line.strip().split()
                    scores.append((nickname, int(score)))
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def write_score(nickname, score):
    """Save a score to the scores file"""
    with open("scores.txt", "a") as file:
        file.write(f"{nickname} {score}\n")

def get_player_nickname(team_num):
    """Get 3-letter nickname for a player"""
    nickname = ""
    font = pygame.font.SysFont(None, 55)
    while len(nickname) < 3:
        display.fill((0, 0, 0))
        prompt = font.render(f"Player {team_num} enter 3-letter nickname:", True, (255,255,255))
        name_display = font.render(nickname, True, (255,255,255))
        display.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 50))
        display.blit(name_display, (WIDTH//2 - name_display.get_width()//2, HEIGHT//2 + 20))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                elif len(nickname) < 3 and event.unicode.isalpha():
                    nickname += event.unicode.upper()
    return nickname

def display_scores():
    scores = read_scores()
    scores.sort(key=lambda x: x[1], reverse=True)
    top_scores = scores[:5]
    return top_scores

def display_end_game_results(nickname):
    global game_started, running, generation, total_team1_units, total_team2_units
    
    # Get player nicknames
    player1 = get_player_nickname(1)
    player2 = get_player_nickname(2)
    
    # Save scores
    write_score(player1, abs(total_team1_units))
    write_score(player2, abs(total_team2_units))
    
    # Show top scores
    display.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 55)
    title = font.render("TOP SCORES:", True, (255,255,255))
    display.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    scores = read_scores()[:3]  # Get top 3 scores
    y_offset = 180
    for i, (name, score) in enumerate(scores, 1):
        score_text = font.render(f"{i}. {name}: {score}", True, (255,255,255))
        display.blit(score_text, (WIDTH//2 - score_text.get_width()//2, y_offset))
        y_offset += 60
    
    # Show current game results
    result_text = f"{player1}: {abs(total_team1_units)} | {player2}: {abs(total_team2_units)}"
    winner_text = "Winner: " + (player1 if abs(total_team1_units) > abs(total_team2_units) 
    else player2 if abs(total_team2_units) > abs(total_team1_units) 
    else "Tie!")
    
    result_surface = font.render(result_text, True, (255,255,255))
    winner_surface = font.render(winner_text, True, (255,255,255))
    display.blit(result_surface, (WIDTH//2 - result_surface.get_width()//2, y_offset + 40))
    display.blit(winner_surface, (WIDTH//2 - winner_surface.get_width()//2, y_offset + 100))
    
    exit_button = pygame.Rect(WIDTH//2 - 100, y_offset + 180, 200, 50)
    pygame.draw.rect(display, (200,0,0), exit_button)
    exit_text = font.render("EXIT", True, (255,255,255))
    display.blit(exit_text, (exit_button.centerx - exit_text.get_width()//2, 
    exit_button.centery - exit_text.get_height()//2))
    
    pygame.display.flip()
    
    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
        
        if exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(display, (255,0,0), exit_button)
            if mouse_clicked:
                pygame.quit()
                exit()
        else:
            pygame.draw.rect(display, (200,0,0), exit_button)
        
        display.blit(exit_text, (exit_button.centerx - exit_text.get_width()//2, 
        exit_button.centery - exit_text.get_height()//2))
        pygame.display.flip()
        clock.tick(60)
    
    return False
    
    while len(player1_nickname) < 3:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player1_nickname = player1_nickname[:-1]
                elif len(player1_nickname) < 3 and event.unicode.isalpha():
                    player1_nickname += event.unicode.upper()
    
    while len(player2_nickname) < 3:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player2_nickname = player2_nickname[:-1]
                elif len(player2_nickname) < 3 and event.unicode.isalpha():
                    player2_nickname += event.unicode.upper()
    
    # Save scores
    save_score(player1_nickname, total_team1_units)
    save_score(player2_nickname, total_team2_units)
    
    # Display top scores
    top_scores = display_scores()
    
    # Display results
    result_text = f"Team 1 Units: {total_team1_units} | Team 2 Units: {total_team2_units}"
    winner_text = "Winner: " + ("Team 1" if total_team1_units > total_team2_units else "Team 2" if total_team2_units > total_team1_units else "It's a Tie!")
    
    result_surface = font.render(result_text, True, (255, 255, 255))
    winner_surface = font.render(winner_text, True, (255, 255, 255))
    
    # Draw buttons
    next_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
    pygame.draw.rect(display, (0, 255, 0), next_button)
    next_button_text = font.render("Next", True, (0, 0, 0))
    display.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT // 2 - 50))
    display.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 2 + 10))
    
    next_text_x = next_button.x + (next_button.width - next_button_text.get_width()) // 2
    next_text_y = next_button.y + (next_button.height - next_button_text.get_height()) // 2
    display.blit(next_button_text, (next_text_x, next_text_y))
    
    pygame.display.flip()
    
    waiting_for_next = True
    while waiting_for_next:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and next_button.collidepoint(event.pos):
                    waiting_for_next = False
                    return True
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
    
    exit_text_x = exit_button.x + (exit_button.width - exit_button_text.get_width()) // 2
    exit_text_y = exit_button.y + (exit_button.height - exit_button_text.get_height()) // 2
    display.blit(exit_button_text, (exit_text_x, exit_text_y))

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
                        return True

def generate_green_fields():
    green_count = 0
    while green_count < 200:
        x = random.randint(0, rows-1)
        y = random.randint(0, cols-1)
        if grid[x][y] == 0:
            grid[x][y] = 3
            green_count += 1

def reset_game():
    global grid, generation, total_team1_units, total_team2_units, game_started, paused, running
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    generation = 0
    total_team1_units = 0
    total_team2_units = 0
    game_started = False
    paused = False
    running = True
    generate_green_fields()
    start_button = draw_start_screen()
    return start_button

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
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if start_button.collidepoint(pos):
                    display.fill((0, 0, 0))  
                    draw_grid()  
                    pygame.display.flip()  

                    generate_green_fields()
                    placement_complete = {1: False, 2: False}

                    team1_positions = select_initial_positions(1, placement_complete) 
                    team2_positions = select_initial_positions(2, placement_complete)

                    game_started = True

    if game_started and not paused:
        update_grid()
        generation += 1
        if generation > 25:
            running = False
            final_score = total_team1_units + total_team2_units
            
            display_end_game_results("")
            pygame.display.flip()
            
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
            should_restart = display_end_game_results(nickname)
            if should_restart:
                start_button = reset_game()
                # Reset the game state and wait for start button click
                waiting_for_start = True
                while waiting_for_start:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                pos = pygame.mouse.get_pos()
                                if start_button.collidepoint(pos):
                                    waiting_for_start = False
                                    game_started = True
                                    display.fill((0, 0, 0))
                                    draw_grid()
                                    pygame.display.flip()
                                    # Reset initial positions
                                    placement_complete = {1: False, 2: False}
                                    team1_positions = select_initial_positions(1, placement_complete)
                                    team2_positions = select_initial_positions(2, placement_complete)
                                    game_started = True
        display.fill((0, 0, 0))
        draw_grid()
        draw_text(0, 0)
        pygame.display.flip()

pygame.quit()
