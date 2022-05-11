import sys

import pygame
from pygame.sprite import Sprite
from rectangle import Rectangle
from settings import Settings
from random import randint
from time import sleep
from game_stats_for_sidewayshooter import GameStats
from target_practice_button import Button

class Ship:
    """A class to manage the ship."""
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
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
class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        self.bullet_speed = 1.5
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60 ,60)


        super().__init__()
        self.screen = ai_game.screen
        self.color = self.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.bullet_width,
            self.bullet_height)
        self.rect.midright = ai_game.ship.rect.midright

        # Store the bullet's position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet cross the screen."""
        # Update the decimal position of the bullet.
        self.x += self.bullet_speed
        # Update the rect position.
        self.rect.x = int(self.x)


    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

class SidewaysShooter:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("SideWays Shooter")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.bullets_allowed = 15

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.rectangles = pygame.sprite.Group()

        self._create_fleet()
        # Set the background color.
        self.bg_color = (230, 230, 230)

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def _check_rectangles_left(self):
        """Check if any rectangless have reached the left side of the screen."""
        screen_rect = self.screen.get_rect()
        for rectangle in self.rectangles.sprites():
            if rectangle.rect.left <= screen_rect.left:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by a rectangle."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining rectangles and bullets.
            self.rectangles.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _create_fleet(self):
        """Create the fleet of rectangles."""
        # Create an rectangle and find the number of rectangles in a row.
        # Spacing between each rectangle is equal to one rectangle width.
        rectangle = Rectangle(self)
        rectangle_width, rectangle_height = rectangle.rect.size
        available_space_x = self.settings.screen_width - rectangle_width
        number_rectangles_x = available_space_x // (3 * rectangle_width)

        # Determine the number of rows of rectangles that fit on the screen.
        ship_width = self.ship.rect.width
        available_space_y = self.settings.screen_height - (2 * rectangle_height)
        number_rows = available_space_y // (2 * rectangle_height)

        # Create the full fleet of rectangles.
        for row_number in range(number_rows):
            for rectangle_number in range(number_rectangles_x):
                self._create_rectangle(rectangle_number, row_number)

    def _create_rectangle(self, rectangle_number, row_number):
            # Create an rectangle and place it in the row.
            rectangle = Rectangle(self)
            rectangle_width, rectangle_height = rectangle.rect.size
            rectangle_width = rectangle.rect.width
            #rectangle.x = 7 * rectangle_width + 2 * rectangle_width * rectangle_number
            rectangle.x = randint(100, 1000)
            rectangle.rect.x = rectangle.x
            rectangle.y = rectangle.rect.height + 2 * rectangle.rect.height * row_number
            #rectangle.y = randint(row_number, 600)
            rectangle.rect.y = rectangle.y
            self.rectangles.add(rectangle)

    def _check_fleet_edges(self):
        """Respond appropriately if any rectangles have reached an edge."""
        for rectangle in self.rectangles.sprites():
            if rectangle.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for rectangle in self.rectangles.sprites():
            rectangle.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_rectangles()

                # Get rid of bullets that have disappeared.
                for bullet in self.bullets.copy():
                    if bullet.rect.left >= 1000:
                        self.bullets.remove(bullet)
                # Check for any bullets that have hit rectangles.
                # If so, get rid of the bullet and the rectangle.
                collisions = pygame.sprite.groupcollide(
                        self.bullets, self.rectangles, True, True)


            self._update_screen()


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.ship.moving_bottom = True
                elif event.key == pygame.K_UP:
                    self.ship.moving_top = True
                elif event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.ship.moving_bottom = False
                elif event.key == pygame.K_UP:
                    self.ship.moving_top = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            
            # Reset game stats.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Get rid of any remaining rectangles and bullets.
            self.rectangles.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Updaete bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_rectangle_collisions()

    def _check_bullet_rectangle_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and rectangles that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.rectangles, True, True)

        if not self.rectangles:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_rectangles(self):
        """
        Check if the fleet is at an edge,
         then update the positions of all rectangles in the fleet.
        """
        self._check_fleet_edges()
        self.rectangles.update()

        # Look for rectangle-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.rectangles):
            self._ship_hit()

        # Look for rectangles hitting the left side of the screen.
        self._check_rectangles_left()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Draw the rectangle.
        for play_rectangle in self.rectangles.sprites():
            play_rectangle.draw_rectangle()

        #Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = SidewaysShooter()
    ai.run_game()
