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
    #wielkosc bloków
    blockSize = 20
    cellSize = 20
    #kolory komórek
    aliveColor = (0, 245, 255)
    deadColor = (255, 110 ,20)

    def drawGrid():
        for x in range(0, winWidth, blockSize):
            for y in range(0, winHeight, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(screen, grey, rect, 1)

    def drawCells():
        pygame.draw.rect(screen, aliveColor, pygame.Rect(20, 20, cellSize, cellSize))
        pygame.draw.rect(screen, deadColor, pygame.Rect(40, 40, cellSize, cellSize))
        

    screen.fill("white")
    drawGrid()
    drawCells()


    pygame.display.flip()
    clock.tick(10)
pygame.quit()
