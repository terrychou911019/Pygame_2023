import pygame, sys, random

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path, sound_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound(sound_path)
        self.kill_target = pygame.mixer.Sound("sound_effect/bone-crack-1.wav")

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self):
        self.gunshot.play()
        if pygame.sprite.spritecollide(crosshair, target_group, True) != []:
            self.kill_target.play()

class Target(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

# General setup
pygame.init()
clock = pygame.time.Clock()

# Game screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("sprites/bg_wood.png")
pygame.mouse.set_visible(False)

# Crosshair
crosshair = Crosshair("sprites/crosshair_outline_small.png", "sound_effect/gun-gunshot-02.wav")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# Target
target_group = pygame.sprite.Group()
for target in range(20):
    new_target = Target("sprites/duck_target_yellow.png", random.randrange(0, screen_width), random.randrange(0, screen_height))
    target_group.add(new_target)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()

    
    screen.blit(background, (0, 0))
    target_group.draw(screen)
    crosshair_group.draw(screen)
    crosshair_group.update()
    pygame.display.flip()
    clock.tick(60)