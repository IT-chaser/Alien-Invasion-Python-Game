import sys

import pygame
from pygame.sprite import Sprite
from alien_sidewayshooter import Alien
from settings import Settings
from random import randint
from time import sleep
from game_stats_for_sidewayshooter import GameStats
from ship_sideways_shooter import Ship
from bullet_sideways_shooter import Bullet
from button_sideways_shooter import Button
from scoreboard import Scoreboard

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
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.alien = Alien(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the play button.
        self.play_button = Button(self, "Play")
        self.normal_mode_button = Button(self, "Normal")
        self.moderate_mode_button = Button(self, "Moderate")
        self.hard_mode_button = Button(self, "Hard")
        self.buttons = [
            self.play_button,
            self.normal_mode_button,
            self.moderate_mode_button,
            self.hard_mode_button
            ]

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - alien_width
        number_aliens_x = available_space_x // (3 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_width = self.ship.rect.width
        available_space_y = self.settings.screen_height - (2 * alien_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
            # Create an alien and place it in the row.
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien_width = alien.rect.width
            alien.x = 7 * alien_width + 2 * alien_width * alien_number
            #alien.x = randint(100, 1000)
            alien.rect.x = alien.x
            alien.y = alien.rect.height + 2 * alien.rect.height * row_number
            #alien.y = randint(row_number, 600)
            alien.rect.y = alien.y
            self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_left(self):
        """Check if any aliens have reached the left side of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.left <= screen_rect.left:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sb.high_score_file()
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
                    self.sb.high_score_file()
                    sys.exit()
                elif event.key == pygame.K_p:
                    self._start_game()
                elif event.key == pygame.K_s:
                    self.stats.game_active = False
                    pygame.mouse.set_visible(True)
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.ship.moving_bottom = False
                elif event.key == pygame.K_UP:
                    self.ship.moving_top = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        for button in self.buttons:
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            normal_mode = self.normal_mode_button.rect.collidepoint(mouse_pos)
            moderate_mode = self.moderate_mode_button.rect.collidepoint(mouse_pos)
            hard_mode = self.hard_mode_button.rect.collidepoint(mouse_pos)
            if button_clicked and not self.stats.game_active:
                self._start_game()
            elif normal_mode and not self.stats.game_active:
                self._start_game()
            elif moderate_mode and not self.stats.game_active:
                self._start_game()
                self._move_next_level()
            elif hard_mode and not self.stats.game_active:
                self._start_game()
                self.settings.hard_mode()
                self._move_next_level()

    def _start_game(self):
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()
        
        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Updaete bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= 1000:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        self._move_next_level()

    def _move_next_level(self):
        """Move to next level if there is no aliens left."""
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
         then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the left side of the screen.
        self._check_aliens_left()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            b = 0
            for y in range(100, 500, 100):
                self.buttons[b].rect.y = y
                self.buttons[b].msg_image_rect.y = y + 10
                self.buttons[b].draw_button()
                b += 1

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = SidewaysShooter()
    ai.run_game()
