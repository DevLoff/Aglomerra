import pygame

pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
SCREEN_RECT = SCREEN.get_rect()
ML_run = True
CLOCK = pygame.time.Clock()
SPEED = 10
FONT = pygame.font.Font("ARIAL.TTF",20)

tiling = pygame.Surface(SCREEN.get_size())

tile_blue = pygame.image.load("images/default_blue.png")
tile_sky = pygame.image.load("images/default_sky.png")

w,h = 100, 25
for y in range(6*4):
    for x in range(8):
        if y%2 == 0:
            tiling.blit(tile_blue, (x * w, y * h))
        else:
            tiling.blit(tile_sky, (x * w + 50, y * h))
SCREEN.blit(tiling, (0,0))

class Player:
    def __init__(self):
        self.image = pygame.Surface((50,50))
        self.image.fill((0,50,255))
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(0,0)
        self.speed = 10

    def move(self,inputs,clamp):
        axis = pygame.Vector2(inputs[pygame.K_RIGHT]-inputs[pygame.K_LEFT],inputs[pygame.K_DOWN]-inputs[pygame.K_UP])
        if axis.length() > 0:
            axis = axis.normalize()
        self.pos += axis * self.speed
        self.pos.x = self.pos.x % clamp.get_width()
        self.pos.y = self.pos.y % clamp.get_height()

player = Player()

while ML_run:
    CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ML_run = False

    player.move(pygame.key.get_pressed(),SCREEN)

    position = FONT.render(f"{player.pos.x}:{player.pos.y}", True, (255,0,255))

    SCREEN.blit(player.image, player.pos)
    SCREEN.blit(position,(0,0))
    pygame.display.flip()
    SCREEN.blit(tiling.subsurface(player.rect.move(player.pos).clip(SCREEN_RECT)), player.pos)
    SCREEN.blit(tiling.subsurface(position.get_rect()), (0,0))

pygame.quit()