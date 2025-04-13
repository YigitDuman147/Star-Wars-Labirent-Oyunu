from location import Location


class Maze:
    def __init__(self, maze_data):
        self.data = maze_data
        self.height = len(maze_data)
        self.width = len(maze_data[0]) if self.height > 0 else 0

        self.doors = {
            'A': Location(0, 5),
            'B': Location(4, 0),
            'C': Location(12, 0),
            'D': Location(13, 5),
            'E': Location(4, 10)
        }

        self.trophy_location = Location(13, 9)

        self.player_start = Location(6, 5)

    def is_valid_move(self, location):
        x, y = location.get_x(), location.get_y()

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False

        return self.data[y][x] == 1

    def is_wall(self, location):
        x, y = location.get_x(), location.get_y()

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True

        return self.data[y][x] == 0

    def is_trophy_location(self, location):
        return location.get_x() == self.trophy_location.get_x() and \
            location.get_y() == self.trophy_location.get_y()

    def get_valid_neighbors(self, location):
        x, y = location.get_x(), location.get_y()
        neighbors = []

        directions = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)
        ]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            new_location = Location(new_x, new_y)

            if self.is_valid_move(new_location):
                neighbors.append(new_location)

        return neighbors

    def get_all_neighbors(self, location):
        x, y = location.get_x(), location.get_y()
        neighbors = []

        directions = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)
        ]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                neighbors.append(Location(new_x, new_y))

        return neighbors

    def get_double_step_neighbors(self, location):
        x, y = location.get_x(), location.get_y()
        neighbors = []

        double_directions = [
            (0, -2),
            (2, 0),
            (0, 2),
            (-2, 0),
            (1, -1),
            (1, 1),
            (-1, 1),
            (-1, -1)
        ]

        for dx, dy in double_directions:
            new_x, new_y = x + dx, y + dy
            new_location = Location(new_x, new_y)

            mid_x, mid_y = x + dx // 2, y + dy // 2
            mid_location = Location(mid_x, mid_y)

            if 0 <= new_x < self.width and 0 <= new_y < self.height and \
                    self.is_valid_move(new_location) and self.is_valid_move(mid_location):
                neighbors.append(new_location)

        return neighbors

    def print_maze(self):
        for row in self.data:
            print(''.join(['#' if cell == 0 else ' ' for cell in row]))

    def get_door_location(self, door_key):
        return self.doors.get(door_key)