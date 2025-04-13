from location import Location

import pathfinding


class Character:
    def __init__(self, name, character_type, location):
        self.name = name
        self.type = character_type
        self.location = location

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_location(self):
        return self.location

    def set_location(self, new_location):
        self.location = new_location

class GoodCharacter(Character):
    def __init__(self, name, location, lives):
        super().__init__(name, "İyi", location)
        self.lives = lives


class LukeSkywalker(GoodCharacter):
    def __init__(self, location):
        super().__init__("Luke Skywalker", location, 3)

    def lose_life(self):
        self.lives -= 1
        return self.lives <= 0


class MasterYoda(GoodCharacter):
    def __init__(self, location):
        super().__init__("Master Yoda", location, 3)
    def lose_life(self):
        self.lives -= 0.5
        return self.lives <= 0


class EnemyCharacter(Character):
    def __init__(self, name, location):
        super().__init__(name, "Kötü", location)

    def find_shortest_path(self, maze, target_location):
        pass


class Stormtrooper(EnemyCharacter):
    def __init__(self, location):
        super().__init__("Stormtrooper", location)

    def find_shortest_path(self, maze, target_location):
        return pathfinding.bfs(maze, self.location, target_location)


class DarthVader(EnemyCharacter):
    def __init__(self, location):
        super().__init__("Darth Vader", location)

    def find_shortest_path(self, maze, target_location):
        return pathfinding.bfs_ignore_walls(maze, self.location, target_location)


class KyloRen(EnemyCharacter):
    def __init__(self, location):
        super().__init__("Kylo Ren", location)

    def find_shortest_path(self, maze, target_location):
        return pathfinding.bfs_double_step(maze, self.location, target_location)