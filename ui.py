import pygame
import sys
from location import Location


class UI:
    def __init__(self, maze, cell_size=50):
        self.maze = maze
        self.cell_size = cell_size
        self.width = maze.width * cell_size
        self.height = maze.height * cell_size

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Star Wars Labirent Oyunu")

        self.colors = {
            "wall": (0, 0, 0),
            "path": (255, 255, 255),
            "player": (255, 255, 0),
            "enemy": (255, 0, 0),
            "door": (0, 0, 255),
            "trophy": (255, 215, 0),
            "path_highlight": (255, 182, 193),
            "background": (200, 200, 200),
            "nearest_enemy_path": (255, 0, 0),
            "start_location": (255, 255, 0)
        }

        self.font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 16)


        self.load_images()

        self.load_sounds()

    def load_images(self):
        self.images = {
            "luke": self.load_and_scale_image("assets/Luke Skywalker.png"),
            "yoda": self.load_and_scale_image("assets/Master Yoda.png"),
            "vader": self.load_and_scale_image("assets/Darth Vader.png"),
            "kylo": self.load_and_scale_image("assets/Kylo Ren.png"),
            "trooper": self.load_and_scale_image("assets/Stromtrooper.png"),
            "trophy": self.load_and_scale_image("assets/Trophy.png"),
            "heart": self.load_and_scale_image("assets/Hearth.png", scale=0.5),
            "half_heart": self.load_and_scale_image("assets/Half Hearth.png", scale=0.5),
            "door": self.load_and_scale_image("assets/Door.png")
        }

        if not all(self.images.values()):
            print("Warning: Some images could not be loaded, using placeholder shapes")
            self.images = {}

    def load_and_scale_image(self, path, scale=1.0):
        try:
            image = pygame.image.load(path)
            new_width = int(self.cell_size * scale)
            new_height = int(self.cell_size * scale)
            return pygame.transform.scale(image, (new_width, new_height))
        except (pygame.error, FileNotFoundError):
            print(f"Could not load image: {path}")
            return None

    def load_sounds(self):
        self.sounds = {}
        try:
            self.sounds["caught"] = pygame.mixer.Sound("assets/caught.wav")
            self.sounds["victory"] = pygame.mixer.Sound("assets/victory .wav")
            self.sounds["game_over"] = pygame.mixer.Sound("assets/game over.wav")
            self.sounds["background_music"] = pygame.mixer.Sound("assets/background_music.wav")
        except (pygame.error, FileNotFoundError):
            print("Warning: Some sounds could not be loaded")

    def draw_maze(self):
        self.screen.fill(self.colors["background"])

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                cell_type = "wall" if self.maze.data[y][x] == 0 else "path"
                pygame.draw.rect(self.screen, self.colors[cell_type], rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

        for door_key, door_loc in self.maze.doors.items():
            x, y = door_loc.get_x(), door_loc.get_y()

            door_rect = pygame.Rect(
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.screen, self.colors["door"], door_rect, 3)

            text = self.small_font.render(door_key, True, self.colors["door"])
            text_rect = text.get_rect(center=(
                x * self.cell_size + self.cell_size // 2,
                y * self.cell_size + self.cell_size // 2
            ))
            self.screen.blit(text, text_rect)

            if "door" in self.images and self.images["door"]:
                self.screen.blit(self.images["door"], door_rect)


        trophy_x, trophy_y = self.maze.trophy_location.get_x(), self.maze.trophy_location.get_y()
        trophy_rect = pygame.Rect(
            trophy_x * self.cell_size,
            trophy_y * self.cell_size,
            self.cell_size,
            self.cell_size
        )

        if "trophy" in self.images and self.images["trophy"]:
            self.screen.blit(self.images["trophy"], trophy_rect)
        else:
            pygame.draw.rect(self.screen, self.colors["trophy"], trophy_rect)
            text = self.small_font.render("🏆", True, (0, 0, 0))
            text_rect = text.get_rect(center=(
                trophy_x * self.cell_size + self.cell_size // 2,
                trophy_y * self.cell_size + self.cell_size // 2
            ))
            self.screen.blit(text, text_rect)

        start_x, start_y = self.maze.player_start.get_x(), self.maze.player_start.get_y()
        start_rect = pygame.Rect(
            start_x * self.cell_size,
            start_y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        if "start_location" in self.images and self.images["start_location"]:
            self.screen.blit(self.images["start_location"], start_rect)
        else:
            pygame.draw.rect(self.screen, self.colors["start_location"], start_rect)
            text = self.small_font.render("", True, (0, 0, 0))
            text_rect = text.get_rect(center=(
                start_x * self.cell_size + self.cell_size // 2,
                start_y * self.cell_size + self.cell_size // 2
            ))
            self.screen.blit(text, text_rect)


    def draw_characters(self, player, enemies, paths=None):
        enemy_paths = []
        enemy_distances = []

        for enemy in enemies:
            path = enemy.find_shortest_path(self.maze, player.get_location())
            enemy_paths.append(path)
            if path:
                enemy_distances.append(len(path) - 1)
            else:
                enemy_distances.append(float('inf'))

        if enemy_distances:
            nearest_enemy_index = enemy_distances.index(min(enemy_distances))
        else:
            nearest_enemy_index = -1

        for i, path in enumerate(enemy_paths):
            if path:
                for loc in path[1:]:
                    path_rect = pygame.Rect(
                        loc.get_x() * self.cell_size,
                        loc.get_y() * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    )

                    if i == nearest_enemy_index:
                        pygame.draw.rect(self.screen, self.colors["nearest_enemy_path"], path_rect)

        player_x, player_y = player.get_location().get_x(), player.get_location().get_y()
        player_rect = pygame.Rect(
            player_x * self.cell_size,
            player_y * self.cell_size,
            self.cell_size,
            self.cell_size
        )

        player_image = None
        if player.get_name() == "Luke Skywalker" and "luke" in self.images:
            player_image = self.images["luke"]
        elif player.get_name() == "Master Yoda" and "yoda" in self.images:
            player_image = self.images["yoda"]

        if player_image:
            self.screen.blit(player_image, player_rect)
        else:
            pygame.draw.rect(self.screen, self.colors["player"], player_rect)
            text = self.small_font.render("P", True, (0, 0, 0))
            text_rect = text.get_rect(center=(
                player_x * self.cell_size + self.cell_size // 2,
                player_y * self.cell_size + self.cell_size // 2
            ))
            self.screen.blit(text, text_rect)

        for i, enemy in enumerate(enemies):
            enemy_x, enemy_y = enemy.get_location().get_x(), enemy.get_location().get_y()
            enemy_rect = pygame.Rect(
                enemy_x * self.cell_size,
                enemy_y * self.cell_size,
                self.cell_size,
                self.cell_size
            )

            enemy_image = None
            if enemy.get_name() == "Darth Vader" and "vader" in self.images:
                enemy_image = self.images["vader"]
            elif enemy.get_name() == "Kylo Ren" and "kylo" in self.images:
                enemy_image = self.images["kylo"]
            elif enemy.get_name() == "Stormtrooper" and "trooper" in self.images:
                enemy_image = self.images["trooper"]

            if enemy_image:
                self.screen.blit(enemy_image, enemy_rect)
            else:
                if i == nearest_enemy_index:
                    pygame.draw.rect(self.screen, (255, 0, 0), enemy_rect)
                else:
                    pygame.draw.rect(self.screen, self.colors["enemy"], enemy_rect)

                initial = enemy.get_name()[0]
                text = self.small_font.render(initial, True, (255, 255, 255))
                text_rect = text.get_rect(center=(
                    enemy_x * self.cell_size + self.cell_size // 2,
                    enemy_y * self.cell_size + self.cell_size // 2
                ))
                self.screen.blit(text, text_rect)

        self.draw_lives(player)

    def draw_lives(self, player):
        heart_size = self.cell_size // 2
        lives = player.lives

        lives_text = self.small_font.render(f"Can: {lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 10))

        if "heart" in self.images and "half_heart" in self.images:
            full_hearts = int(lives)
            for i in range(full_hearts):
                self.screen.blit(self.images["heart"], (10 + i * heart_size, 40))

            if lives - full_hearts >= 0.5:
                self.screen.blit(self.images["half_heart"], (10 + full_hearts * heart_size, 40))
        else:
            life_width = 50
            life_height = 20

            life_border = pygame.Rect(10, 40, 3 * life_width, life_height)
            pygame.draw.rect(self.screen, (255, 255, 255), life_border, 2)

            if player.get_name() == "Luke Skywalker":
                max_lives = 3.0
            else:
                max_lives = 6.0

            life_percent = lives / max_lives
            life_rect = pygame.Rect(10, 40, int(3 * life_width * life_percent), life_height)
            pygame.draw.rect(self.screen, (255, 0, 0), life_rect)

    def show_start_screen(self):
        self.screen.fill((0, 0, 0))

        title = self.font.render("Star Wars Labirent", True, (255, 255, 0))
        subtitle = self.small_font.render("Karakterinizi seçin:", True, (255, 255, 255))

        luke_text = self.font.render("1 - Luke Skywalker", True, (255, 255, 255))
        yoda_text = self.font.render("2 - Master Yoda", True, (255, 255, 255))

        title_rect = title.get_rect(center=(self.width // 2, self.height // 4))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, self.height // 3))
        luke_rect = luke_text.get_rect(center=(self.width // 2, self.height // 2))
        yoda_rect = yoda_text.get_rect(center=(self.width // 2, self.height // 2 + 50))

        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        self.screen.blit(luke_text, luke_rect)
        self.screen.blit(yoda_text, yoda_rect)

        if "luke" in self.images and self.images["luke"]:
            luke_img = self.images["luke"]
            luke_img_rect = luke_img.get_rect(center=(self.width // 4, self.height // 2))
            self.screen.blit(luke_img, luke_img_rect)

        if "yoda" in self.images and self.images["yoda"]:
            yoda_img = self.images["yoda"]
            yoda_img_rect = yoda_img.get_rect(center=(self.width // 4, self.height // 2 + 50))
            self.screen.blit(yoda_img, yoda_img_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "Luke Skywalker"
                    elif event.key == pygame.K_2:
                        return "Master Yoda"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if luke_rect.collidepoint(mouse_pos):
                        return "Luke Skywalker"
                    elif yoda_rect.collidepoint(mouse_pos):
                        return "Master Yoda"

    def show_game_over(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        instruction = self.small_font.render("Tekrar Oynamak için SPACE Tuşuna, Çıkmak İçin ESC, Menüye Dönmek için M Tuşuna Basınız", True,(255, 255, 255))

        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
        instruction_rect = instruction.get_rect(center=(self.width // 2, self.height // 2 + 50))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(instruction, instruction_rect)

        if "game_over" in self.sounds:
            self.sounds["game_over"].play()

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "play_again"
                    elif event.key == pygame.K_ESCAPE:
                        return "quit"
                    elif event.key == pygame.K_m:
                        return "menu"

    def show_victory(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        victory_text = self.font.render("VICTORY!", True, (255, 215, 0))
        instruction = self.small_font.render("Press SPACE to play again, ESC to quit, or M to return to menu", True,
                                             (255, 255, 255))

        victory_rect = victory_text.get_rect(center=(self.width // 2, self.height // 2))
        instruction_rect = instruction.get_rect(center=(self.width // 2, self.height // 2 + 50))

        self.screen.blit(victory_text, victory_rect)
        self.screen.blit(instruction, instruction_rect)


        if "victory" in self.sounds:
            self.sounds["victory"].play()

        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "play_again"
                    elif event.key == pygame.K_ESCAPE:
                        return "quit"
                    elif event.key == pygame.K_m:
                        return "menu"
    def play_caught_sound(self):
        if "caught" in self.sounds:
            self.sounds["caught"].play()

    def show_distance_info(self, enemy_distances):
        y_offset = 70
        for i, (enemy_name, distance) in enumerate(enemy_distances.items()):
            if distance is not None:
                distance_text = self.small_font.render(
                    f"{enemy_name}: {distance} adım uzaklıkta",
                    True,
                    (255, 255, 255)
                )
                self.screen.blit(distance_text, (10, y_offset + i * 25))