import pygame

from pygame.sprite import Sprite

class Shield(Sprite):
    """A class to manage shield for the ship."""

    def __init__(self, ai_game):
        """Create a shield object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.color = self.settings.shield_color

        # Create a shield's rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.shield_width,
            self.settings.shield_height)

        # Start each new shield at the bottom center of the screen.
        self.rect.midbottom = ai_game.ship.rect.midbottom
        self.rect.y = self.screen_rect.y + 520

        # Store a decimal value for the shield's horizontal postion.
        self.x = float(self.rect.x)
        #self.y = float(self.rect.y)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the shield's postion based on the movement flag."""
        # Update the shield's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x


    def draw_shield(self):
        """Draw the shield to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def center_shield(self):
        """Center the shield on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y = self.screen_rect.y + 520
        self.x = float(self.rect.x)
        #self.y = float(self.rect.y)
