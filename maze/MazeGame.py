"""
Ver 2
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
from maze.Shape import Line, Cell, Color
from maze.solver.BFS import BFSSolver
from maze.solver.DFS import DFSSolver
from maze.utils import draw_line, draw_centered_square, remove_walls, get_direction, is_there_path, update_display, \
    draw_circle, \
    draw_line_between_cells, get_line

# Constants
NUM_PLAYERS = 1

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
        # Initialize Init
        pygame.init()

        # Tittle
        pygame.display.set_caption("Maze Creator")

        # icon Need work to display
        # pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'maze3.png')))

        # Create the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # Creating the lines for the grid
        self.create_walls()

        # Call show maze
        self.running = True

    def show_maze(self, path_shape, enable_find_route=False):

        # Drawing the grid
        self.draw_grid(Color.ORANGE_BROWN)

        dfs = DFSSolver(self.cells, pygame, self.screen, self.delay, fpsClock, FPS, enable_find_route)
        bfs = BFSSolver(self.cells, pygame, self.screen, self.delay, fpsClock, FPS, enable_find_route)

        counter = 0
        is_algo_set = None
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
                            draw_centered_square(pygame, self.screen, self.players[0], Color.BLACK, self.player_size,
                                                 self.cell_size)

                        self.players[0] = clicked_cell
                        draw_centered_square(pygame, self.screen, clicked_cell, Color.RED, self.player_size,
                                             self.cell_size)
                    else:
                        if clicked_cell is not None:
                            if self.players[1] is not None:
                                draw_centered_square(pygame, self.screen, self.players[1], Color.BLACK,
                                                     self.player_size,
                                                     self.cell_size)

                            # we create the target
                            self.players[1] = clicked_cell
                            draw_centered_square(pygame, self.screen, clicked_cell, Color.RED, self.player_size,
                                                 self.cell_size)
                    update_display(pygame, fpsClock, FPS)
                    print(clicked_cell)
                    counter += 1
                if event.type == pygame.KEYDOWN:

                    # Generate Maze
                    if event.key == pygame.K_g:
                        if self.check_players_position() and is_algo_set is not None:
                            if is_algo_set == "BFS":
                                self.cells = bfs.generate_maze(self.players[0])
                            elif is_algo_set == "DFS":
                                self.cells = dfs.generate_maze(self.players[0])
                            self.set_cells_not_visited()
                            # repaint grid
                            for cell_rows in self.cells:
                                for cell in cell_rows:
                                    self.draw_walls(cell.walls, Color.BLACK)
                                update_display(pygame, fpsClock, FPS)

                            self.start_maze_solver = True
                        else:
                            print(
                                f"is_algo_set = {is_algo_set}, are_players_in_position = {self.check_players_position()}")

                    # We use BFS for generating the maze
                    if event.key == pygame.K_b:
                        if self.check_players_position():
                            print(f"Generating MAZE using BFS")
                            is_algo_set = "BFS"

                    # We use DFS for generating the maze
                    if event.key == pygame.K_d:
                        if self.check_players_position():
                            print(f"Generating MAZE using DFS")
                            is_algo_set = "DFS"

                    # We repaint the grid
                    if event.key == pygame.K_p:
                        print("P-Pressed regenerate grid")
                        self.draw_grid(Color.ORANGE_BROWN)
                        self.players[0] = None
                        self.players[1] = None

                    # Solve the maze
                    if event.key == pygame.K_s:
                        # We start BFS once the MAZE has been constructed by DFS
                        self.solving = True
                        if self.start_maze_solver and is_algo_set is not None:
                            if is_algo_set == "BFS":
                                self.paths = bfs.solve(self.players, self.player_size, self.cell_size)
                            elif is_algo_set == "DFS":
                                self.paths = dfs.solve(self.players, self.player_size, self.cell_size)
                            self.draw_route(Color.BLUE, path_shape)
                            self.start_maze_solver = False
                            self.solving = False
                            self.set_cells_not_visited()

    def check_players_position(self):
        is_target_placed = self.players[1] is not None and type(self.players[1]) is Cell
        is_hero_placed = self.players[0] is not None and type(self.players[0]) is Cell
        return is_hero_placed and is_target_placed

    def set_cells_not_visited(self):
        for cell_row in self.cells:
            for cell in cell_row:
                cell.is_visited = False

    def draw_route(self, color, path_type):
        for cells_rows in self.cells:
            for cell in cells_rows:
                if cell != self.players[0] and cell != self.players[1]:
                    draw_centered_square(pygame, self.screen, cell, Color.BLACK, self.player_size, self.cell_size)

        final_route = self.paths[self.players[1].get_position()]
        if path_type != Maze.LINED_PATH:
            for row, col in final_route:
                c_cell = self.cells[row][col]
                if c_cell != self.players[0] and c_cell != self.players[1]:
                    if path_type == Maze.DOTTED_PATH:
                        draw_circle(pygame, self.screen, c_cell, (self.cell_size - self.player_size) / 2, color)
                    elif path_type == Maze.RECTANGLE_PATH:
                        draw_centered_square(pygame, self.screen, c_cell, color, self.player_size, self.cell_size)
                pygame.time.delay(self.delay)
                update_display(pygame, fpsClock, FPS)
        else:
            size_path = len(final_route)
            for i in range(size_path):
                if i < size_path - 1:
                    s_row, s_col = final_route[i]
                    e_row, e_col = final_route[i + 1]
                    draw_line_between_cells(pygame, self.screen, self.cells[s_row][s_col], self.cells[e_row][e_col],
                                            Color.RED)
                    update_display(pygame, fpsClock, FPS)
                    pygame.time.delay(self.delay)

    def draw_grid(self, color):
        self.screen.fill(Color.BLACK)
        for cell_row in self.cells:
            for cell in cell_row:
                for wall in cell.walls.values():
                    wall.set_blocking_wall()
                    draw_line(pygame, self.screen, wall, color)

        north_first_cell: Line = get_line(self.cells[0][0], Line.NORTH)
        west_last_cell: Line = get_line(self.cells[0][-1], Line.EAST)
        space_between_surfaces = 0.01
        statistics_rect_width = 0.20 - space_between_surfaces
        start_point_x = west_last_cell.start[0] + int(self.screen_width * space_between_surfaces)
        start_point_y = north_first_cell.start[1]

        pygame.draw.rect(self.screen, Color.WHITE,
                         pygame.Rect(start_point_x, start_point_y, self.screen_width * statistics_rect_width,
                                     self.screen_height - 3 * self.margin), 3)

        update_display(pygame, fpsClock, FPS)
        # Setting max grid Dimension
        self.R = len(self.cells)
        self.C = len(self.cells[0])

    def create_walls(self):
        # 85% of the width and height is for the maze screen
        maze_screen_width = self.screen_width * .80

        num_horizontal_cells = int((maze_screen_width - 2 * self.margin) / self.cell_size)
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
    margin = 10
    m = Maze(1800, 1000, 18, margin, 5)
    m.create_maze()
    print(
        f"(rows, cols) in the grid ({len(m.cells)}, {len(m.cells[0])}), total cells = {len(m.cells) * len(m.cells[0])}")
    m.show_maze(Maze.LINED_PATH, True)
