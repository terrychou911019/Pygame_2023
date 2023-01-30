import pygame, sys

def rotate(surface, angle):
    rotated_surface = pygame.transform.rotozoom(surface, angle, 1)
    rotated_surface_rect = rotated_surface.get_rect(center = (300, 300))
    return rotated_surface, rotated_surface_rect

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((600, 600))

mario = pygame.image.load("sprites/mario.png")
mario_rect = mario.get_rect(center = (300, 300))
angle = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    angle += 1
    screen.fill((255, 255, 255))
    mario_rotated, mario_rotated_rect = rotate(mario, angle)

    screen.blit(mario_rotated, mario_rotated_rect)
    pygame.display.flip()
    clock.tick(60)