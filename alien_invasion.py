"""Alien Invasion"""
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self._screen_mode()
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        # Create ship instance and initialize Group for game elements.
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self._setup_buttons()

    def _screen_mode(self):
        """Screen Ratio"""
        if self.settings.screen_mode:
            self._setup_fullscreen()
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))

    def _setup_fullscreen(self):
        """Start the game in FULLSCREEN if screen mode == True."""
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

    def _setup_buttons(self):
        """Initialize all the button objects and set the correct position."""
        screen_rect = self.screen.get_rect()
        button = Button(self)
        # x_coordinate of the buttons (center of the screen).
        x_position = screen_rect.centerx - button.width // 2
        # Create the button instance and set its x,y_coordinate.
        self.play_button = Button(self, "Batu Speed", x_position, 350)
        self.hard_button = Button(self, "Rico Speed", x_position, 500)
        self.quit_button = Button(self, "Quit", x_position, 650)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events() # Watch for keypress and mouse events.

            if self.stats.game_active:
                self.ship.update() # Update the ship position based on events.
                self._update_bullets() # Update the bullet based on events.
                self._update_aliens() # Manage the movement and status of the alien fleet.

            self._update_screen() # Redraw the screen during each pass through the loop.

    def _check_events(self):
        """Response to keypress and mouse events."""
        for event in pygame.event.get():
            # Exit the program.
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mousebuttondown_events()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_mousebuttondown_events(self):
        """Respond to mouse button down events."""
        # Get the mouse cursor's x- and y-coordinates.
        mouse_pos = pygame.mouse.get_pos()
        self._check_play_button(mouse_pos)
        self._check_hard_button(mouse_pos)
        self._check_quit_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True


            self._start_game()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_hard_button(self, mouse_pos):
        """Enter hard mode when the player clicks Hard."""
        button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            # Enter hard mode settings.
            self.settings.hard_mode()
            # Reset the game statistics and start the game.
            self.stats.reset_stats()
            self.stats.game_active = True
            self._start_game()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_quit_button(self, mouse_pos):
        """Quit the game when the player clicks Quit."""
        button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.save_high_score()
            sys.exit()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        # Ship movement
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        # Bullet movement
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # System
        elif event.key == pygame.K_ESCAPE:
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_p:
            self.stats.game_active = False
        elif event.key == pygame.K_u:
            self.stats.game_active = True

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if self.settings.bullet_mode:
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
        else:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of the old bullets."""
        self.bullets.update()

        # Get rid of the bullet that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            #print(len(self.bullets))

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, self.settings.bullet_strength, True)
        self._update_game_score(collisions)
        self._start_new_level()

    def _update_game_score(self, collisions):
        """Update the game score."""
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

    def _start_new_level(self):
        """Leveling the game if all aliens were destroyed."""
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet() # Repopulating the fleet.
            self.settings.increase_speed()
            # Increase level.
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

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

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ship_left > 0:
            # Decrement ship left.
            self.stats.ship_left -= 1
            self.scoreboard.prep_ships()
            # Reset all the game elements.
            self._start_game()
            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _start_game(self):
        """Reset all the game elements for a new game."""
        # Get rid of the any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()
        # Reset all the scoreboard items.
        self.scoreboard.pre_images()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Determine the number of aliens each row.
        number_aliens_x = self._numbers_alien_x(alien_width)
        # Determine the number of rows of aliens that fit on the screen.
        number_rows = self._numbers_row(alien_height)

        # Create a fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _numbers_alien_x(self, alien_width):
        """Determine the number of aliens each row."""
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        return number_aliens_x

    def _numbers_row(self, alien_height):
        """Determine the number of rows of aliens that fit on the screen."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (
            3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        return number_rows

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # x_coordinate of alien.
        alien.x = alien_width + 2 * alien_width * alien_number
        # y_coordinate of alien.
        alien.y = 1.5 * alien_height + 2 * alien_height * row_number
        alien.rect.x, alien.rect.y = alien.x, alien.y
        # Add it to the aliens Group()
        self.aliens.add(alien)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.scoreboard.show_score()

        # Draw the buttons if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.hard_button.draw_button()
            self.quit_button.draw_button()

        # Make the most rencently drawn screen visible.
        pygame.display.flip()

if __name__ == "__main__":
    # Make a game instance, and run the game.
    AI = AlienInvasion()
    AI.run_game()
