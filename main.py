import pygame
from pygame_cards.classics import CardSets

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create a Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Card Display")

# Set up the game clock
clock = pygame.time.Clock()

# A set of 52 cards from the classic sets
card_set = CardSets.n52

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a background color
    screen.fill((0, 128, 0))  # Green background (like a poker table)

    # Simply blit the graphics surface of the first card (Ace of Spades, usually)
    screen.blit(card_set[0].graphics.surface, (100, 100))  # Position at (100, 100)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
