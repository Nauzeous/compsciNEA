import pygame
pygame.init()
import sys

screen = pygame.display.set_mode((600,400))
White = (255,255,255)
screen.fill(White)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        screen.fill(White)
        pygame.display.update()
            