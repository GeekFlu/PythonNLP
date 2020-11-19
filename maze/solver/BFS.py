import random
from collections import deque
from maze.Shape import Cell, Color
from maze.solver.MazeSolverIfc import MazeSolverInterface
from maze.utils import remove_walls, get_direction, is_there_path, draw_square, update_display


class BFSSolver(MazeSolverInterface):

    def solve(self, players: [], player_size, cell_size) -> dict:
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
