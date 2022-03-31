from const import *
import pygame
from math import sqrt

class Vertex:
    DEF_COLOR = PAS_GREEN
    OBS_COLOR = D_GREEN
    PNT_COLOR = RED
    VST_COLOR = LBLUE
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
        if self.obs:
            return
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