import pygame
import random

# Initialisierung von Pygame
pygame.init()

# Bildschirmgröße und Farbe
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basement Level")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Spieler
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5
player_image = pygame.Surface((player_width, player_height))
player_image.fill(GREEN)

# Projektile
bullet_width = 5
bullet_height = 10
bullets = []

# Gegner
enemy_width = 50
enemy_height = 50
enemy_speed = 2
enemies = []

# Schriftarten
font = pygame.font.SysFont("Arial", 30)

# Spielerbewegung
def move_player(keys):
    global player_x, player_y
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_height:
        player_y += player_speed

# Schießen
def shoot():
    bullet_x = player_x + player_width // 2 - bullet_width // 2
    bullet_y = player_y
    bullets.append([bullet_x, bullet_y])

# Gegner erstellen
def create_enemy():
    enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
    enemy_y = random.randint(-100, -40)
    enemies.append([enemy_x, enemy_y])

# Gegnerbewegung
def move_enemies():
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > SCREEN_HEIGHT:
            enemies.remove(enemy)

# Projektilbewegung
def move_bullets():
    for bullet in bullets:
        bullet[1] -= 5
        if bullet[1] < 0:
            bullets.remove(bullet)

# Kollision
def check_collisions():
    global enemies, bullets
    for bullet in bullets:
        for enemy in enemies:
            if (bullet[0] > enemy[0] and bullet[0] < enemy[0] + enemy_width and
                bullet[1] > enemy[1] and bullet[1] < enemy[1] + enemy_height):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

# Hauptspiel-Loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot()

    keys = pygame.key.get_pressed()
    move_player(keys)
    move_bullets()
    move_enemies()
    check_collisions()

    # Zeichnen des Spielers
    screen.blit(player_image, (player_x, player_y))

    # Zeichnen der Gegner
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

    # Zeichnen der Schüsse
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Gegner erstellen
    if random.random() < 0.02:
        create_enemy()

    # Bildschirm aktualisieren
    pygame.display.flip()

    # Framerate
    clock.tick(120)

pygame.quit()
