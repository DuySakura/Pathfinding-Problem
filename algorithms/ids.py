from .dls import _dls_search, is_valid


def ids(maze, start, goal):
    if not is_valid(maze, *start):
        return -1, -1, 0

    if not is_valid(maze, *goal):
        return -1, -1, 0

    total_expanded = 0

    # So o co the di chuyen
    max_depth = int((maze == 0).sum()) - 1

    for limit in range(max_depth + 1):
        status, path, cost, expanded = _dls_search(
            maze, start, goal, limit
        )

        total_expanded += expanded

        if status == "FOUND":
            return path, cost, total_expanded

        if status == "FAILURE":
            return -1, -1, total_expanded

    return -1, -1, total_expanded