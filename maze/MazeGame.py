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

import pygame
from maze.Shape import Line, Cell
from maze.solver.Solvers import DFSSolver
from maze.utils import draw_line, draw_square, remove_walls, get_direction, is_there_path, update_display, draw_circle, \
    draw_line_between_cells

# Constants
NUM_PLAYERS = 1
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
ORANGE_BROWN = (102, 47, 0)

FPS = 90
# frames per second setting
fpsClock = pygame.time.Clock()


class Maze:
    DOTTED_PATH = "dotted"
    RECTANGLE_PATH = "rectangle"
    LINED_PATH = "lined"

    def __init__(self, screen_width, screen_height, cell_size=10, margin=10, delay=0):
        self.start_maze_solver = False
        self.running = False
        if screen_width < 100 or screen_height < 100:
            raise ValueError(
                f"Either Screen width = {screen_width} or Screen Height = {screen_height} must be at least 100")
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.screen = None
        self.cell_size = cell_size
        self.player_size = math.ceil(cell_size * .60)
        self.margin = margin
        self.lines = []
        self.cells = []
        self.R = 0
        self.C = 0
        self.players = [None, None]
        self.paths = dict()
        self.delay = delay
        self.solving = False

    def create_maze(self):
        """
        Create Maze will create the grid, to create the grid we are going to create the lines
        then we will draw those lines, we are also taking into account a margin
        :return:
        """
        # Creating the lines for the grid
        self.create_walls()
        # Call show maze
        self.running = True

    def show_maze(self, path_shape, is_bfs=True):
        dfs = DFSSolver(self.cells)

        # Initialize Init
        pygame.init()

        # Tittle
        pygame.display.set_caption("Maze Creator")

        # icon Need work to display
        # pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'maze3.png')))

        # Create the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Drawing the grid
        self.draw_grid(ORANGE_BROWN)

        counter = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = event.pos
                    clicked_cell = self.get_cell(pos_x, pos_y)
                    if clicked_cell is not None and counter % 2 == 0:
                        # we create a hero pos 0
                        if self.players[0] is not None:
                            draw_square(pygame, self.screen, self.players[0], BLACK, self.player_size, self.cell_size)

                        self.players[0] = clicked_cell
                        draw_square(pygame, self.screen, clicked_cell, BLUE, self.player_size, self.cell_size)
                    else:
                        if clicked_cell is not None:
                            if self.players[1] is not None:
                                draw_square(pygame, self.screen, self.players[1], BLACK, self.player_size,
                                            self.cell_size)

                            # we create the target
                            self.players[1] = clicked_cell
                            draw_square(pygame, self.screen, clicked_cell, random.choice([RED, PINK]), self.player_size,
                                        self.cell_size)
                    update_display(pygame, fpsClock, FPS)
                    print(clicked_cell)
                    counter += 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print("Pressed left")
                    if event.key == pygame.K_RIGHT:
                        print("Pressed right")
                    if event.key == pygame.K_UP:
                        print("Pressed up")
                    if event.key == pygame.K_DOWN:
                        print("Pressed down")

                    # We repaint the grid
                    if event.key == pygame.K_p:
                        if not self.start_maze_solver:
                            print("P-Pressed regenerate grid")
                            self.draw_grid(ORANGE_BROWN)
                            self.players[0] = None
                            self.players[1] = None

                    if event.key == pygame.K_SPACE:
                        print("Space BAR pressed")
                        is_target_placed = self.players[1] is not None and type(self.players[1]) is Cell
                        is_hero_placed = self.players[0] is not None and type(self.players[0]) is Cell
                        if is_hero_placed and is_target_placed and not self.solving:
                            self.solving = True
                            self.cells = dfs.generate_maze(self.players[0])
                            # repaint grid
                            for cell_rows in self.cells:
                                for cell in cell_rows:
                                    self.draw_walls(cell.walls, BLACK)
                                update_display(pygame, fpsClock, FPS)

                            self.start_maze_solver = True
                            self.set_cells_not_visited()

                            # We start BFS once the MAZE has been constructed by DFS
                            if self.start_maze_solver:
                                self.execute_solver(is_bfs, path_shape)

    def explore_neighbours(self, row, col):
        """
        We explore the neighbours from a cell
        :param row: row
        :param col: col
        :return: Neighbours
        """
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

    def set_cells_not_visited(self):
        for cell_row in self.cells:
            for cell in cell_row:
                cell.is_visited = False

    def draw_route(self, color, path_type):
        for cells_rows in self.cells:
            for cell in cells_rows:
                if cell != self.players[0] and cell != self.players[1]:
                    draw_square(pygame, self.screen, cell, BLACK, self.player_size, self.cell_size)

        final_route = self.paths[self.players[1].get_position()]
        if path_type != Maze.LINED_PATH:
            for row, col in final_route:
                c_cell = self.cells[row][col]
                if c_cell != self.players[0] and c_cell != self.players[1]:
                    if path_type == Maze.DOTTED_PATH:
                        draw_circle(pygame, self.screen, c_cell, (self.cell_size - self.player_size) / 2, color)
                    elif path_type == Maze.RECTANGLE_PATH:
                        draw_square(pygame, self.screen, c_cell, color, self.player_size, self.cell_size)
                pygame.time.delay(50)
                update_display(pygame, fpsClock, FPS)
        else:
            size_path = len(final_route)
            for i in range(size_path):
                if i < size_path - 1:
                    s_row, s_col = final_route[i]
                    e_row, e_col = final_route[i + 1]
                    draw_line_between_cells(pygame, self.screen, self.cells[s_row][s_col], self.cells[e_row][e_col],
                                            GREEN_YELLOW)
                    update_display(pygame, fpsClock, FPS)
                    pygame.time.delay(50)

    def draw_grid(self, color):
        self.screen.fill(BLACK)
        for cell_row in self.cells:
            for cell in cell_row:
                for wall in cell.walls.values():
                    wall.set_blocking_wall()
                    draw_line(pygame, self.screen, wall, color)
        update_display(pygame, fpsClock, FPS)
        # Setting max grid Dimension
        self.R = len(self.cells)
        self.C = len(self.cells[0])

    def create_walls(self):
        num_horizontal_cells = int((self.screen_width - 2 * self.margin) / self.cell_size)
        num_vertical_cells = int((self.screen_height - 2 * self.margin) / self.cell_size)
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

    def draw_walls(self, walls, color):
        """
        Receives walls dictionary
        :param walls:
        :param color:
        :return:
        """
        for wall in walls.values():
            if not wall.is_blocking_wall:
                draw_line(pygame, self.screen, wall, color)

    def execute_solver(self, is_bfs, path_shape):
        row_queue = deque()
        col_queue = deque()

        # Variables used toi keep track number of steps taken to
        move_count = 0
        nodes_left_in_layer = 1
        nodes_in_next_layer = 0
        reached_end = False

        row_queue.append(self.players[0].row)
        col_queue.append(self.players[0].col)
        self.players[0].set_visited()
        initial_position = [self.players[0].get_position()]
        self.paths[(self.players[0].get_position())] = initial_position
        while len(row_queue) > 0:
            # deque is LIFO but using pop left we get queue behaviour FIFO
            if is_bfs:
                row = row_queue.popleft()
                col = col_queue.popleft()
            else:
                row = row_queue.pop()
                col = col_queue.pop()

            current_cell: Cell = self.cells[row][col]
            if current_cell == self.players[1]:
                draw_square(pygame, self.screen, self.players[1], WHITE, self.player_size, self.cell_size)
                update_display(pygame, fpsClock, FPS)
                reached_end = True
                break

            # this is not that wrong
            neighbours = self.explore_neighbours(row, col)
            for cell_n in neighbours:
                row_queue.append(cell_n.row)
                col_queue.append(cell_n.col)
                cell_n.set_visited()
                nodes_in_next_layer += 1
                # we mark the paths
                draw_square(pygame, self.screen, cell_n, GREEN_YELLOW, self.player_size, self.cell_size)
                pygame.time.delay(self.delay)
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
            self.draw_route(GREEN_YELLOW, path_shape)
            self.start_maze_solver = False
            self.solving = False
            self.set_cells_not_visited()

    def get_cell(self, pos_x, pos_y):
        delta_col = math.ceil((pos_x - self.margin) / self.cell_size) - 1  # zero based
        delta_row = math.ceil((pos_y - self.margin) / self.cell_size) - 1  # zero based
        last_cell = self.cells[-1][-1]
        limit_x, limit_y = last_cell.walls[Line.SOUTH].end
        if pos_x < limit_x and pos_y < limit_y:
            cell = self.cells[delta_row][delta_col]
            top_x, top_y = cell.walls[Line.NORTH].start
            down_x, down_y = cell.walls[Line.SOUTH].end
            if top_x < pos_x < down_x and top_y < pos_y < down_y:
                return cell
            else:
                return None


if __name__ == "__main__":
    print(f'Welcome home Maze creator {time.time()}')
    margin = 20
    m = Maze(900, 800, 20, margin, 0)
    m.create_maze()
    print(
        f"(rows, cols) in the grid ({len(m.cells)}, {len(m.cells[0])}), total cells = {len(m.cells) * len(m.cells[0])}")
    m.show_maze(Maze.LINED_PATH, False)