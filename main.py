import sys, pygame, numpy

print("pygame version:", pygame.ver)
print("numpy version:", numpy.__version__)

pygame.init()
winHeight = 800
winWidth = 800
screen = pygame.display.set_mode((winHeight, winWidth))
pygame.display.set_caption("Gra w życie")
clock = pygame.time.Clock()
running = True

while running:

    # zamykanie programu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #kolory
    white= (255, 255, 255)
    black = (0, 0, 0)
    grey = (200, 200, 200)
    #wielkosc grid
    blockSize = 20
    #kolory komórek
    aliveColor = (0, 245, 255)
    deadColor = (255, 109 ,0)

    def drawGrid():
        for x in range(0, winWidth, blockSize):
            for y in range(0, winHeight, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(screen, grey, rect, 1)

    screen.fill("white")
    drawGrid()

    pygame.display.flip()
    clock.tick(10)
pygame.quit()
