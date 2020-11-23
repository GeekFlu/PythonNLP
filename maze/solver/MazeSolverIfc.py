"""
Maze Generator DFS
Maze Solver BFS
Luis Enrique Gonzalez
Sunnyvale CA
November 6, 2020
"""
import random
from collections import deque

from maze.Shape import Cell, Color
from maze.utils import remove_walls, get_direction, is_there_path, draw_square, update_display


class MazeSolverInterface:

    def __init__(self, the_grid, pygame, screen, delay, fps_clock, fps, enable_visual_solve):
        self.cells = the_grid
        self.R = len(self.cells)
        self.C = len(self.cells[0])
        self.pygame = pygame
        self.screen = screen
        self.delay = delay
        self.fps_clock = fps_clock
        self.fps = fps
        self.enable_visual_solve = enable_visual_solve

    def solve(self, players: [], player_size, cell_size) -> dict:
        """
        Will implement BFS or DFS to solve the maze
        :return:
        """
        pass

    def generate_maze(self, hero: Cell):
        pass

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

    def get_random_neighbour(self, current_cell):
        neighbours = self.get_neighbours(current_cell.row, current_cell.col)
        if len(neighbours) > 0:
            return random.choice(neighbours)
        else:
            return None
