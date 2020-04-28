"""Game Statistics"""
import json

class GameStats:
    """Tracking statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # File path for saved high score.
        self.file_path = 'json/saved_file.json'
        # Retrieve saved high score or set it to zero if not found.
        self.high_score = self._load_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def save_high_score(self):
        """Save the high score."""
        high_score = self.high_score
        with open(self.file_path, 'w') as fhand:
            json.dump(high_score, fhand)
        return high_score

    def _load_high_score(self):
        """Load the high score."""
        try:
            with open(self.file_path) as fhand:
                high_score = json.load(fhand)
        except FileNotFoundError:
            return 0
        else:
            return high_score
