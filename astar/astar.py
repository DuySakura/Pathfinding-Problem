import sys
import math
import heapq
import numpy as np

SQRT2 = math.sqrt(2)
DIRECTIONS = [
    (1, 0, 1.0),
    (-1, 0, 1.0),
    (0, 1, 1.0),
    (0, -1, 1.0),
    (1, 1, SQRT2),
    (1, -1, SQRT2),
    (-1, 1, SQRT2),
    (-1, -1, SQRT2),
]

def octile_heuristic(x1: int, y1: int, x2: int, y2: int) -> float:
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx + dy) + (SQRT2 - 2.0) * min(dx, dy)

def astar_search(grid: np.ndarray, start: tuple[int, int], goal: tuple[int, int]) -> float:

    height, width = grid.shape
    sx, sy = start
    gx, gy = goal

    if not (0 <= sx < width and 0 <= sy < height) or not (0 <= gx < width and 0 <= gy < height):
        return -1.0
    if grid[sy, sx] == 1 or grid[gy, gx] == 1:
        return -1.0

    initial_h = octile_heuristic(sx, sy, gx, gy)
    priority_queue = [(initial_h, 0.0, sx, sy)]

    g_costs = {(sx, sy): 0.0}

    while priority_queue:
        f, g, x, y = heapq.heappop(priority_queue)
        if (x, y) == (gx, gy):
            return g

        if g > g_costs.get((x, y), float('inf')):
            continue

        for dx, dy, step_cost in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny, nx] == 0:
                if dx != 0 and dy != 0:
                    if grid[y, nx] == 1 or grid[ny, x] == 1:
                        continue

                new_g = g + step_cost
                if new_g < g_costs.get((nx, ny), float('inf')):
                    g_costs[(nx, ny)] = new_g
                    f_cost = new_g + octile_heuristic(nx, ny, gx, gy)
                    heapq.heappush(priority_queue, (f_cost, new_g, nx, ny))

    return -1.0

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    map_path = input_data[0]
    x_start = int(input_data[1])
    y_start = int(input_data[2])
    x_end = int(input_data[3])
    y_end = int(input_data[4])

    grid = np.load(map_path)

    result = astar_search(grid, (x_start, y_start), (x_end, y_end))

    print(f"{result:.8f}")

if __name__ == '__main__':
    main()
