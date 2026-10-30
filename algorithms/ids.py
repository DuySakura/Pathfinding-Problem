
from .dls import dls, is_valid


def ids(maze, start, goal, max_depth=20):
    """
    Iterative Deepening Search

    maze: Ban do me cung
    start: Toa do bat dau (x, y)
    goal: Toa do dich (x, y)
    max_depth: Gioi han do sau toi da

    Return:
        path, cost, total_expanded
    """

    if max_depth < 0:
        raise ValueError("max_depth phai >= 0")

    if not is_valid(maze, *start):
        return None, None, 0

    if not is_valid(maze, *goal):
        return None, None, 0

    total_expanded = 0

    # Tang gioi han do sau tu 0 den max_depth
    for limit in range(max_depth + 1):

        path, cost, expanded = dls(
            maze, start, goal, limit
        )

        total_expanded += expanded

        # Neu tim thay duong di
        if path is not None:
            return path, cost, total_expanded

    # Khong tim thay duong di
    return None, None, total_expanded
