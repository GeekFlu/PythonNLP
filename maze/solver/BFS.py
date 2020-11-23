import random
from collections import deque
from maze.Shape import Cell, Color
from maze.solver.MazeSolverIfc import MazeSolverInterface
from maze.utils import remove_walls, get_direction, is_there_path, draw_square, update_display


class BFSSolver(MazeSolverInterface):

    def __init__(self, the_grid, pygame, screen, delay, fps_clock, fps, enable_visual_solve):
        super(BFSSolver, self).__init__(the_grid, pygame, screen, delay, fps_clock, fps, enable_visual_solve)

    def solve(self, players: [], player_size, cell_size) -> dict:
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
            row = row_queue.popleft()
            col = col_queue.popleft()

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
                if self.enable_visual_solve:
                    draw_square(self.pygame, self.screen, cell_n, Color.GREEN_YELLOW, player_size, cell_size)
                    self.pygame.time.delay(self.delay)
                    update_display(self.pygame, self.fps_clock, self.fps)

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
            current_cell_row = cell_stack_row.popleft()
            current_cell_col = cell_stack_col.popleft()
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
