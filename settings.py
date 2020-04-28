"""Settings"""
class Settings:
    """A class to store all setting for Alien Invasion.""" # pylint: disable=too-few-public-methods

    def __init__(self):
        """Initialize the game's settings."""
        # Screen Settings
        self.screen_mode = True # True to run in Full screen mode
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship Settings
        self.ship_width = 100 # 60 / 100
        self.ship_height = 204 #48 / 204
        self.ship_limit = 3

        #Bullet settings
        self.bullet_mode = True # True to turn off ulimited bullets
        self.bullet_type = True # True for qute bullet.
        self.bullet_strength = False # False for penetrated bullet
        self.bullet_width = 10
        self.bullet_height = 30
        self.epic_bullet_width = 30
        self.epic_bullet_height = 81
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #Alien settings
        self.alien_width = 70 # 60 / 60
        self.alien_height = 70 # 58 / 60
        self.fleet_drop_speed = 10

        # Game Settings
        self.speedup_scale = 1.1
        self.difficulty_scale = 5
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throught out the game."""
        self.ship_speed = 15
        self.bullet_speed = 30
        self.alien_speed = 10

        # fleet_direction of 1 represents right; -1 represent left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def hard_mode(self):
        """Change setting to hard mode."""
        self.ship_speed *= self.difficulty_scale
        self.alien_speed *= self.difficulty_scale
