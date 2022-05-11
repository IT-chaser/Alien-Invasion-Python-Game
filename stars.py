import sys

import pygame
from pygame.sprite import Sprite
from settings import Settings
from random import randint

class Star(Sprite):
    """A class to represent a single star in the fleet."""

    def __init__(self, ai_game):
        """Initialize the star and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        # Load the start image and set its rect attribute.
        self.image = pygame.image.load('images/rocket.bmp')
        self.rect = self.image.get_rect()

        # Start each new star near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the star's exact horizantal position.
        self.x = float(self.rect.x)

class StarMain:
    """Main class for star class"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Stars Layout")

        self.stars = pygame.sprite.Group()
        self.bg_color = (230, 230, 230)
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _create_fleet(self):
        """Create the fleet of star."""
        # Create a star and find the number of aliens in a row.
        # Spacing between each star is equal to one star width.
        star = Star(self)
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_width - (2 * star_width)
        number_star_x = available_space_x // (2 * star_width)

        # Determine the number of rows of stars that fit on the screen.
        available_space_y = self.settings.screen_height - (3 * star_height)
        number_rows = available_space_y // (2 * star_height)

        # Craete the full fleet of stars.
        for row_number in range(number_rows):
            for star_number in range(number_star_x):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
            # Create a star and place it in the row.
            star = Star(self)
            star_width, star_height = star.rect.size
            #star.x = star_width + 2 * star_width * star_number
            star.x = randint(0, 1000)
            star.rect.x = star.x

            #star.rect.y = star.rect.height + 2 * star.rect.height * row_number
            star.rect.y = randint(0, 600)
            self.stars.add(star)

    def _update_screen(self):
        self.stars.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = StarMain()
    ai.run_game()
