import time
import pygame
import random
from pygame import mixer
from maze.Shape import Line, Cell
from collections import deque

# Constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)

# Direction Vectors
DIRECTION_ROW = [-1, 1, 0, 0]
DIRECTION_COL = [0, 0, 1, -1]

FPS = 30
# frames per second setting
fpsClock = pygame.time.Clock()


class Maze:

    def __init__(self, screen_width, screen_height, cell_size=10, margin=10):
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

        # Create the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(BLACK)

        # Drawing the grid
        for cell_row in self.cells:
            for cell in cell_row:
                for wall in cell.walls.values():
                    if not wall.is_duplicate and wall.is_drawable:
                        pygame.draw.line(self.screen, WHITE, wall.start, wall.end)

        # Setting max grid Dimension
        self.R = len(self.cells)
        self.C = len(self.cells[0])

        # Randomly we select the initial cell
        rnd_row = random.randint(0, self.R)
        rnd_col = random.randint(0, self.C)

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
                    # Get current from grid
                    current_cell = self.cells[current_cell_row][current_cell_col]

                    # Remove walls between current cell and rnd_cell
                    self.remove_walls(current_cell, rnd_cell, current_cell_row, current_cell_col)

                    # Mark rnd cell as visited
                    current_cell.set_visited()

                    # Push rnd cell to the stacks
                    cell_stack_row.append(rnd_cell.row)
                    cell_stack_col.append(rnd_cell.col)

                    # repaint lines with black line
                    for wall in current_cell.walls.values():
                        if not wall.is_drawable:
                            pygame.draw.line(self.screen, BLACK, wall.start, wall.end)
                    for wall in rnd_cell.walls.values():
                        if not wall.is_drawable:
                            pygame.draw.line(self.screen, BLACK, wall.start, wall.end)
                    pygame.display.update()
                    fpsClock.tick(FPS)

    def explore_neighbours_bfs(self, current_cell):
        neighbours = self.get_neighbours(current_cell.row, current_cell.col)
        # TODO complete BFS https://youtu.be/09_LlHjoEiY?t=3239

    def get_random_neighbour(self, current_cell):
        neighbours = self.get_neighbours(current_cell.row, current_cell.col)
        if len(neighbours) > 0:
            return random.choice(neighbours)
        else:
            return None

    def get_neighbours(self, row, col):
        neighbours = []
        for i in range(4):
            rr = row + DIRECTION_ROW[i]
            cc = col + DIRECTION_COL[i]

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

    def remove_walls(self, current_cell, rnd_cell, current_row, current_col):
        if current_row == rnd_cell.row:
            relative_col_pos = current_col - rnd_cell.col
            if relative_col_pos == 1:
                # we remove current cell west wall and rnd east wall
                current_cell.walls[Line.WEST].set_not_drawable()
                rnd_cell.walls[Line.EAST].set_not_drawable()
            elif relative_col_pos == -1:
                # we remove current cell's east wall and rnd cell's west wall
                current_cell.walls[Line.EAST].set_not_drawable()
                rnd_cell.walls[Line.WEST].set_not_drawable()
        elif current_col == rnd_cell.col:
            relative_row_pos = current_row - rnd_cell.row
            if relative_row_pos == 1:
                # Remove current's North and Rnd's South
                current_cell.walls[Line.NORTH].set_not_drawable()
                rnd_cell.walls[Line.SOUTH].set_not_drawable()
            elif relative_row_pos == -1:
                current_cell.walls[Line.SOUTH].set_not_drawable()
                rnd_cell.walls[Line.NORTH].set_not_drawable()

if __name__ == "__main__":
    print(f'Welcome home Maze creator {time.time()}')
    l1 = Line(1, 2, 3, 5)
    l2 = Line(1, 2, 3, 5)
    print(f"l1 key = {l1.generate_key()}")
    print(f"l2 key = {l2.generate_key()}")
    print(l1.generate_key() == l2.generate_key())
    print(l1)
    l = 30
    for r in range(1, l + 1):
        print(r)
    sd = (1, 2)
    sd1 = (1, 2)
    print(sd == sd1)
    m = Maze(900, 800, 80)
    m.create_maze()
    print(
        f"(rows, cols) in the grid ({len(m.cells)}, {len(m.cells[0])}), total cells = {len(m.cells) * len(m.cells[0])}")
    m.show_maze()
