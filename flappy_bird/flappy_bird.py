import pygame, sys, random

class Floor(pygame.sprite.Sprite):
    def __init__(self, init_x_pos):
        super().__init__()
        self.x_pos = init_x_pos
        self.x_starting_pt = init_x_pos
        self.image = pygame.image.load("assets/base.png").convert()
        self.rect = self.image.get_rect(topleft = (self.x_pos, 450))
    
    def update(self):
        self.x_pos -= 0.5
        self.rect = self.image.get_rect(topleft = (self.x_pos, 450))
        if self.x_starting_pt - self.x_pos >= screen_width:
            self.x_pos = self.x_starting_pt

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.y_pos = 216
        self.image = pygame.image.load("assets/bluebird-midflap.png").convert()
        self.rect = self.image.get_rect(center = (50, self.y_pos))
        self.y_movement = 0
    
    def update(self, gravity):
        self.y_movement += gravity
        self.y_pos += self.y_movement
        self.rect = self.image.get_rect(center = (50, self.y_pos))

class Pipe(pygame.sprite.Sprite):
    def __init__(self, is_bottom, pipe_pos_y):
        super().__init__()
        self.pos_x = 320
        self.pos_y = pipe_pos_y
        self.is_bottom = is_bottom
        self.image = pygame.image.load("assets/pipe-green.png").convert()
        self.flip_image = pygame.transform.flip(self.image, False, True)
        if self.is_bottom:
            self.rect = self.image.get_rect(midtop = (self.pos_x, self.pos_y))
        else:
            self.image = self.flip_image
            self.rect = self.image.get_rect(midbottom = (self.pos_x, self.pos_y))

    def update(self):
        self.pos_x -= 2.5
        if self.is_bottom:
            self.rect = self.image.get_rect(midtop = (self.pos_x, self.pos_y))
        else:
            self.image = self.flip_image
            self.rect = self.image.get_rect(midbottom = (self.pos_x, self.pos_y))
        

# Basic Setup
pygame.init()
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Gane Variables
gravity = 0.125
CREATE_PIPE = pygame.USEREVENT
pygame.time.set_timer(CREATE_PIPE, 1200)
pipe_height = [200, 300, 400]

# Background
bg_surface = pygame.image.load("assets/background-day.png").convert() # convert(): to make the image work with pygame more easily

# Floor
floor_head = Floor(0)
floor_rear = Floor(screen_width)
floor_group = pygame.sprite.Group()
floor_group.add(floor_head)
floor_group.add(floor_rear)

# Bird
bird = Bird()
bird_group = pygame.sprite.Group()
bird_group.add(bird)

# Pipe
pipe_group = pygame.sprite.Group()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.y_movement = -6
        if event.type == CREATE_PIPE:
            pipe_pos_y = random.choice(pipe_height)
            pipe_group.add(Pipe(True, pipe_pos_y))
            pipe_group.add(Pipe(False, pipe_pos_y - 150))

    screen.blit(bg_surface, (0, 0))

    pipe_group.draw(screen)
    pipe_group.update()

    floor_group.draw(screen)
    floor_group.update()

    bird_group.draw(screen)
    bird_group.update(gravity)

    

    pygame.display.update()
    clock.tick(120)