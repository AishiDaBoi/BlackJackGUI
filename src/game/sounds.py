import pygame

pygame.mixer.init()

def play_sound(file):
    """Spielt einen Soundeffekt ab."""
    pygame.mixer.Sound(file).play()
