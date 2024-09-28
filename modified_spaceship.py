import pygame
import random
import sys
from time import sleep

# Game Settings
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SHUTTLE_SIZE = (53, 111)  # width, height
ASTEROID_SIZE = (39, 22)  # width, height
MISSILE_LIMIT = 2
DESTROY_COUNT = 0
SHUTTLE_LIVES = 3

# Initialize Game
def initialize():
    global screen, clock, shuttle_img, missile_img, asteroid_img, sound_shot, sound_explosion, sound_destroy

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Defender of Earth")

    # Load images and sounds
    shuttle_img = pygame.image.load('shuttle.jpg')
    asteroid_img = pygame.image.load('ast.png')
    missile_img = pygame.image.load('mis.png')
    sound_shot = pygame.mixer.Sound('shot.wav')
    sound_explosion = pygame.mixer.Sound('big.wav')
    sound_destroy = pygame.mixer.Sound('small.wav')
    clock = pygame.time.Clock()

# Draw Object on Screen
def draw_image(image, x, y):
    screen.blit(image, (x, y))

# Handle Collision
def handle_collision():
    pygame.display.update()
    sleep(3)
    main_game_loop()

# Display Current Score
def display_score(score):
    font = pygame.font.SysFont('malgungothic', 20)
    score_text = font.render(f"SCORE: {score}", True, (0, 0, 255))
    screen.blit(score_text, (10, 10))

# End the Game
def end_game():
    font = pygame.font.SysFont('malgungothic', 50)
    end_text = "Mission Complete!" if DESTROY_COUNT == 100 else "Game Over!"
    text_color = (0, 255, 0) if DESTROY_COUNT == 100 else (255, 0, 0)
    
    # Render text
    rendered_text = font.render(end_text, True, text_color)
    
    # Get the width and height of the rendered text
    text_width = rendered_text.get_width()
    text_height = rendered_text.get_height()
    
    # Center the text on the screen
    text_x = (SCREEN_WIDTH - text_width) // 2
    text_y = (SCREEN_HEIGHT - text_height) // 2
    
    # Display text
    screen.blit(rendered_text, (text_x, text_y))
    
    pygame.display.update()
    sleep(2)
    main_game_loop()

# Main Game Loop
def main_game_loop():
    global DESTROY_COUNT, SHUTTLE_LIVES

    missiles = []
    x_pos = SCREEN_WIDTH * 0.4
    y_pos = SCREEN_HEIGHT * 0.75
    x_change = 0

    # Initialize Asteroid
    asteroid_x = random.randint(0, SCREEN_WIDTH - ASTEROID_SIZE[0])
    asteroid_y = 0
    asteroid_speed = 3

    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_SPACE:
                    sound_shot.play()
                    if len(missiles) < MISSILE_LIMIT:
                        missile_x = x_pos + SHUTTLE_SIZE[0] / 2
                        missile_y = y_pos - SHUTTLE_SIZE[1] / 4
                        missiles.append([missile_x, missile_y])

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    x_change = 0

        screen.fill((255, 255, 255))

        # Move Shuttle
        x_pos += x_change
        if x_pos < 0:
            x_pos = 0
        elif x_pos > SCREEN_WIDTH - SHUTTLE_SIZE[0]:
            x_pos = SCREEN_WIDTH - SHUTTLE_SIZE[0]

        # Collision Check: Shuttle & Asteroid
        if y_pos < asteroid_y + ASTEROID_SIZE[1]:
            if asteroid_x > x_pos and asteroid_x < x_pos + SHUTTLE_SIZE[0]:
                SHUTTLE_LIVES -= 1
                sound_explosion.play()
                handle_collision()

        if SHUTTLE_LIVES == 0 or DESTROY_COUNT == 100:
            end_game()

        draw_image(shuttle_img, x_pos, y_pos)

        # Move Missiles
        if missiles:
            for missile in missiles[:]:
                missile[1] -= 10
                if missile[1] < 0:
                    missiles.remove(missile)

                # Check for Collision: Missile & Asteroid
                if asteroid_y < missile[1] < asteroid_y + ASTEROID_SIZE[1]:
                    if asteroid_x < missile[0] < asteroid_x + ASTEROID_SIZE[0]:
                        sound_destroy.play()
                        DESTROY_COUNT += 10
                        missiles.remove(missile)
                        asteroid_x = random.randint(0, SCREEN_WIDTH - ASTEROID_SIZE[0])
                        asteroid_y = 0

            for missile_x, missile_y in missiles:
                draw_image(missile_img, missile_x, missile_y)

        # Update Score
        display_score(DESTROY_COUNT)

        # Move Asteroid
        asteroid_y += asteroid_speed
        if asteroid_y > SCREEN_HEIGHT:
            asteroid_y = 0
            asteroid_x = random.randint(0, SCREEN_WIDTH - ASTEROID_SIZE[0])

        draw_image(asteroid_img, asteroid_x, asteroid_y)

        pygame.display.update()
        clock.tick(60)

# Start Game
initialize()
main_game_loop()