import pygame

class Tank:
    """A class to manage the tank."""

    def __init__(self, ai_game):
        """Initialize the tank and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the tank image and get its rect.
        self.image = pygame.image.load('images/tank.bmp')
        self.rect = self.image.get_rect()

        # Start each new tank at the bottom center of the screen.
        self.rect.center = self.screen_rect.center

    def blitme(self):
        """Draw the tank at its current location."""
        self.screen.blit(self.image, self.rect)
