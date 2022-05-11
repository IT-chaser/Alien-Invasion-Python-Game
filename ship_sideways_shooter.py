import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.ship_speed = 1.5
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship_1.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the left side of the screen.
        self.rect.midleft = self.screen_rect.midleft

        #Store a decimal value for the ship's vertical position.
        self.y = float(self.rect.y)
        #Movement flag
        self.moving_top = False
        self.moving_bottom = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ship_speed
        if self.moving_top and self.rect.top > 0:
            self.y -= self.ship_speed

        # Update rect object from self.y.
        self.rect.y = int(self.y)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
