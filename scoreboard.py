import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_images()

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        high_score_lable_str = "High Score: "
        self.high_score_lable_image = self.font.render(high_score_lable_str,
                True, self.text_color, self.settings.bg_color)
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)

        # Center the high score lable at the top of the screen.
        self.high_score_lable_rect = self.high_score_lable_image.get_rect()
        self.high_score_lable_rect.centerx = self.screen_rect.centerx - 210
        self.high_score_lable_rect.top = self.score_rect.top

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        score_lable_str = "Score: "
        self.score_lable_image = self.font.render(score_lable_str, True,
                self.text_color, self.settings.bg_color)

        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)

        # Display the score lable at the top right of the screen.
        self.score_lable_rect = self.score_lable_image.get_rect()
        self.score_lable_rect.right = self.screen_rect.right - 170
        self.score_lable_rect.top = 20

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.score_lable_image, self.score_lable_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.high_score_lable_image, self.high_score_lable_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.level_lable_image, self.level_lable_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def high_score_file(self):
        """Write the high score to the file."""
        with open("high_score.txt", "w") as f:
            f.write(str(self.stats.high_score))

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        level_lable_str = "Level: "
        self.level_lable_image = self.font.render(level_lable_str, True,
                self.text_color, self.settings.bg_color)

        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)

        # Position the level lable below the score.
        self.level_lable_rect = self.level_lable_image.get_rect()
        self.level_lable_rect.right = self.score_rect.right - 40
        self.level_lable_rect.top = self.score_rect.bottom + 10

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_images(self):
        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
