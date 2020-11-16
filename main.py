from maze.MazeCreator import Maze


def print_maze_info(m):
    print(f"(rows, cols) in the grid ({len(m.cells)}, {len(m.cells[0])}), total cells = {len(m.cells) * len(m.cells[0])}")


if __name__ == '__main__':
    print('Maze Example')
    m = Maze(1800, 1000, 88, 10, 1)
    m.create_maze()
    print_maze_info(m)
    m.show_maze(Maze.DOTTED_PATH)

    m1 = Maze(500, 500, 15)
    m1.create_maze()
    print_maze_info(m1)
    is_bfs = False
    m1.show_maze(Maze.LINED_PATH, is_bfs)
