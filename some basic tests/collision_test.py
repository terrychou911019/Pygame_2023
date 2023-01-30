import pygame, sys

def bouncing_rect():
    global x_speed, y_speed, another_speed

    # moving another_rect
    if another_rect.bottom >= screen_height or another_rect.top <= 0:
        another_speed *= -1
    another_rect.y += another_speed

    # collision with screen borders
    if moving_rect.right >= screen_width or moving_rect.left <= 0:
        x_speed *= -1
    if moving_rect.bottom >= screen_height or moving_rect.top <= 0:
        y_speed *= -1

    # collision with anoter_rect
    collision_tolerance = 10
    if moving_rect.colliderect(another_rect):
        if abs(another_rect.top - moving_rect.bottom) < collision_tolerance and y_speed > 0: 
            y_speed *= -1
        if abs(another_rect.bottom - moving_rect.top) < collision_tolerance and y_speed < 0:
            y_speed *= -1
        if abs(another_rect.right - moving_rect.left) < collision_tolerance and x_speed < 0:
            x_speed *= -1
        if abs(another_rect.left - moving_rect.right) < collision_tolerance and x_speed > 0:
            x_speed *= -1

    moving_rect.x += x_speed
    moving_rect.y += y_speed

    pygame.draw.rect(screen, (255, 255, 255), moving_rect)
    pygame.draw.rect(screen, (255, 0, 0), another_rect)

pygame.init()
clock = pygame.time.Clock()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

moving_rect = pygame.Rect(250, 250, 60, 60)
x_speed, y_speed = 4, 3
another_rect = pygame.Rect(200, 300, 180, 100)
another_speed = 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    bouncing_rect()

    pygame.display.flip()
    clock.tick(60)