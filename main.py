from maze.MazeGame import Maze


def print_maze_info(maze):
    print(f"(rows, cols) in the grid ({len(maze.cells)}, {len(maze.cells[0])}), total cells = {len(maze.cells) * len(maze.cells[0])}")


if __name__ == '__main__':
    print('Maze Example')
    m = Maze(900, 900, 80, 10, 1)
    m.create_maze()
    print_maze_info(m)
    m.show_maze(Maze.DOTTED_PATH)

    m1 = Maze(700, 700, 15)
    m1.create_maze()
    print_maze_info(m1)
    is_bfs = False
    m1.show_maze(Maze.LINED_PATH, is_bfs)
