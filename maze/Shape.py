"""
Maze Generator DFS
Maze Solver BFS
Luis Enrique Gonzalez
Sunnyvale CA
Noviembre 6, 2020
"""


class Color:
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


class Line:
    WEST = 'west'
    EAST = 'east'
    SOUTH = 'south'
    NORTH = 'north'

    def __init__(self, start_x, start_y, end_x, end_y):
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
        self.is_duplicate = False
        self.is_blocking_wall = True

    def __str__(self):
        return f"Start Point {self.start} , End Point {self.end}"

    def __eq__(self, other):
        top_bottom = self.start == other.start and self.end == other.end
        bottom_up = self.start == other.end and self.end == other.start
        return top_bottom or bottom_up

    def generate_key(self):
        return str(self.start) + str(self.end)

    def set_is_duplicate(self):
        self.is_duplicate = True

    def set_not_blocking_wall(self):
        self.is_blocking_wall = False

    def set_blocking_wall(self):
        self.is_blocking_wall = True

    def mid_point(self):
        m_x = (self.start[0] + self.end[0]) / 2
        m_y = (self.start[1] + self.end[1]) / 2
        return m_x, m_y


class Cell:
    # Direction Vectors
    DIRECTION_ROW = [-1, 1, 0, 0]
    DIRECTION_COL = [0, 0, 1, -1]

    def __init__(self, row: int, col: int, _north: Line, _south: Line, _east: Line, _west: Line):
        self.is_visited = False
        self.row = row
        self.col = col
        self.position_tuple = (row, col)
        # To test we are going to set one wall not drawable
        self.walls = dict(north=_north, south=_south, east=_east, west=_west)

    def add_wall(self, line, direction):
        """
        :param line: Line or Wall to be added
        :param direction: north, south, east and west keys are valid
        :return:
        """
        self.walls[direction] = line

    def set_visited(self):
        self.is_visited = True

    def __eq__(self, other):
        cols_eq = self.col == other.col
        rows_eq = self.row == other.row
        return cols_eq and rows_eq

    def __str__(self):
        return f"Cell({self.row},{self.col})"

    def get_position(self):
        return self.position_tuple
