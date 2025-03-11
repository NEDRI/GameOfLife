import pygame
import sys

pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mouse position display")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(f"Mouse position: ({x}, {y})")
            screen.fill((0, 0, 0))
            pygame.display.flip()

    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()