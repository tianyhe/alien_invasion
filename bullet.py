"""Bullet"""
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current location."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self._create_bullet()
        self._position_bullet(ai_game)

    def _create_bullet(self):
        """Load the bullet image or create a bullet rect."""
        if self.settings.bullet_type:
            self.image = pygame.image.load('images/rocket.bmp') # 30*81
            self.image = pygame.transform.scale(self.image, (
                self.settings.epic_bullet_width, self.settings.epic_bullet_height))
        else:
            self.rect = pygame.Rect(
                0, 0, self.settings.bullet_width, self.settings.bullet_height)

    def _position_bullet(self, ai_game):
        """
        Set the bullet in correct position.
        and store y coordinate in decimal value.
        """
        if self.settings.bullet_type:
            self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        #Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        if self.settings.bullet_type:
            self.screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)
