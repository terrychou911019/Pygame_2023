import pygame, sys, pymunk

def create_apple(space, pos):
    body = pymunk.Body(1, 100, body_type = pymunk.Body.DYNAMIC) # mass, inertia, bodt_type
    body.position = pos
    shape = pymunk.Circle(body, 50) # body, radius
    space.add(body, shape)
    return shape

def draw_apples(apples):
    for apple in apples:
        pos_x = int(apple.body.position.x)
        pos_y = int(apple.body.position.y)
        pygame.draw.circle(screen, (255, 0, 0), (pos_x, pos_y), 50)

def static_ball(space, pos):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, 40)
    space.add(body, shape)
    return shape

def draw_static_ball(balls):
    for ball in balls:
        pos_x = int(ball.body.position.x)
        pos_y = int(ball.body.position.y)
        pygame.draw.circle(screen, (0, 0, 255), (pos_x, pos_y), 40)

# physics
space = pymunk.Space()
space.gravity = (0, 500)
apples = []
balls = []
balls.append(static_ball(space, (400, 300)))
balls.append(static_ball(space, (200, 400)))

pygame.init()
clock = pygame.time.Clock()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            apples.append(create_apple(space, event.pos))

    screen.fill((200, 200, 200))
    draw_apples(apples)
    draw_static_ball(balls)
    space.step(1 / 50) # update physics
    pygame.display.flip()
    clock.tick(60)