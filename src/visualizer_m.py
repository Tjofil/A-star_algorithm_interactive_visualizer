import pygame
from grid import *
    
def main():
    grid = Grid()
    clock = pygame.time.Clock()

    while grid.is_running():
        clock.tick(FPS)
        grid.decide()
    pygame.quit()

if __name__ == '__main__':
    main()