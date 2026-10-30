
def is_valid(maze, x, y):
    rows, cols = maze.shape

    if x < 0 or x >= cols:
        return False

    if y < 0 or y >= rows:
        return False

    if maze[y][x] == 1:
        return False

    return True

DIRECTIONS = [
    (0, -1, 1),    # Len
    (0, 1, 1),     # Xuong
    (-1, 0, 1),    # Trai
    (1, 0, 1),     # Phai

    (-1, -1, 2),   # Cheo tren trai
    (1, -1, 2),    # Cheo tren phai
    (-1, 1, 2),    # Cheo duoi trai
    (1, 1, 2)      # Cheo duoi phai
]

def dls(maze, start, goal, limit):
    # Kiem tra vi tri bat dau va ket thuc
    if not is_valid(maze, *start):
        return None, None, 0

    if not is_valid(maze, *goal):
        return None, None, 0

    if limit < 0:
        raise ValueError("Limit phai >= 0")

    # Moi phan tu gom:
    # (vi_tri, duong_di, chi_phi, do_sau)
    stack = [(start, [start], 0, 0)]

    nodes_expanded = 0

    while stack:
        current, path, cost, depth = stack.pop()

        nodes_expanded += 1

        # Neu da den dich
        if current == goal:
            return path, cost, nodes_expanded

        # Neu dat gioi han do sau
        if depth >= limit:
            continue

        x, y = current

        # Duyet 8 huong di chuyen
        for dx, dy, step_cost in reversed(DIRECTIONS):
            nx = x + dx
            ny = y + dy

            next_pos = (nx, ny)

            # Kiem tra o hop le
            if not is_valid(maze, nx, ny):
                continue

            # Khong di lai o da co trong duong
            if next_pos in path:
                continue

            stack.append((
                next_pos,
                path + [next_pos],
                cost + step_cost,
                depth + 1
            ))

    return None, None, nodes_expanded

