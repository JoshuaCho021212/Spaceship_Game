import pygame
import sys
 
pygame.init()
pygame.display.set_caption("Saving Earth")
screen_width=400
screen_height=560
screen = pygame.display.set_mode((screen_width, screen_height))
done = False
is_blue = True
x = screen_width* 0.4
y = screen_height * 0.8

clock = pygame.time.Clock()

img = pygame.image.load("shuttle.jpg")

rect = img.get_rect()


while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                        pygame.quit()
                        sys.exit()
                        
                rect.left = x
                rect.top = y
 
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_UP]: y -= 10
                if pressed[pygame.K_DOWN]: y += 10
                if pressed[pygame.K_LEFT]: x -= 10
                if pressed[pygame.K_RIGHT]:  x += 10

                screen.fill((255, 255, 255))        
                screen.blit(img, rect)
                
                pygame.display.flip()
                clock.tick(60)
