import sys

import pygame
from pygame.sprite import Sprite
from settings import Settings
from random import randint

class Raindrop(Sprite):
    """A class to represent a single raindrop in the fleet."""

    def __init__(self, ai_game):
        """Initialize the raindrop and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the raindrop image and set its rect attribute.
        self.image = pygame.image.load('images/rocket.bmp')
        self.rect = self.image.get_rect()

        # Start each new raindrop near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the raindrop's exact horizantal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def update(self):
        """Move the raindrop to the bottom."""
        self.y += self.settings.alien_speed
        self.rect.y = int(self.y)



class RaindropMainClass:
    """Main class for raindrop class"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Raindrops Layout")

        self.raindrops = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            self._update_raindrops()
            self._update_screen()

    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _create_fleet(self):
        """Create the fleet of raindrop."""
        # Create a raindrop and find the number of raindrops in a row.
        # Spacing between each raindrop is equal to one raindrop width.
        raindrop = Raindrop(self)
        raindrop_width, raindrop_height = raindrop.rect.size
        available_space_x = self.settings.screen_width - (2 * raindrop_width)
        number_raindrop_x = available_space_x // (2 * raindrop_width)

        # Determine the number of rows of raindrops that fit on the screen.
        available_space_y = self.settings.screen_height - (3 * raindrop_height)
        number_rows = available_space_y // (2 * raindrop_height)

        # Craete the full fleet of raindrops.
        for raindrop_number in range(number_raindrop_x):
            for row_number in range(number_rows):
                self._create_raindrop()

    def _create_raindrop(self):
            # Create a raindrop and place it in the row.
            raindrop = Raindrop(self)
            raindrop_width, raindrop_height = raindrop.rect.size
            #raindrop.x = raindrop_width + 2 * raindrop_width * raindrop_number
            raindrop.x = randint(0, 1000)
            raindrop.rect.x = raindrop.x

            #raindrop.rect.y = raindrop.rect.height
            #raindrop.rect.y += 2 * raindrop.rect.height * row_number
            raindrop.y = randint(0, 600)
            raindrop.rect.y = raindrop.y
            self.raindrops.add(raindrop)

    def _new_raindrop(self):
        """Create a new raindrop and add it to the raindrops group."""
        if len(self.raindrops) < self.settings.raindrops_allowed:
            new_raindrop = Raindrop(self)
            new_raindrop.x = randint(0, 1000)
            new_raindrop.rect.x = new_raindrop.x
            new_raindrop.y = randint(0, 600)
            new_raindrop.rect.y = new_raindrop.y
            self.raindrops.add(new_raindrop)


    def _update_raindrops(self):
        """Update the positions of all raindrops."""
        self.raindrops.update()

        # Get rid of raindrops that have disappeared.
        for raindrop in self.raindrops.copy():
            if raindrop.rect.top >= 600:
                self.raindrops.remove(raindrop)
            self._new_raindrop()

    def draw_raindrop(self):
        """Draw the raindrop to the screen."""
        self.raindrops.draw(self.screen)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for raindrop in self.raindrops.sprites():
            self.draw_raindrop()
        #self._create_raindrop()


        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = RaindropMainClass()
    ai.run_game()
