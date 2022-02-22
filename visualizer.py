import pygame
from tkinter import *
from tkinter import ttk
from queue import PriorityQueue
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Visualizer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (230, 230, 250)

NUM_COL, NUM_ROW = 50, 50
VER_WIDTH, VER_HEIGHT = WIDTH//NUM_COL, HEIGHT//NUM_ROW

obstacle_mode = True
window = 0
destroyed_manually = False

class Vertex:
    DEF_COLOR = WHITE
    OBS_COLOR = GREEN
    PNT_COLOR = RED
    VST_COLOR = BLUE
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = self.DEF_COLOR
        self.obs = False
        self.pnt = False
        self.vst = False
        self.neighbours = []
        self.dst = -1

    def display(self, win):
        pygame.draw.rect(win, self.color ,(self.x*VER_WIDTH, self.y*VER_HEIGHT, VER_WIDTH-2, VER_HEIGHT-2))
        #print(f'{self.x*VER_WIDTH}, {self.y*VER_HEIGHT} tried to be drawn.')

    def set_obstacle(self):
        self.color = self.OBS_COLOR
        self.obs = True

    def set_point(self):
        self.color = self.PNT_COLOR
        self.pnt = True

    def set_visit(self, start, end):
        if start != self and end != self:
            self.color = self.VST_COLOR
        self.vst = True

    def is_visited(self):
        return self.vst

    def reset(self):
        self.color = self.DEF_COLOR
        self.pnt = False
        self.obs = False
        self.vst = False

    def appoint_neighbours(self, grid):
        if self.obs:
            return
        if self.x > 0 and not grid[self.x-1][self.y].obs:
            self.neighbours.append(grid[self.x-1][self.y])
        if self.x < NUM_COL - 1 and not grid[self.x+1][self.y].obs:
            self.neighbours.append(grid[self.x+1][self.y])
        if self.y > 0 and not grid[self.x][self.y-1].obs:
            self.neighbours.append(grid[self.x][self.y-1])
        if self.y < NUM_ROW - 1 and not grid[self.x][self.y+1].obs:
            self.neighbours.append(grid[self.x][self.y+1])


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

def prepare_simulation(grid):
    for row in grid:
        for vertex in row:
            vertex.appoint_neighbours(grid)


def simulation(win, grid, points):
    pq = PriorityQueue()
    fifofy = 0
    grid[points[0][0]][points[0][1]].dst = 0
    pq.put((0, fifofy, grid[points[0][0]][points[0][1]]))
    fifofy+=1
    while not pq.empty():
        next = pq.get()
        next[2].set_visit(grid[points[0][0]][points[0][1]], grid[points[1][0]][points[1][1]])
        next[2].display(win)
        pygame.display.update()
        if next[2] == grid[points[1][0]][points[1][1]]:
            break
        for neighbour in next[2].neighbours:
            if next[0] + 1 < neighbour.dst or neighbour.dst == -1:
                pq.put((next[0] + 1, fifofy, neighbour))
                neighbour.dst = next[0] + 1
                fifofy+=1

    pygame.display.update()
    print("Done")



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
        if keys[pygame.K_SPACE] and obstacle_mode:
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
            ready_for_simulation = False
            prepare_simulation(grid)
            simulation(WIN, grid, points)
        elif keys[pygame.K_r]:
            grid[points[0][0]][points[0][1]].reset()
            grid[points[1][0]][points[1][1]].reset()
            draw(WIN, grid)
            ready_for_simulation = False



    pygame.quit()

if __name__ == '__main__':
    main()