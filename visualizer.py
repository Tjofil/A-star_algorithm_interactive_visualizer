import pygame
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Visualizer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)

NUM_COL, NUM_ROW = 50, 50
VER_WIDTH, VER_HEIGHT = WIDTH//NUM_COL, HEIGHT//NUM_ROW



class Vertex:
    DEF_COLOR = WHITE
    OBS_COLOR = GREEN
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = self.DEF_COLOR
        self.obs = False
    def display(self, win):
        pygame.draw.rect(win, self.color ,(self.x*VER_WIDTH, self.y*VER_HEIGHT, VER_WIDTH-2, VER_HEIGHT-2) )
        #print(f'{self.x*VER_WIDTH}, {self.y*VER_HEIGHT} tried to be drawn.')

    def set_obstacle(self):
        self.color = self.OBS_COLOR
        self.obs = True

def draw(win, grid):
    win.fill(BLACK)
    for i in range(NUM_ROW):
        for j in range(NUM_COL):
            grid[i][j].display(win)
    pygame.display.update()

def main():
    grid = [0 for i in range(NUM_ROW)]
    for i in range(NUM_ROW):
        grid[i] = [0 for i in range(NUM_COL)]

    for i in range(NUM_ROW):
        for j in range(NUM_COL):
            grid[i][j] = Vertex(i , j)

    run = True

    draw(WIN, grid)
   
    while run:
               
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                grid[pos[0]//VER_WIDTH][pos[1]//VER_HEIGHT].set_obstacle()
                draw(WIN, grid)
                inner = True
                while inner:
                    for event2 in pygame.event.get():
                        if event2.type == pygame.MOUSEBUTTONUP:
                            inner = False
                            break
                        else:
                            pos = pygame.mouse.get_pos()
                            grid[pos[0]//VER_WIDTH][pos[1]//VER_HEIGHT].set_obstacle()
                            draw(WIN, grid)
    pygame.quit()

if __name__ == '__main__':
    main()