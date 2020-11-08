import time
import pygame
from pygame import mixer

# Constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)


class Line:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)

    def __str__(self):
        return f"Start Point {self.start} , End Point {self.end}"

    def __eq__(self, other):
        top_bottom = self.start == other.start and self.end == other.end
        bottom_up = self.start == other.end and self.end == other.start
        return top_bottom or bottom_up


class Maze:

    def __init__(self, screen_width, screen_height, cell_size, margin=10):
        if screen_width < 100 or screen_height < 100:
            raise ValueError(
                f"Either Screen width = {screen_width} or Screen Height = {screen_height} must be at least 100")
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.screen = None
        self.cell_size = cell_size
        self.margin = margin
        self.lines = {}

    def create_maze(self):
        """
        Create Maze will create the grid, to create the grid we are going to create the lines
        then we will draw those lines, we are also taking into account a margin
        :return:
        """
        num_horizontal_cells = int((self.screen_width - self.margin) / self.cell_size)
        num_vertical_cells = int((self.screen_height - self.margin) / self.cell_size)

        # Creating the lines for the grid
        start_x = self.margin
        start_y = self.margin
        for row in range(1, num_vertical_cells + 1):
            for col in range(1, num_horizontal_cells + 1):
                delta_x = start_x + self.cell_size
                delta_y = start_y + self.cell_size
                north = Line(start_x, start_y, delta_x, start_y)
                south = Line(start_x, delta_y, delta_x, delta_y)
                east = Line(delta_x, start_y, delta_x, delta_y)
                west = Line(start_x, start_y, start_x, delta_y)
                # increment x by cell size
                start_x = start_x + self.cell_size
            # increment y by cell size
            start_y = start_y + self.cell_size
            start_x = self.margin



        # Initialize Init
        pygame.init()

        pygame.draw.line(self.screen, )

        # Create the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))


if __name__ == "__main__":
    print(f'Welcome home Maze creator {time.time()}')
    l1 = Line(1, 2, 3, 5)
    l2 = Line(1, 2, 3, 5)
    print(l1)
    l = 30
    for r in range(1, l + 1):
        print(r)
    sd = (1, 2)
    sd1 = (1, 2)
    print(sd == sd1)
