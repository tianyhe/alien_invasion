"""Scoreboard"""
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self._font_settings()
        self.pre_images()

    def _font_settings(self):
        """Font settings for scoring information."""
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.high_text_color = (153, 0, 61)
        self.high_font = pygame.font.SysFont(None, 60)

    def pre_images(self):
        """Prepare the initial image for all the scoreboard items."""
        self.prep_score() # Prepare the initial score image.
        self.prep_high_score() # Prepare the initial score image.
        self.prep_level() # Prepare the initial level image.
        self.prep_ships() # Prepare the initial ship limit.

    def prep_score(self):
        """Turn the score into a rendered images."""
        round_score = round(self.stats.score, -1)
        score_str = f"Score: " + "{:,}".format(round_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered images."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High Score:" + "{:,}".format(high_score)
        self.high_score_image = self.high_font.render(
            high_score_str, True, self.high_text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        """Turn the level into a rendered images."""
        level_str = f"Level: {str(self.stats.level)}"
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.transform.scale(ship.image, (
                self.settings.ship_width // 3, self.settings.ship_height // 3))
            ship.rect.x = 10 + 1.3 * ship_number * self.settings.ship_width // 3
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
