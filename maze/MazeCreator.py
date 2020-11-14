"""
Maze Generator DFS
Maze Solver BFS
Luis Enrique Gonzalez
Sunnyvale CA
Noviembre 6, 2020
"""
import os
import random
import time
import math
from collections import deque
from queue import Queue

import pygame
from maze.Shape import Line, Cell
from maze.utils import draw_line, draw_square, remove_walls, get_direction, is_there_path, update_display

# Constants
NUM_PLAYERS = 1
CELL_SIZE = 20
PLAYER_SIZE = math.ceil(CELL_SIZE * .53)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)
NOOB = (255, 0, 0)
LEMON_CHIFFON = (255, 250, 205)
YELLOW = (255, 255, 0)
GREEN_YELLOW = (173, 255, 47)

FPS = 90
# frames per second setting
fpsClock = pygame.time.Clock()

# DELAY
DELAY = 0


class Maze:

    def __init__(self, screen_width, screen_height, cell_size=10, margin=10):
        self.start_bfs = False
        self.running = False
        if screen_width < 100 or screen_height < 100:
            raise ValueError(
                f"Either Screen width = {screen_width} or Screen Height = {screen_height} must be at least 100")
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.screen = None
        self.cell_size = cell_size
        self.margin = margin
        self.lines = []
        self.cells = []
        self.R = 0
        self.C = 0
        self.players_drawn = False
        self.players = []
        self.hero = None
        self.paths = dict()

    def create_maze(self):
        """
        Create Maze will create the grid, to create the grid we are going to create the lines
        then we will draw those lines, we are also taking into account a margin
        :return:
        """
        num_horizontal_cells = int((self.screen_width - 2 * self.margin) / self.cell_size)
        num_vertical_cells = int((self.screen_height - 2 * self.margin) / self.cell_size)

        # Creating the lines for the grid
        start_x = self.margin
        start_y = self.margin
        for row in range(num_vertical_cells):
            cell_cols = []
            for col in range(num_horizontal_cells):
                # Calculate deltas
                delta_x = start_x + self.cell_size
                delta_y = start_y + self.cell_size

                # Generate WALLS
                north = Line(start_x, start_y, delta_x, start_y)
                south = Line(start_x, delta_y, delta_x, delta_y)
                east = Line(delta_x, start_y, delta_x, delta_y)
                west = Line(start_x, start_y, start_x, delta_y)

                cell_cols.append(Cell(row, col, north, south, east, west))

                # increment x by cell size
                start_x = start_x + self.cell_size
            # increment y by cell size
            start_y = start_y + self.cell_size
            start_x = self.margin
            self.cells.append(cell_cols)

        # Call show maze
        self.running = True

    def show_maze(self):
        # stack to start DFS
        cell_stack_row = deque()
        cell_stack_col = deque()

        # Initialize Init
        pygame.init()

        # Tittle
        pygame.display.set_caption("Maze Creator")

        # icon
        pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'maze3.png')))

        # Create the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(BLACK)

        # Drawing the grid
        for cell_row in self.cells:
            for cell in cell_row:
                for wall in cell.walls.values():
                    if not wall.is_duplicate and wall.is_blocking_wall:
                        draw_line(pygame, self.screen, wall, WHITE)

        # Setting max grid Dimension
        self.R = len(self.cells)
        self.C = len(self.cells[0])

        # Randomly we select the initial cell
        rnd_row = random.randint(0, self.R - 1)
        rnd_col = random.randint(0, self.C - 1)

        initial_cell = self.cells[rnd_row][rnd_col]
        initial_cell.set_visited()
        cell_stack_row.append(initial_cell.row)
        cell_stack_col.append(initial_cell.col)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Both stacks are in sync
            while len(cell_stack_row) > 0:
                current_cell_row = cell_stack_row.pop()
                current_cell_col = cell_stack_col.pop()
                rnd_cell = self.get_random_neighbour(self.cells[current_cell_row][current_cell_col])
                if rnd_cell is not None:
                    # Push current cell to Stack
                    cell_stack_row.append(current_cell_row)
                    cell_stack_col.append(current_cell_col)
                    # Get current from grid
                    current_cell = self.cells[current_cell_row][current_cell_col]

                    # Remove walls between current cell and rnd_cell
                    remove_walls(current_cell, rnd_cell, current_cell_row, current_cell_col)

                    # Mark rnd cell as visited
                    current_cell.set_visited()

                    # Push rnd cell to the stacks
                    rnd_cell.set_visited()
                    cell_stack_row.append(rnd_cell.row)
                    cell_stack_col.append(rnd_cell.col)

                    # repaint lines with black line
                    for wall in current_cell.walls.values():
                        if not wall.is_blocking_wall:
                            draw_line(pygame, self.screen, wall, BLACK)
                    for wall in rnd_cell.walls.values():
                        if not wall.is_blocking_wall:
                            draw_line(pygame, self.screen, wall, BLACK)
                    update_display(pygame, fpsClock, FPS)

            # Maze Generation has finished, create origin (blue) destination (Green)
            if not self.players_drawn:
                self.hero = self.get_random_cell()
                draw_square(pygame, self.screen, self.hero, BLUE, PLAYER_SIZE, CELL_SIZE)
                for i in range(NUM_PLAYERS):
                    player = self.get_random_cell()
                    self.players.append(player)
                    draw_square(pygame, self.screen, player, random.choice([RED, PINK]), PLAYER_SIZE,
                                CELL_SIZE)
                update_display(pygame, fpsClock, FPS)
                self.players_drawn = True
                self.start_bfs = True
                self.set_cells_not_visited()

            # We start BFS once the MAZE has been constructed by DFS
            if self.start_bfs:
                row_queue = deque()
                col_queue = deque()

                # Variables used toi keep track number of steps taken to
                move_count = 0
                nodes_left_in_layer = 1
                nodes_in_next_layer = 0
                reached_end = False

                row_queue.append(self.hero.row)
                col_queue.append(self.hero.col)
                self.hero.set_visited()
                initial_position = [self.hero.get_position()]
                self.paths[(self.hero.get_position())] = initial_position
                while len(row_queue) > 0:
                    # deque is LIFO but using pop left we get queue behaviour FIFO
                    row = row_queue.popleft()
                    col = col_queue.popleft()

                    # only the first player for now TODO extend solution for all the players
                    current_cell = self.cells[row][col]
                    # print(f"current Cell= {current_cell} ---> {self.players[0]}")
                    if current_cell == self.players[0]:
                        draw_square(pygame, self.screen, self.players[0], RED, PLAYER_SIZE, CELL_SIZE)
                        update_display(pygame, fpsClock, FPS)
                        reached_end = True
                        break

                    # this is not that wrong
                    neighbours = self.explore_neighbours_bfs(row, col)
                    for cell_n in neighbours:
                        row_queue.append(cell_n.row)
                        col_queue.append(cell_n.col)
                        cell_n.set_visited()
                        nodes_in_next_layer += 1
                        # we mark the paths
                        draw_square(pygame, self.screen, cell_n, GREEN_YELLOW, PLAYER_SIZE, CELL_SIZE)
                        pygame.time.delay(DELAY)
                        update_display(pygame, fpsClock, FPS)
                        nodes_left_in_layer -= 1
                        if nodes_left_in_layer == 0:
                            nodes_left_in_layer = nodes_in_next_layer
                            nodes_in_next_layer = 0
                            move_count += 1

                        # Get current cell path
                        current_path = self.paths[current_cell.get_position()]
                        # Step 1 create new Key
                        self.paths[cell_n.get_position()] = []
                        # Step 2 get current path and add all the positions
                        for position in current_path:
                            self.paths[cell_n.get_position()].append(position)
                        # Step 3 append current position to path
                        self.paths[cell_n.get_position()].append(cell_n.get_position())
                    # delete current cell path key
                    del self.paths[current_cell.get_position()]

                if reached_end:
                    print(f"We found it move count = {move_count}")
                    # lets paint the final route

                    final_route = self.paths[self.players[0].get_position()]
                    for row, col in final_route:
                        if self.cells[row][col] != self.hero and self.cells[row][col] != self.players[0]:
                            draw_square(pygame, self.screen, self.cells[row][col], DARK_BLUE, PLAYER_SIZE, CELL_SIZE)
                            update_display(pygame, fpsClock, FPS)
                    self.start_bfs = False

    def explore_neighbours_bfs(self, row, col):
        # BFS https://youtu.be/09_LlHjoEiY?t=3239
        neighbours = []
        for i in range(4):
            rr, cc = get_direction(row, col, i)

            # we skip bounds
            if rr < 0 or cc < 0:
                continue
            if rr >= self.R or cc >= self.C:
                continue

            if self.cells[rr][cc].is_visited:
                continue

            # we have to determine if there is a pathway between current cell and next cell we use relative position
            if is_there_path(self.cells[row][col], self.cells[rr][cc]):
                neighbours.append(self.cells[rr][cc])

        return neighbours

    def get_random_neighbour(self, current_cell):
        neighbours = self.get_neighbours(current_cell.row, current_cell.col)
        if len(neighbours) > 0:
            return random.choice(neighbours)
        else:
            return None

    def get_neighbours(self, row, col):
        neighbours = []
        for i in range(4):
            rr, cc = get_direction(row, col, i)
            # we skip bounds
            if rr < 0 or cc < 0:
                continue
            if rr >= self.R or cc >= self.C:
                continue

            # we skip visited cells
            if self.cells[rr][cc].is_visited:
                continue
            neighbours.append(self.cells[rr][cc])
        return neighbours

    def get_random_cell(self):
        rnd_row = random.randint(0, len(self.cells) - 1)
        rnd_col = random.randint(0, len(self.cells[0]) - 1)
        return self.cells[rnd_row][rnd_col]

    def set_cells_not_visited(self):
        for cell_row in self.cells:
            for cell in cell_row:
                cell.is_visited = False


if __name__ == "__main__":
    print(f'Welcome home Maze creator {time.time()}')
    n = Queue()
    n.put('a')
    n.put('b')
    n.put('c')
    print(n.get())
    print(n.get())
    print(n.get())
    dd = deque()
    dd.append('aa')
    dd.append('bb')
    dd.append('cc')
    print(dd.popleft())
    print(dd.popleft())
    print(dd.popleft())

    cc = dict()
    cc[(0, 0)] = (0, 1)
    cc[(0, 0)] = (0, 2)
    print(cc[(0, 0)])

    lst = list()
    inner = list()
    inner.append((1, 2))
    inner.append((1, 3))

    m = Maze(1500, 1000, CELL_SIZE)
    m.create_maze()
    print(
        f"(rows, cols) in the grid ({len(m.cells)}, {len(m.cells[0])}), total cells = {len(m.cells) * len(m.cells[0])}")
    m.show_maze()
