class Line:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
        self.is_duplicate = False
        self.is_drawable = True

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

    def set_not_drawable(self):
        self.is_drawable = False


class Cell:

    def __init__(self, row: int, col: int, _north: Line, _south: Line, _east: Line, _west: Line):
        self.row = row
        self.col = col
        # To test we are going to set one wall not drawable
        self.walls = dict(north=_north, south=_south, east=_east, west=_west)

    def add_wall(self, line, direction):
        """
        :param line: Line or Wall to be added
        :param direction: north, south, east and west keys are valid
        :return:
        """
        self.walls[direction] = line
