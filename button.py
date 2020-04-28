"""Button"""
import pygame.font

class Button:
    """A class to represent buttons in the game."""

    def __init__(self, ai_game, msg=None, x_position=0, y_position=0):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the buttons.
        self.width, self.height = 200, 50
        self.x_position = x_position
        self.y_position = y_position
        self.button_color = (210, 8, 45)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self._create_button()
        #self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _create_button(self):
        """Build the button's rect object and set the correct position."""
        self.rect = pygame.Rect(
            self.x_position, self.y_position, self.width, self.height)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
