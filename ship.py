"""Ship"""
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self._create_ship()
        self._position_ship()

        self._movement_flag()

    def _create_ship(self):
        """Load the ship image and get its rect."""
        self.image = pygame.image.load('images/batu.bmp') # 50*102
        #self.image = pygame.image.load('images/ship.bmp') # 60*48
        self.image = pygame.transform.scale(self.image, (
            self.settings.ship_width, self.settings.ship_height))
        self.rect = self.image.get_rect()

    def _position_ship(self):
        """
        Set the ship in correct position
        and store x,y coordinate in decimal value.
        """
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def _movement_flag(self):
        """Initialize movement flags for the ship."""
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship position based on the movement flag."""
        self._ship_movement()

        # Update rect object from self.x and self.y.
        self.rect.x = self.x
        self.rect.y = self.y

    def _ship_movement(self):
        """Movement control of the ship."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # Update the ship's y value, not the rect.
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
