from maze.Shape import Cell, Line


def draw_line(pygame, screen, line: Line, color):
    pygame.draw.line(screen, color, line.start, line.end)


def draw_rectangle(pygame, screen, cell: Cell, color, width, height):
    pygame.draw.rect(screen, color,
                     pygame.Rect(cell.walls[Line.NORTH].start[0], cell.walls[Line.NORTH].start[1], width, height))


def draw_square(pygame, screen, cell: Cell, color, side, rectangle_size):
    """
    Drawing the player centered
    :param pygame:
    :param screen:
    :param cell:
    :param color:
    :param side:
    :param rectangle_size:
    :return:
    """
    delta = rectangle_size - side
    delta_x = delta / 2
    delta_y = delta / 2
    pygame.draw.rect(screen, color,
                     pygame.Rect(cell.walls[Line.NORTH].start[0] + delta_x, cell.walls[Line.NORTH].start[1] + delta_y, side, side))
