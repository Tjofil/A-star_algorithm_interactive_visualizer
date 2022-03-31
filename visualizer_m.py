import pygame
from tkinter import *
from tkinter.ttk import *
from math import sqrt
from enum import Enum


import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
        self.fifo = 0
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item, priority: float):
        heapq.heappush(self.elements, (priority, self.fifo, item))
        self.fifo += 1
    
    def get(self):
        return heapq.heappop(self.elements)[2]


WIDTH, HEIGHT = 800, 800
NUM_COL, NUM_ROW = 50, 50
VER_WIDTH, VER_HEIGHT = WIDTH//NUM_COL, HEIGHT//NUM_ROW

BLACK = (255, 255, 255)
WHITE = (196, 238, 221)
GREEN = (109, 207, 22)
RED = (204, 39, 11)
BLUE = (184, 203, 239)
DBLUE = (38, 148, 232)

class Vertex:
    DEF_COLOR = WHITE
    OBS_COLOR = GREEN
    PNT_COLOR = RED
    VST_COLOR = BLUE
    EDG_COLOR = DBLUE
    win = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = self.DEF_COLOR
        self.obs = self.pnt = self.vst = False
        self.neighbours = []
        self.cost_so_far = self.hst = -1
        self.vst_ngh = 0
        self.came_from = None

    def display(self):

        if self.vst:
            pygame.draw.rect(self.win, BLACK ,(self.x*VER_WIDTH, self.y*VER_HEIGHT, VER_WIDTH, VER_HEIGHT))
            pygame.draw.circle(self.win, self.color, (self.x*VER_WIDTH+VER_WIDTH//2, self.y*VER_HEIGHT+VER_HEIGHT//2), VER_HEIGHT//2 + 1)
        else:
            pygame.draw.circle(self.win, self.color, (self.x*VER_WIDTH+VER_WIDTH//2, self.y*VER_HEIGHT+VER_HEIGHT//2), VER_HEIGHT//2 + 2)
        pygame.display.update((self.x*VER_WIDTH, self.y*VER_HEIGHT, VER_WIDTH, VER_HEIGHT))


    def set_obstacle(self, update):
        self.color = self.OBS_COLOR
        self.obs = True
        if update:
            self.display()

    def set_point(self, update):
        self.color = self.PNT_COLOR
        self.pnt = True
        if update:
            self.display()

    def set_visit(self, start, end):
        if start != self and end != self:
            self.color = self.EDG_COLOR
        self.vst = True
        for neighbour in self.neighbours:
            neighbour.inc()
            if neighbour.vst and neighbour != start and neighbour != end:
                neighbour.tst()
        if self != start and self != end:
            self.tst()

    def inc(self):
        self.vst_ngh += 1

    def tst(self):
        if self.vst_ngh == len(self.neighbours):
            self.color = self.VST_COLOR
            self.display()

    def recon(self):
            self.color = self.PNT_COLOR
            self.display()

        
    def reset(self, update):
        self.color = self.DEF_COLOR
        self.pnt = self.obs = self.vst = False
        if update:
            self.display()

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

class Mode(Enum):
    OBSTACLE = 1
    PATH = 2
    SIMULATION = 3
    PRE_SIM = 4
    RECONSTRUCT = 5
    IDLE = 6

class Grid:

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("A* Visualizer")

        self.grid = [None for _ in range(NUM_ROW)]
        for i in range(NUM_ROW):
            self.grid[i] = [None for _ in range(NUM_COL)]

        for i in range(NUM_ROW):
            for j in range(NUM_COL):
                self.grid[i][j] = Vertex(i , j)

        Vertex.win = self.win

        self.draw_all()

        self.running = True
        self.mode = Mode.OBSTACLE
        self.hold = False

        self.invasive = None

        self.s_ver, self.e_ver = None, None
        self.s_chosen = self.e_chosen = False

        self.front = PriorityQueue()

    def is_running(self):
        return self.running

    def get_ver_pos(self):
        pos = pygame.mouse.get_pos()
        return self.grid[pos[0]//VER_WIDTH][pos[1]//VER_HEIGHT]

    def on_done(self):
        self.mode = Mode.PATH
        self.invasive.destroy()

    def on_resume(self):
        self.invasive.destroy()
    
    def on_rerun(self):
        self.invasive.destroy()
        self.__init__()

    def on_exit(self):
        self.running = False
        self.invasive.destroy()

    def draw_all(self):
        self.win.fill(BLACK)
        for i in range(NUM_ROW):
            for j in range(NUM_COL):
                self.grid[i][j].display()

    def decide(self):
        if self.mode == Mode.OBSTACLE:
            self.obstacle_handle()
            
        elif self.mode == Mode.PATH:
            self.path_handle()

        elif self.mode == Mode.PRE_SIM:
            self.pre_sim_handle()

        elif self.mode == Mode.SIMULATION:
            self.simulation_handle()

        elif self.mode == Mode.RECONSTRUCT:
            self.reconstruct_handle()
        
        elif self.mode == Mode.IDLE:
            self.idle_handle()

    def obstacle_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif self.hold and self.mode == Mode.OBSTACLE:
                if event.type == pygame.MOUSEBUTTONUP:
                    self.get_ver_pos().set_obstacle(True) 
                    self.hold = False
                else:
                    self.get_ver_pos().set_obstacle(True) 
            elif not self.hold and event.type == pygame.MOUSEBUTTONDOWN:
                if self.mode == Mode.OBSTACLE:
                    self.get_ver_pos().set_obstacle(True)
                    self.hold = True
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.invasive = Tk()
                self.invasive.geometry('205x110+850+490')
                frame = Frame(self.invasive)

                Label(frame, 
                    text = '\nAre you done putting up obstacles\n           and want to proceed?\n').pack(side = 'top')
                Button(frame, width=12, text = 'Resume',
                    command=lambda : self.on_resume()).pack(side = 'left')
                Button(frame, width=12, text = 'Done!',
                    command=lambda : self.on_done()).pack(side = 'right')

                frame.pack()
                self.invasive.title('Obstacles')
                self.invasive.mainloop()

    def path_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.s_chosen and self.e_chosen:
                self.mode = Mode.PRE_SIM
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if self.s_chosen:
                    self.s_ver.reset(True)
                    self.s_chosen = False
                if self.e_chosen:
                    self.e_ver.reset(True)
                    self.e_chosen = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.s_chosen:
                    self.s_ver = self.get_ver_pos()
                    self.s_ver.set_point(True)
                    self.s_chosen = True
                elif not self.e_chosen:
                    self.e_ver = self.get_ver_pos()
                    if self.s_ver == self.e_ver:
                        continue
                    self.e_ver.set_point(True)
                    self.e_chosen = True

    def pre_sim_handle(self): 
        for row in self.grid:
            for vertex in row:
                vertex.appoint_neighbours(self.grid)
                vertex.appoint_heuristic(self.e_ver)
        self.front.put(self.s_ver, 0)
        self.s_ver.came_from = None
        self.s_ver.cost_so_far = 0
        self.mode = Mode.SIMULATION
        

    def simulation_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
        if self.front.empty():
            self.running = False
            return
        current = self.front.get()
        if current == self.e_ver:
            self.mode = Mode.RECONSTRUCT
            current.set_visit(self.s_ver, self.e_ver)
            current.display()
            self.backtrack = self.e_ver
            return
        for next in current.neighbours:
            new_cost = current.cost_so_far + 1
            if next.cost_so_far == -1 or new_cost < next.cost_so_far:
                next.cost_so_far = new_cost
                priority = new_cost + next.hst
                self.front.put(next, priority)
                next.came_from = current
        current.set_visit(self.s_ver, self.e_ver)
        current.display()

    def reconstruct_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
        if self.backtrack != self.s_ver:
            self.backtrack.recon()
            self.backtrack = self.backtrack.came_from
        else:
            self.s_ver.display()
            self.mode = Mode.IDLE
        

    def idle_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.invasive = Tk()
                self.invasive.geometry('205x110+850+490')
                frame = Frame(self.invasive)

                Label(frame, 
                    text = '\nRerun the simulation ?\n').pack(side = 'top')
                Button(frame, width=12, text = 'Rerun!',
                    command=lambda : self.on_rerun()).pack(side = 'left')
                Button(frame, width=12, text = 'Exit',
                    command=lambda : self.on_exit()).pack(side = 'right')

                frame.pack()
                self.invasive.title('Restart')
                self.invasive.mainloop()


    
def main():
    grid = Grid()
    clock = pygame.time.Clock()

    while grid.is_running():
        clock.tick(60)
        grid.decide()
    pygame.quit()

if __name__ == '__main__':
    main()