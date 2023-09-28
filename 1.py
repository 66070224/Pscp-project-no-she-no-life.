import pygame
pygame.init

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pygame Tutorial")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        #elif event.type == pygame.KEYDOWN:


    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (255, 0, 0), (600, 600, 200, 100))

    clock.tick(60)
    pygame.display.update()