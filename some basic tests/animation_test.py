import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.is_animating = False
        self.sprites = []
        for i in range(1, 11):
            self.sprites.append(pygame.image.load(f"sprites/attack_{i}.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def animate(self):
        self.is_animating = True

    def update(self, speed):
        if self.is_animating:
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]

# General set
pygame.init()
clock = pygame.time.Clock()

# Game screen
scree_width = 128
scree_height = 64
screen = pygame.display.set_mode((scree_width, scree_height))
pygame.display.set_caption("Sprite Aimation")

# Creating the sprites and the groups
moving_sprites = pygame.sprite.Group()
player = Player(0, 0)
moving_sprites.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            player.animate()

    screen.fill((255, 255, 255))
    moving_sprites.draw(screen)
    moving_sprites.update(0.25)
    pygame.display.flip()
    clock.tick(60)
