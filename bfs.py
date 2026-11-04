import sys
import math
import numpy as np
from collections import deque


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


def bfs(grid: np.ndarray, start: tuple, end: tuple) -> float:
    rows, cols = grid.shape
    r_start, c_start = start
    r_end, c_end = end
    if grid[r_start][c_start] == 1 or grid[r_end][c_end] == 1:
        return -1
    if start == end:
        return 0.0
    visited = np.full((rows, cols), -1.0)
    visited[r_start][c_start] = 0.0
    queue = deque()
    queue.append((r_start, c_start, 0.0))
    while queue:
        r, c, g = queue.popleft()
        for dr, dc, cost in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == 1:
                continue
            if dr != 0 and dc != 0:
                if grid[r][nc] == 1 or grid[nr][c] == 1:
                    continue
            new_g = g + cost
            if visited[nr][nc] == -1.0:
                visited[nr][nc] = new_g
                if nr == r_end and nc == c_end:
                    return new_g
                queue.append((nr, nc, new_g))
    return -1

def main():
    lines = sys.stdin.read().split('\n')
    map_file = lines[0].strip()
    x_start, y_start = map(int, lines[1].strip().split())
    x_end, y_end = map(int, lines[2].strip().split())
    grid = np.load(map_file)
    result = bfs(grid, (x_start, y_start), (x_end, y_end))
    print(result)

if __name__ == '__main__':
    main()
