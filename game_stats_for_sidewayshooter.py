class GameStats:
    """Track statistics for Sideways Shooter."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start Sideways Shooter in an active state.
        self.game_active = False

        # High score should never be reset.
        with open('high_score.txt') as f:
            contents = f.read()
            if contents:
                self.high_score = int(contents)
            else:
                self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
