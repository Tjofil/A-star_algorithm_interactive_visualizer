from time import sleep
import pygame
from tkinter import *
from tkinter import ttk
from queue import PriorityQueue
from math import sqrt
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Visualizer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (230, 230, 250)
DBLUE = (0, 0, 139)

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
    EDG_COLOR = DBLUE
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = self.DEF_COLOR
        self.obs = False
        self.pnt = False
        self.vst = False
        self.neighbours = []
        self.dst = -1
        self.hst = -1
        self.vst_ngh = 0
        self.prev = 0

    def display(self, win):
        pygame.draw.rect(win, self.color ,(self.x*VER_WIDTH, self.y*VER_HEIGHT, VER_WIDTH-2, VER_HEIGHT-2))

    def set_obstacle(self):
        self.color = self.OBS_COLOR
        self.obs = True

    def set_point(self):
        self.color = self.PNT_COLOR
        self.pnt = True

    def set_visit(self, start, end, prev):
        #print(f'{self.x} {self.y}')
        if self.vst: 
            print("RETARDU")
        if start != self and end != self:
            self.color = self.EDG_COLOR
        self.vst = True
        for neighbour in self.neighbours:
            neighbour.inc()
            if neighbour.vst and neighbour != start and neighbour != end:
                neighbour.tst()
        if self != start and self != end:
            self.tst()
        self.prev = prev

    def inc(self):
        self.vst_ngh += 1
    def pulse(self):
        if self.color == self.PNT_COLOR:
            return
        self.color = DBLUE
        self.display(WIN)
        pygame.display.update((self.x*VER_WIDTH, self.y*VER_HEIGHT, VER_WIDTH-2, VER_HEIGHT-2))


    def unpulse(self):
        if len(self.neighbours) != self.vst_ngh or self.color == self.PNT_COLOR:
            return
        self.color = BLUE
        self.display(WIN)
        pygame.display.update((self.x*VER_WIDTH, self.y*VER_HEIGHT, VER_WIDTH-2, VER_HEIGHT-2))

    def tst(self):
        if self.vst_ngh == len(self.neighbours):
            self.color = self.VST_COLOR
            pygame.draw.rect(WIN, self.color ,(self.x*VER_WIDTH, self.y*VER_HEIGHT, VER_WIDTH-2, VER_HEIGHT-2))
    def path(self):
            self.color = self.PNT_COLOR
            pygame.draw.rect(WIN, self.color ,(self.x*VER_WIDTH, self.y*VER_HEIGHT, VER_WIDTH-2, VER_HEIGHT-2))

        

    def reset(self):
        self.color = self.DEF_COLOR
        self.pnt = False
        self.obs = False
        self.vst = False

    def appoint_neighbours(self, grid):
        if self.obs:
            return
        y = max(0, self.x - 1)
        x = max(0, self.y - 1)
        n = min(NUM_COL - 1, self.x + 1)
        m = min(NUM_ROW - 1, self.y + 1)
        for i in range(y, n + 1):
            for j in range(x, m + 1):
                if not grid[i][j].obs and grid[i][j] != self:
                    self.neighbours.append(grid[i][j])


    def appoint_heuristic(self, end):
        self.hst = sqrt((self.x - end.x)**2 +(self.y-end.y)**2)
        #self.hst = abs(self.x - end.x) + abs(self.y - end.y)


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

def prepare_simulation(grid, end):
    for row in grid:
        for vertex in row:
            vertex.appoint_neighbours(grid)
            vertex.appoint_heuristic(end)


def simulation(win, grid, points):
    pq = PriorityQueue()
    start, end = points
    visited = []
    fifofy = 0
    start.dst = 0
    pq.put((start.hst, fifofy, Vertex(-1, -1) , start))
    fifofy+=1
    while not pq.empty():
        next = pq.get()
        next[3].set_visit(start, end, next[2])
        visited.append(next[3])
        next[3].display(win)
        pygame.display.update()
        if (len(visited) % 25 == 0):
            for vertex in visited:
                vertex.pulse()
            for vertex in visited:
                vertex.unpulse()
        if next[3] == end:
            break
        for neighbour in next[3].neighbours:
            if next[3].dst + 1 < neighbour.dst or neighbour.dst == -1:
                pq.put((next[3].dst + 1 + neighbour.hst, fifofy, next[3],neighbour))
                neighbour.dst = next[3].dst + 1
                fifofy+=1
    prev = end
    while prev != start:
            prev.path()
            prev = prev.prev
    start.path()
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
            prepare_simulation(grid, grid[points[1][0]][points[1][1]])
            simulation(WIN, grid, (grid[points[0][0]][points[0][1]], grid[points[1][0]][points[1][1]]))
        elif keys[pygame.K_r]:
            grid[points[0][0]][points[0][1]].reset()
            grid[points[1][0]][points[1][1]].reset()
            draw(WIN, grid)
            ready_for_simulation = False



    pygame.quit()

if __name__ == '__main__':
    main()