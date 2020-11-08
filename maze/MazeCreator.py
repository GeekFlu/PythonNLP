import time
import pygame
from pygame import mixer
from maze.Shape import Line, Cell

# Constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)


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

                if north.generate_key() not in self.lines:
                    self.lines.append(north.generate_key())
                else:
                    north.set_is_duplicate()

                if south.generate_key() not in self.lines:
                    self.lines.append(south.generate_key())
                else:
                    south.set_is_duplicate()

                if east.generate_key() not in self.lines:
                    self.lines.append(east.generate_key())
                else:
                    east.set_is_duplicate()

                if west.generate_key() not in self.lines:
                    self.lines.append(west.generate_key())
                else:
                    west.set_is_duplicate()

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
        # Initialize Init
        pygame.init()

        # Tittle
        pygame.display.set_caption("Maze Creator")

        # Create the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(BLACK)

        for cell_row in self.cells:
            for cell in cell_row:
                for wall in cell.walls.values():
                    if not wall.is_duplicate:
                        pygame.draw.line(self.screen, WHITE, wall.start, wall.end)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.update()


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
    m = Maze(900, 700, 50)
    m.create_maze()
    print(f"(rows, cols) in the grid ({len(m.cells)}, {len(m.cells[0])}), total cells = {len(m.cells) * len(m.cells[0])}")
    m.show_maze()
