"""
Maze Generator DFS
Maze Solver BFS
Luis Enrique Gonzalez
Sunnyvale CA
Noviembre 6, 2020
"""
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

    def get_position_tuple(self):
        return self.position_tuple
