import sys
import math
import numpy as np


DIRECTIONS = [
    (-1,  0, 1.0),
    ( 1,  0, 1.0),
    ( 0, -1, 1.0),
    ( 0,  1, 1.0),
    (-1, -1, math.sqrt(2)),
    (-1,  1, math.sqrt(2)),
    ( 1, -1, math.sqrt(2)),
    ( 1,  1, math.sqrt(2)),
]


def dfs(grid: np.ndarray, start: tuple, end: tuple) -> float:
    rows, cols = grid.shape
    r_start, c_start = start
    r_end, c_end = end
    if grid[r_start][c_start] == 1 or grid[r_end][c_end] == 1:
        return -1
    if start == end:
        return 0.0
    visited = set()
    stack = [(r_start, c_start, 0.0)]
    while stack:
        r, c, g = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        for dr, dc, cost in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == 1:
                continue
            if dr != 0 and dc != 0:
                if grid[r][nc] == 1 or grid[nr][c] == 1:
                    continue
            if (nr, nc) in visited:
                continue
            new_g = g + cost
            if nr == r_end and nc == c_end:
                return new_g
            stack.append((nr, nc, new_g))
    return -1

def main():
    lines = sys.stdin.read().split('\n')
    map_file = lines[0].strip()
    x_start, y_start = map(int, lines[1].strip().split())
    x_end, y_end = map(int, lines[2].strip().split())
    grid = np.load(map_file)
    result = dfs(grid, (x_start, y_start), (x_end, y_end))
    print(result)
if __name__ == '__main__':
    main()
