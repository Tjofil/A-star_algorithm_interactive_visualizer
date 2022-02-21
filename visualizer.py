from time import sleep
import pygame
from tkinter import *
from tkinter import ttk
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Visualizer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

NUM_COL, NUM_ROW = 50, 50
VER_WIDTH, VER_HEIGHT = WIDTH//NUM_COL, HEIGHT//NUM_ROW

obstacle_mode = True
window = 0
destroyed_manually = False

class Vertex:
    DEF_COLOR = WHITE
    OBS_COLOR = GREEN
    PNT_COLOR = RED
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = self.DEF_COLOR
        self.obs = False
        self.pnt = True
    def display(self, win):
        pygame.draw.rect(win, self.color ,(self.x*VER_WIDTH, self.y*VER_HEIGHT, VER_WIDTH-2, VER_HEIGHT-2) )
        #print(f'{self.x*VER_WIDTH}, {self.y*VER_HEIGHT} tried to be drawn.')

    def set_obstacle(self):
        self.color = self.OBS_COLOR
        self.obs = True

    def set_point(self):
        self.color = self.PNT_COLOR
        self.pnt = True

    def reset(self):
        self.color = self.DEF_COLOR
        self.pnt = False


def on_done():
    global obstacle_mode
    global window
    global destroyed_manually
    obstacle_mode = False
    destroyed_manually = True
    window.quit()

def on_resume():
    global window
    global destroyed_manually
    destroyed_manually = True
    window.quit()

def draw(win, grid):
    win.fill(BLACK)
    for i in range(NUM_ROW):
        for j in range(NUM_COL):
            grid[i][j].display(win)
    pygame.display.update()

def main():
    grid = [0 for _ in range(NUM_ROW)]
    for i in range(NUM_ROW):
        grid[i] = [0 for _ in range(NUM_COL)]

    for i in range(NUM_ROW):
        for j in range(NUM_COL):
            grid[i][j] = Vertex(i , j)

    run = True

    draw(WIN, grid)
    global obstacle_mode
    ready_for_simulation = False
    points = [[0, 0], [0, 0]]

    while run:     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if obstacle_mode:
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
                elif not ready_for_simulation:
                    pos = pygame.mouse.get_pos()
                    points[0] = [pos[0]//VER_WIDTH, pos[1]//VER_HEIGHT]
                    grid[points[0][0]][points[0][1]].set_point()
                    draw(WIN, grid)
                    inner = True
                    while inner:
                        for event2 in pygame.event.get():
                            if event2.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                points[1] = [pos[0]//VER_WIDTH, pos[1]//VER_HEIGHT]
                                if (points[1] == points[0]):
                                    continue
                                grid[points[1][0]][points[1][1]].set_point()
                                draw(WIN, grid)
                                inner = False
                                ready_for_simulation = True
                                break
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_r]:
                            grid[points[0][0]][points[0][1]].reset()
                            draw(WIN, grid)
                            inner = False



        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not ready_for_simulation:
            #prompt label
            global window
            global destroyed_manually
            destroyed_manually = False
            window = Tk()
            window.geometry('205x90+850+490')
            window.title('Obstacles')
            prompt = Label(window, text='Are you done putting up obstacles?')
            prompt.place(x = 7, y = 5)
            done = Button(window, text = 'Done!', width = 10, command = on_done)
            resume = Button(window, text = 'Resume', width = 10, command = on_resume)
            done.place(x = 10, y = 50)
            resume.place(x = 115 , y = 50)
            window.mainloop()
            if destroyed_manually:
                window.destroy()
            print("ESCAPED")
        elif keys[pygame.K_SPACE] and ready_for_simulation:
            print("SIMULATION")

        elif keys[pygame.K_r]:
            grid[points[0][0]][points[0][1]].reset()
            grid[points[1][0]][points[1][1]].reset()
            draw(WIN, grid)
            ready_for_simulation = False



    pygame.quit()

if __name__ == '__main__':
    main()