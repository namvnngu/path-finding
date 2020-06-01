try:
    import pygame
    import sys
    import math
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os
except:
    import install_requirements  # install packages
    import pygame
    import sys
    import math
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os


# Initialize all the available pygame modules
pygame.init()
pygame.display.set_caption('Path Finding By Breadth First Search')

class Node:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.neighbors = []
        self.previous = None
        self.obs = False

    def show(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
        pygame.display.update()

    def addNeighbors(self, grid):
        i = self.i
        j = self.j
        if i+1 < cols and grid[self.i + 1][j].obs == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i-1 >= 0 and grid[self.i - 1][j].obs == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j+1 < rows and grid[self.i][j + 1].obs == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j-1 >= 0 and grid[self.i][j - 1].obs == False:
            self.neighbors.append(grid[self.i][j - 1])
        #  if j-1 >= 0 and i-1 >= 0 and grid[i-1][j - 1].obs == False:
            #  self.neighbors.append(grid[i - 1][j - 1])
        #  if j+1 < rows and i+1 < cols and grid[i + 1][j + 1].obs == False:
            #  self.neighbors.append(grid[i + 1][j + 1])
        #  if j-1 >= 0 and i+1 < cols and grid[i+1][j - 1].obs == False:
            #  self.neighbors.append(grid[i + 1][j - 1])
        #  if j+1 < rows and i-1 >=0 and grid[i - 1][j + 1].obs == False:
            #  self.neighbors.append(grid[i - 1][j + 1])


# Set up global variable
# Colors
yellow = (255, 208, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
green = (107, 245, 27)
red = (255, 0, 0)
purple = (208, 0, 250)

# The sizes of main window and square nodes
WIDTH_WIN = 500
HEIGHT_WIN = 500
screen = pygame.display.set_mode((WIDTH_WIN, HEIGHT_WIN))
screen.fill(white)
cols = 25
rows = 25
grid = [0 for i in range(cols)]
w = WIDTH_WIN / cols
h = HEIGHT_WIN / rows

# Create a grid
for i in range(cols):
    grid[i] = [0 for i in range(rows)]

# Create square nodes
for i in range(cols):
    for j in range(rows):
        grid[i][j] = Node(i, j)
        grid[i][j].show(black, 1)

# Choose point A and point B on the grid
def draw_point(name_point, color):
    stop = False
    while not stop:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.mouse.get_pressed()[0]:
                try:
                    coor = pygame.mouse.get_pos()
                    x = coor[0] // (WIDTH_WIN // cols)
                    y = coor[1] // (HEIGHT_WIN // rows)
                    grid[x][y].show(color, 0)
                    return grid[x][y]
                except AttributeError:
                    pass

pointA = draw_point('A', yellow)
pointB = draw_point('B', blue)
print(pointA, pointB)

# Draw Barrier
def colorize_barrier(coor):
    x = coor[0] // (WIDTH_WIN // cols)
    y = coor[1] // (HEIGHT_WIN // rows)
    barrier = grid[x][y] 
    if barrier != pointA and barrier != pointB:
        if barrier.obs == False:
            barrier.obs = True
            barrier.show(black, 0)

def draw_barrier():
    stop = False
    while not stop:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.mouse.get_pressed()[0]:
                try:
                    coor = pygame.mouse.get_pos()
                    colorize_barrier(coor)
                except AttributeError:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stop = True
                    break
draw_barrier()

# Add Neighbors
for i in range(cols):
    for j in range(rows):
        grid[i][j].addNeighbors(grid)

def heuristic_dis(s, e):
    return (s.i - e.i)**2 + (s.j - e.j)**2

# Breadth-First Search
def backtrace(start, target):
    while target.previous != start:
        target.previous.show(green, 0)
        target = target.previous

def bfs():
    # The starting and ending points are the same
    if(pointA == pointB):
        os.execl(sys.executable,sys.executable, *sys.argv)
        
    # "Visited" DP
    visited = [0 for i in range(rows)]
    for i in range(cols):
        visited[i] = [False for i in range(cols)]

    # Initialize queue and current point 
    visited[pointA.i][pointA.j] = True
    current = pointA
    queue = [current]

    # Start BFS
    while(queue):
        current = queue.pop(0)

        # Run over all current point's neighbors
        neighbors = current.neighbors
        for neighbor in neighbors:
            x = neighbor.i
            y = neighbor.j

            neighbor.show(purple, 5)
            if(not visited[x][y]):
                visited[x][y] = True
                neighbor.show(red, 5)

                # Push neighbor to queue
                queue.append(neighbor)

                # Set neighbor's parent
                if neighbor.previous == None:
                    neighbor.previous = current

            # Approaching the destination
            if(neighbor == pointB):
                backtrace(pointA, pointB)
                print('Found')
                while True:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                            elif event.key == pygame.K_SPACE:
                                os.execl(sys.executable,sys.executable, *sys.argv)
# Main
while True:
    ev = pygame.event.poll()
    if(ev.type == pygame.QUIT):
        pygame.quit()
    pygame.display.update()
    bfs()
