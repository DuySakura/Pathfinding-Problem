import math


def is_valid(maze, x, y):
    rows, cols = maze.shape

    if x < 0 or x >= cols:
        return False

    if y < 0 or y >= rows:
        return False

    return maze[y][x] == 0


DIRECTIONS = [
    (0, -1, 1),
    (0, 1, 1),
    (-1, 0, 1),
    (1, 0, 1),
    (-1, -1, math.sqrt(2)),
    (1, -1, math.sqrt(2)),
    (-1, 1, math.sqrt(2)),
    (1, 1, math.sqrt(2))
]


def get_neighbors(maze, x, y):
    neighbors = []

    for dx, dy, step_cost in DIRECTIONS:
        nx = x + dx
        ny = y + dy

        if not is_valid(maze, nx, ny):
            continue

        # Khong cho di cheo qua goc tuong
        if dx != 0 and dy != 0:
            if not is_valid(maze, x + dx, y):
                continue

            if not is_valid(maze, x, y + dy):
                continue

        neighbors.append(((nx, ny), step_cost))

    return neighbors


def _dls_search(maze, start, goal, limit):
    # Moi frame gom: vi tri, cac o ke, chi so o ke tiep theo
    stack = [[start, get_neighbors(maze, *start), 0]]

    path = [start]
    path_cost = [0]
    in_path = {start}

    nodes_expanded = 1
    cutoff = False

    if start == goal:
        return "FOUND", path, 0, nodes_expanded

    while stack:
        current, neighbors, index = stack[-1]
        depth = len(path) - 1

        if depth >= limit:
            for next_pos, _ in neighbors:
                if next_pos not in in_path:
                    cutoff = True
                    break

            stack.pop()
            in_path.remove(path.pop())
            path_cost.pop()
            continue

        if index >= len(neighbors):
            stack.pop()
            in_path.remove(path.pop())
            path_cost.pop()
            continue

        # Chuyen sang neighbor tiep theo
        next_pos, step_cost = neighbors[index]
        stack[-1][2] += 1

        if next_pos in in_path:
            continue

        path.append(next_pos)
        in_path.add(next_pos)
        path_cost.append(path_cost[-1] + step_cost)

        nodes_expanded += 1

        if next_pos == goal:
            return "FOUND", path.copy(), path_cost[-1], nodes_expanded

        next_neighbors = get_neighbors(maze, *next_pos)

        stack.append([next_pos, next_neighbors, 0])

    if cutoff:
        return "CUTOFF", -1, -1, nodes_expanded

    return "FAILURE", -1, -1, nodes_expanded


def dls(maze, start, goal, limit):
    if limit < 0:
        raise ValueError("Limit phai >= 0")

    if not is_valid(maze, *start):
        return -1, -1, 0

    if not is_valid(maze, *goal):
        return -1, -1, 0

    status, path, cost, nodes_expanded = _dls_search(
        maze, start, goal, limit
    )

    return path, cost, nodes_expanded