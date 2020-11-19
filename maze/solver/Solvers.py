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

    def __init__(self, the_grid):
        self.cells = the_grid
        self.R = len(self.cells)
        self.C = len(self.cells[0])

    def solve(self, pygame, screen, delay, fps_clock, fps, players: [], player_size, cell_size) -> dict:
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


class BFSSolver(MazeSolverInterface):

    def solve(self, pygame, screen, delay, fps_clock, fps, players: [], player_size, cell_size) -> dict:
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
            row = row_queue.popleft()
            col = col_queue.popleft()

            current_cell: Cell = self.cells[row][col]
            if current_cell == self.players[1]:
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
            return

    def generate_maze(self, hero: Cell):
        pass


class DFSSolver(MazeSolverInterface):

    def __init__(self, the_grid):
        super(DFSSolver, self).__init__(the_grid)

    def solve(self, pygame, screen, delay, fps_clock, fps, players: [], player_size, cell_size) -> dict:
        paths = dict()
        row_queue = deque()
        col_queue = deque()

        # Variables used toi keep track number of steps taken to
        move_count = 0
        nodes_left_in_layer = 1
        nodes_in_next_layer = 0
        reached_end = False

        row_queue.append(players[0].row)
        col_queue.append(players[0].col)
        players[0].set_visited()
        initial_position = [players[0].get_position()]
        paths[(players[0].get_position())] = initial_position
        while len(row_queue) > 0:
            # deque is LIFO but using pop left we get queue behaviour FIFO
            row = row_queue.pop()
            col = col_queue.pop()

            current_cell: Cell = self.cells[row][col]
            if current_cell == players[1]:
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
                draw_square(pygame, screen, cell_n,  Color.GREEN_YELLOW, player_size, cell_size)
                pygame.time.delay(delay)
                update_display(pygame, fps_clock, fps)
                nodes_left_in_layer -= 1
                if nodes_left_in_layer == 0:
                    nodes_left_in_layer = nodes_in_next_layer
                    nodes_in_next_layer = 0
                    move_count += 1

                # Get current cell path
                current_path = paths[current_cell.get_position()]
                # Step 1 create new Key
                paths[cell_n.get_position()] = []
                # Step 2 get current path and add all the positions
                for position in current_path:
                    paths[cell_n.get_position()].append(position)
                # Step 3 append current position to path
                paths[cell_n.get_position()].append(cell_n.get_position())
            # delete current cell path key
            del paths[current_cell.get_position()]

        if reached_end:
            print(f"We found it move count = {move_count}")

        return paths

    def generate_maze(self, hero: Cell):
        # stack to start DFS
        cell_stack_row = deque()
        cell_stack_col = deque()
        initial_cell = hero
        initial_cell.set_visited()
        cell_stack_row.append(initial_cell.row)
        cell_stack_col.append(initial_cell.col)
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

        return self.cells

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
