import pygame, sys, random

class GameState():
    def __init__(self):
        self.state = "game_init"
        self.game_init_image = pygame.image.load("assets/message.png").convert_alpha()
        self.game_over_image = pygame.image.load("assets/gameover.png").convert_alpha()

    def state_manager(self):
        if self.state == "game_init":
            self.game_init()
        if self.state == "game":
            self.game()
        if self.state == "game_over":
            self.game_over()

    def game_init(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:     
                    pipe_group.empty()
                    bird.y_pos = 216
                    bird.y_movement = 0
                    pygame.time.set_timer(CREATE_PIPE, 1200)
                    global score
                    score = 0
                    self.state = "game"
                if event.key == pygame.K_TAB:
                    global DEBUG
                    DEBUG = not DEBUG
        
        screen.blit(bg_surface, (0, 0))
        floor_group.draw(screen)
        floor_group.update()
        screen.blit(self.game_init_image, (52, 122))
        score_display(self.state)
        pygame.display.update()
            
    def game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.y_movement = -5
                    bird.flap_sound.play()
                if event.key == pygame.K_TAB:
                    global DEBUG
                    DEBUG = not DEBUG
            if event.type == CREATE_PIPE:
                pipe_pos_y = random.choice(pipe_height)
                pipe_group.add(Pipe(True, pipe_pos_y))
                pipe_group.add(Pipe(False, pipe_pos_y - 150))
            if event.type == BIRD_FLAP:
                bird.current_sprite += 1
                if bird.current_sprite >= len(bird.sprites):
                    bird.current_sprite = 0

        screen.blit(bg_surface, (0, 0))
        pipe_group.draw(screen)
        pipe_group.update()
        floor_group.draw(screen)
        floor_group.update()
        bird_group.draw(screen)
        bird_group.update(gravity)
        #global score
        #score += 0.01
        score_display(self.state)
        pygame.display.update()

    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.time.set_timer(CREATE_PIPE, 0) # remove the timer
                    pipe_group.empty()
                    bird.y_pos = 216
                    bird.y_movement = 0
                    global score
                    score = 0
                    self.state = "game_init"
                if event.key == pygame.K_TAB:
                    global DEBUG
                    DEBUG = not DEBUG
        
        screen.blit(bg_surface, (0, 0))
        floor_group.draw(screen)
        floor_group.update()
        screen.blit(self.game_over_image, (48, 235))
        score_display(self.state)
        pygame.display.update()

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
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
        self.sprites.append(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
        self.sprites.append(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
        self.current_sprite = 0
        self.regular_image = self.sprites[self.current_sprite]
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center = (50, self.y_pos))
        self.y_movement = 0
        self.flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
        self.death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
        self.score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
    
    def update(self, gravity):
        if self.rect.centery <= -50 or self.rect.centery >= 450:
            if not DEBUG:
                game_state.state = "game_over"
                self.death_sound.play()
                self.y_pos = 216
        for pipe in pipe_group:
            if self.rect.colliderect(pipe.rect):
                if not DEBUG:
                    game_state.state = "game_over"
                    self.death_sound.play()
        self.regular_image = self.sprites[int(self.current_sprite)]
        self.y_movement += gravity
        self.y_pos += self.y_movement
        #self.rect = self.image.get_rect(center = (50, self.y_pos))
        self.image, self.rect = self.rotate(self.regular_image)

    def rotate(self, bird):
        rotated_bird = pygame.transform.rotozoom(bird, -self.y_movement * 5, 1)
        rotated_bird_rect = rotated_bird.get_rect(center = (50, self.y_pos))
        return rotated_bird, rotated_bird_rect        

class Pipe(pygame.sprite.Sprite):
    def __init__(self, is_bottom, pipe_pos_y):
        super().__init__()
        self.pos_x = 320
        self.pos_y = pipe_pos_y
        self.scored = False
        self.is_bottom = is_bottom
        self.image = pygame.image.load("assets/pipe-green.png").convert()
        self.flip_image = pygame.transform.flip(self.image, False, True)
        if self.is_bottom:
            self.rect = self.image.get_rect(midtop = (self.pos_x, self.pos_y))
        else:
            self.image = self.flip_image
            self.rect = self.image.get_rect(midbottom = (self.pos_x, self.pos_y))

    def update(self):
        if not self.scored:
            if abs(bird.rect.centerx - self.pos_x) < 10:
                global score 
                score += 0.5 # we have 2 pipes on same pos_x
                bird.score_sound.play()
                self.scored = True
        self.pos_x -= 2.5
        if self.is_bottom:
            self.rect = self.image.get_rect(midtop = (self.pos_x, self.pos_y))
        else:
            self.image = self.flip_image
            self.rect = self.image.get_rect(midbottom = (self.pos_x, self.pos_y))
        if self.pos_x <= -100:
            self.kill()

def score_display(state):
    global high_score
    if state == "game_init":
        high_score_surface = game_font.render("High Score: " + str(int(high_score)), True, "white")
        high_score_rect = high_score_surface.get_rect(center = (144, 425))
        screen.blit(high_score_surface, high_score_rect)
    if state == "game":
        score_surface = game_font.render(str(int(score)), True, "white")
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)
    if state == "game_over":
        high_score = max(score, high_score)
        score_surface = game_font.render("Score: " + str(int(score)), True, "white")
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render("High Score: " + str(int(high_score)), True, "white")
        high_score_rect = high_score_surface.get_rect(center = (144, 425))
        screen.blit(high_score_surface, high_score_rect)  

# Basic Setup
pygame.init()
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game_font = pygame.font.Font("fonts/04B_19.ttf", 20)

# Gane Variables
game_state = GameState()
gravity = 0.125
pipe_height = [200, 300, 400]
CREATE_PIPE = pygame.USEREVENT + 0
BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_PIPE, 1200)
pygame.time.set_timer(BIRD_FLAP, 200)
DEBUG = False
score = 0
high_score = 0

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
    game_state.state_manager()
    clock.tick(120)