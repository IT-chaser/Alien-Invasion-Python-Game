import sys

import pygame

class Keys:
    """Initialaze the screen and its resources"""

    def __init__(self):
        """Start the main loop for the empty screen"""
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Keys analysis")

    def run_keys(self):
        """Start tha main loop for the keys."""
        while True:
            # Watch for keyboard events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    print(event)

            # Make the most drawn screen visible.
            pygame.display.flip()

if __name__ == '__main__':
    # Make a key instance, and run the keys.
    ai = Keys()
    ai.run_keys()
