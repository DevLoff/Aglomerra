import pygame

SCREEN = pygame.display.set_mode((800, 600))
ML_run = True
CLOCK = pygame.time.Clock()

class Player:
    def __init__(self):
        self.image = pygame.Surface((50,50))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(0,0)

player = Player()

while ML_run:
    CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ML_run = False
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        player.pos.x -= 1
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        player.pos.x += 1
    if pygame.key.get_pressed()[pygame.K_UP]:
        player.pos.y -= 1
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        player.pos.y += 1

    SCREEN.blit(player.image, player.pos)
    pygame.display.flip()
    pygame.draw.rect(SCREEN, (0,0,0), player.rect.move(player.pos))
pygame.quit()