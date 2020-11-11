"""
Maze Generator DFS
Maze Solver BFS
Luis Enrique Gonzalez
Sunnyvale CA
Noviembre 6, 2020
"""
from maze.Shape import Cell, Line


def update_display(_pygame, _fps_clock, _fps):
    _pygame.display.update()
    _fps_clock.tick(_fps)


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
                     pygame.Rect(cell.walls[Line.NORTH].start[0] + delta_x, cell.walls[Line.NORTH].start[1] + delta_y,
                                 side, side))


def remove_walls(current_cell, rnd_cell, current_row, current_col):
    if current_row == rnd_cell.row:
        relative_col_pos = current_col - rnd_cell.col
        if relative_col_pos == 1:
            # we remove current cell west wall and rnd east wall
            current_cell.walls[Line.WEST].set_not_blocking_wall()
            rnd_cell.walls[Line.EAST].set_not_blocking_wall()
        elif relative_col_pos == -1:
            # we remove current cell's east wall and rnd cell's west wall
            current_cell.walls[Line.EAST].set_not_blocking_wall()
            rnd_cell.walls[Line.WEST].set_not_blocking_wall()
    elif current_col == rnd_cell.col:
        relative_row_pos = current_row - rnd_cell.row
        if relative_row_pos == 1:
            # Remove current's North and Rnd's South
            current_cell.walls[Line.NORTH].set_not_blocking_wall()
            rnd_cell.walls[Line.SOUTH].set_not_blocking_wall()
        elif relative_row_pos == -1:
            current_cell.walls[Line.SOUTH].set_not_blocking_wall()
            rnd_cell.walls[Line.NORTH].set_not_blocking_wall()


def get_direction(row, col, i):
    rr = row + Cell.DIRECTION_ROW[i]
    cc = col + Cell.DIRECTION_COL[i]
    return rr, cc


def is_there_path(current_cell, next_cell):
    is_path = False
    if current_cell.row == next_cell.row:
        relative_col_pos = current_cell.col - next_cell.col
        if relative_col_pos == 1:
            # we remove current cell west wall and rnd east wall
            if not current_cell.walls[Line.WEST].is_blocking_wall and not next_cell.walls[
                Line.EAST].set_not_blocking_wall():
                is_path = True
        elif relative_col_pos == -1:
            # we remove current cell's east wall and rnd cell's west wall
            if not current_cell.walls[Line.EAST].is_blocking_wall and not next_cell.walls[
                Line.WEST].set_not_blocking_wall():
                is_path = True
    elif current_cell.col == next_cell.col:
        relative_row_pos = current_cell.row - next_cell.row
        if relative_row_pos == 1:
            # Remove current's North and Rnd's South
            if not current_cell.walls[Line.NORTH].is_blocking_wall and not next_cell.walls[
                Line.SOUTH].set_not_blocking_wall():
                is_path = True
        elif relative_row_pos == -1:
            if not current_cell.walls[Line.SOUTH].is_blocking_wall and not next_cell.walls[
                Line.NORTH].set_not_blocking_wall():
                is_path = True
    return is_path
