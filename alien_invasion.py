import sys
from time import sleep

import pygame

from button import Button
from settings import Settings
from ship import Ship
from bullet import Bullet
from bullet_for_alien import Bullet_For_Alien
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from random import randint
from shield import Shield

#from tank import Tank
#from rocket import Rocket

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")


        # Create an instance to store game statistics.
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.a = 0

        self.ship = Ship(self)
        self.shield = Shield(self)
        self.alien = Alien(self)
        self.bullets = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.aliens_list = []

        self._create_fleet()
        #self.tank = Tank(self)
        #self.rocket = Rocket(self)

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def _create_fleet(self):
        """Creat the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
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
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)
            self.aliens_list.append(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
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
                self.shield.update()
                self._update_bullets()
                self._update_aliens()
            #self.rocket.update()
            self._update_screen()

    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sb.high_score_file()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._fire_bullet()
                pygame.mixer.music.load('sounds/bullet_sound_1.wav')
                pygame.mixer.music.play(0)
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

                # Move the ship to the right.
                self.ship.rect.x += 1
                for self.shield in self.shields:
                    self.shield.rect.x += 1
                #self.rocket.rect.x += 1
                #self.rocket.rect.y += 1
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _start_game(self):
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()
        self.shield.center_shield()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_d:
            self.ship.moving_right = True
            self.shield.moving_right = True
            #self.rocket.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
            self.shield.moving_left = True
            #self.rocket.moving_left = True
        elif event.key == pygame.K_UP:
            self.rocket.moving_top = True
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_bottom = True
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_q:
            self.sb.high_score_file()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            pygame.mixer.music.load('sounds/bullet_sound_1.wav')
            pygame.mixer.music.play(0)
        elif event.key == pygame.K_e:
            self._show_shield()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
            self.shield.moving_right = False
            #self.rocket.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
            self.shield.moving_left = False
            #self.rocket.moving_left = False
        elif event.key == pygame.K_UP:
            self.rocket.moving_top = False
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_bottom = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _show_shield(self):
        """Create a new shield and add it to the shields group."""
        if len(self.shields) <= self.settings.shields_allowed:
            shield = Shield(self)
            self.shields.add(self.shield)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Updaete bullet positions.
        self.bullets.update()
        self.alien_bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)


        if collisions:

            # Crash sound for aliens hit by bullets.
            crash_sound = pygame.mixer.Sound("sounds/explosion_sound.wav")
            pygame.mixer.Sound.play(crash_sound)

            for aliens in collisions.values():

                self.stats.score += self.settings.alien_points * len(aliens)
                self.stats.destroyed_aliens += 1

            #if self.stats.destroyed_aliens % 4 == 0:
            ran_num = randint(0, len(self.aliens_list))
            if ran_num < len(self.aliens_list):
                if self.aliens_list[ran_num] in self.aliens:
                    self.settings.bullet_rect.midbottom = self.aliens_list[
                        ran_num].rect.midbottom
                    alien_bullet = Bullet_For_Alien(self)
                    self.alien_bullets.add(alien_bullet)

            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self.alien_bullets.empty()
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
        self.alien_bullets.update()

        # Look for alien, bullet and shield collisions.
        collisions_for_shield = pygame.sprite.groupcollide(
                    self.shields, self.alien_bullets, True, True)

        collisions_for_shield = pygame.sprite.groupcollide(
                    self.shields, self.aliens, True, True)

        if collisions_for_shield:
            # Crash sound shields hit by bullets and aliens
            crash_sound = pygame.mixer.Sound("sounds/explosion_sound.wav")
            pygame.mixer.Sound.play(crash_sound)

        # Look for alien, bullet and ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Crash sound for ship hit by bullets and aliens.
        crash_sound = pygame.mixer.Sound("sounds/explosion_sound.wav")
        pygame.mixer.Sound.play(crash_sound)

        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            self.shield.center_shield()

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
        for bullet in self.alien_bullets.sprites():
            bullet.draw_alien_bullet()
        self.aliens.draw(self.screen)
        for self.shield in self.shields:
            self.shield.draw_shield()
        #self.tank.blitme()
        #self.rocket.blitme()

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
