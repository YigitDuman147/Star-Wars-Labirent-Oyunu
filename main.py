import pygame
import random
from location import Location
from Character import LukeSkywalker, MasterYoda, Stormtrooper, DarthVader, KyloRen
from maze import Maze
from ui import UI


def read_map_file(file_path):
    characters = []
    maze_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith('Karakter:'):
                parts = line.strip().split(',')
                char_type = parts[0].split(':')[1].strip()
                door = parts[1].split(':')[1].strip()
                characters.append((char_type, door))
                print(f"Karakter eklendi: {char_type} - Kapı: {door}")
            elif any(c in '01' for c in line):
                digits = [c for c in line if c in '01']
                if digits:
                    maze_row = [int(digit) for digit in digits]
                    maze_data.append(maze_row)

    return characters, maze_data


def create_enemies_with_random_doors(character_types, maze):
    enemies = []
    available_doors = list(maze.doors.keys())

    for char_type in character_types:
        if available_doors:
            random_door = random.choice(available_doors)
            enemy_location = maze.doors[random_door]

            available_doors.remove(random_door)

            print(f"Düşman oluşturuluyor: {char_type} - Kapı: {random_door} (rastgele)")

            if char_type == "Stormtrooper":
                enemies.append(Stormtrooper(enemy_location))
            elif char_type == "Darth Vader":
                enemies.append(DarthVader(enemy_location))
            elif char_type == "Kylo Ren":
                enemies.append(KyloRen(enemy_location))

    return enemies


def main():
    pygame.init()

    pygame.mixer.music.load("assets/background_music.wav")
    pygame.mixer.music.play(-1)

    while True:
        characters, maze_data = read_map_file("Star wars harita.txt")

        maze = Maze(maze_data)

        ui = UI(maze)

        selected_character = ui.show_start_screen()

        if selected_character == "Luke Skywalker":
            player = LukeSkywalker(maze.player_start)
        else:
            player = MasterYoda(maze.player_start)


        character_types = [char_type for char_type, _ in characters]

        enemies = create_enemies_with_random_doors(character_types, maze)

        running = True
        game_over = False
        victory = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not game_over and not victory:
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_ESCAPE]:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                            else:
                                new_location = Location(player.get_location().get_x(), player.get_location().get_y())

                                if event.key == pygame.K_UP:
                                    new_location.set_y(new_location.get_y() - 1)
                                elif event.key == pygame.K_DOWN:
                                    new_location.set_y(new_location.get_y() + 1)
                                elif event.key == pygame.K_LEFT:
                                    new_location.set_x(new_location.get_x() - 1)
                                elif event.key == pygame.K_RIGHT:
                                    new_location.set_x(new_location.get_x() + 1)

                                if maze.is_valid_move(new_location):
                                    player.set_location(new_location)

                                    if maze.is_trophy_location(new_location):
                                        victory = True

                                    for enemy in enemies:
                                        path = enemy.find_shortest_path(maze, player.get_location())
                                        if path and len(path) > 1:
                                            enemy.set_location(path[1])

                                        if enemy.get_location().get_x() == player.get_location().get_x() and \
                                                enemy.get_location().get_y() == player.get_location().get_y():
                                            is_game_over = player.lose_life()

                                            ui.play_caught_sound()

                                            player.set_location(maze.player_start)

                                            enemies = create_enemies_with_random_doors(character_types, maze)

                                            game_over = is_game_over

            ui.draw_maze()
            ui.draw_characters(player, enemies)

            if game_over:
                action = ui.show_game_over()
                if action == "play_again":
                    player = LukeSkywalker(maze.player_start) if isinstance(player, LukeSkywalker) else MasterYoda(
                        maze.player_start)

                    enemies = create_enemies_with_random_doors(character_types, maze)

                    game_over = False
                    victory = False
                elif action == "menu":
                    break
                else:
                    running = False


            elif victory:
                action = ui.show_victory()
                if action == "play_again":
                    player = LukeSkywalker(maze.player_start) if isinstance(player, LukeSkywalker) else MasterYoda(
                        maze.player_start)

                    enemies = create_enemies_with_random_doors(character_types, maze)

                    game_over = False
                    victory = False
                elif action == "menu":
                    break
                else:
                    running = False

            pygame.display.flip()

        if not running:
            break

    pygame.quit()

if __name__ == "__main__":
    main()