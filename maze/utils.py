from maze.Shape import Cell, Line


def draw_line(pygame, screen, line: Line, color):
    pygame.draw.line(screen, color, line.start, line.end)


def draw_rect(pygame, screen, cell: Cell, color, width, height):
    pygame.draw.rect(screen, color, pygame.Rect(cell.walls[Line.NORTH].start[0], cell.walls[Line.NORTH].start[1], width, height))
