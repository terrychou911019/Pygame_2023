import pygame, sys

pygame.init()
clock = pygame.time.Clock()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

base_font = pygame.font.Font(None, 32)
user_text = ""

input_rect = pygame.Rect(200, 200, 200, 32)
input_rect_color_active = pygame.Color("lightskyblue3")
input_rect_color_passive = pygame.Color("gray15")
active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    screen.fill((0, 0, 0))
    
    if active:
        color = input_rect_color_active
    else:
        color = input_rect_color_passive
    pygame.draw.rect(screen, color, input_rect, 2)

    text_surface = base_font.render(user_text, True, (255, 255, 255))
    input_rect.w = max(200, text_surface.get_width() + 10)
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    pygame.display.flip()
    clock.tick(60)