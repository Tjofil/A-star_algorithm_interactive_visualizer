from tkinter import *
from tkinter.ttk import *
from const import *
from vertex import *
from pqueue import *

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
                    text = '\nRerun the simulation from scratch?\n\n').pack(side = 'top')
                Button(frame, width=12, text = 'Rerun!',
                    command=lambda : self.on_rerun()).pack(side = 'left')
                Button(frame, width=12, text = 'Exit',
                    command=lambda : self.on_exit()).pack(side = 'right')

                frame.pack()
                self.invasive.title('Restart')
                self.invasive.mainloop()