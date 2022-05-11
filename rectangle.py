import pygame
import pygame.font
from pygame.sprite import Sprite

class Rectangle(Sprite):
    """A class to represent a single rectangle in the fleet."""

    def __init__(self, ai_game):
        """Initialize the rectangle and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.settings = ai_game.settings

        # Set the dimensions and properties of the bottom.
        self.width, self.height = 200, 50
        self.rectangle_color = (0, 255, 155)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topright = self.screen_rect.topright

        # The rectangle message needs to be prepped only once.
        #self._prep_msg(msg)

        # Start each new rectangle near the top left of the screen.
        self.rect.x = self.screen_rect.width
        self.rect.y = self.screen_rect.height

        # Store the rectangle's exact horizantal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Return True if rectangle is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
            return True

    def update(self):
        """Move the rectangle to the left."""
        self.y -= (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.y = self.y

    def draw_rectangle(self):
        # Draw blank rectangle and then draw message.
        self.screen.fill(self.rectangle_color, self.rect)
        #self.screen.blit(self.msg_image, self.msg_image_rect)
