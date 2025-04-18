from collections import deque
import heapq
from location import Location


def bfs(maze, start_location, target_location):
    queue = deque([(start_location, [start_location])])
    visited = set([(start_location.get_x(), start_location.get_y())])

    while queue:
        current_loc, path = queue.popleft()
        if (current_loc.get_x() == target_location.get_x() and
                current_loc.get_y() == target_location.get_y()):
            return path
        for neighbor in maze.get_valid_neighbors(current_loc):
            neighbor_pos = (neighbor.get_x(), neighbor.get_y())
            if neighbor_pos not in visited:
                visited.add(neighbor_pos)
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))

    return None

def bfs_double_step(maze, start_location, target_location):
    queue = deque([(start_location, [start_location])])
    visited = set([(start_location.get_x(), start_location.get_y())])

    while queue:
        current_loc, path = queue.popleft()
        if (current_loc.get_x() == target_location.get_x() and
                current_loc.get_y() == target_location.get_y()):
            return path
        double_neighbors = maze.get_double_step_neighbors(current_loc)

        for double_neighbor in double_neighbors:
            double_pos = (double_neighbor.get_x(), double_neighbor.get_y())

            if double_pos not in visited:
                visited.add(double_pos)
                new_path = path + [double_neighbor]
                queue.append((double_neighbor, new_path))
        normal_neighbors = maze.get_valid_neighbors(current_loc)

        for neighbor in normal_neighbors:
            neighbor_pos = (neighbor.get_x(), neighbor.get_y())

            if neighbor_pos not in visited:
                visited.add(neighbor_pos)
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))

    return None

def bfs_ignore_walls(maze, start_location, target_location):
    queue = deque([(start_location, [start_location])])
    visited = set()

    while queue:
        current_loc, path = queue.popleft()
        current_pos = (current_loc.get_x(), current_loc.get_y())
        if current_pos in visited:
            continue
        if (current_loc.get_x() == target_location.get_x() and
                current_loc.get_y() == target_location.get_y()):
            return path

        visited.add(current_pos)

        for neighbor in maze.get_all_neighbors(current_loc):
            neighbor_pos = (neighbor.get_x(), neighbor.get_y())

            if neighbor_pos not in visited:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))

    return None