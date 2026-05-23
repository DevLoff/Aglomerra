import pygame

pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
SCREEN_RECT = SCREEN.get_rect()
ML_run = True
CLOCK = pygame.time.Clock()
SPEED = 10
FONT = pygame.font.Font("ARIAL.TTF",20)

tiling = pygame.Surface((10000,10000))

tile_blue = pygame.image.load("images/default_blue.png")
tile_sky = pygame.image.load("images/default_sky.png")

def safe_subfill(canva,target):
    body = canva.get_rect()
    safe_target = target.clip(body)
    if body.contains(safe_target):
        return canva.subsurface(safe_target)
    return pygame.Surface((0,0))

w,h = 100, 25
for y in range(6*4):
    z = (1-y)//2
    for x in range(z,8+z):
        if x%2 == y%2:
            tiling.blit(tile_blue, (x * w + 50 * y, y * h)) # + 50 * (y%2 == 1)
        else:
            tiling.blit(tile_sky, (x * w + 50 * y, y * h))

class Player:
    def __init__(self):
        self.image = pygame.Surface((50,50))
        self.image.fill((0,50,255))
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(0,0)
        self.speed = 10

    def move(self,inputs):
        axis = pygame.Vector2(inputs[pygame.K_RIGHT]-inputs[pygame.K_LEFT],inputs[pygame.K_DOWN]-inputs[pygame.K_UP])
        if axis.length() > 0:
            axis = axis.normalize()
        self.pos += axis * self.speed

player = Player()

class Camera:
    def __init__(self,n=1):
        size = pygame.display.get_surface().get_size()
        self.layers = [pygame.Surface(size)] + [pygame.Surface(size,pygame.SRCALPHA) for i in range(n-1)]
        self.rect = pygame.Rect((0,0),size)

    def goto(self,x,y):
        self.rect.move_ip(x-self.rect.center[0],y-self.rect.center[1])

    def paint(self,surface,pos,layer=0):
        self.layers[layer].blit(surface, pygame.Vector2(pos) - pygame.Vector2(self.rect.topleft))

    def capture(self,surface,layer=0):
        to_be_blited = safe_subfill(surface,self.rect)
        print(to_be_blited.get_size())
        self.layers[layer].blit(to_be_blited, (0,0))

    def clear(self,layer=0):
        self.layers[layer].fill((0,0,0,0))

    def clear_all(self):
        for i in range(len(self.layers)):
            self.clear(i)

    def draw(self,surface,pos):
        for layer in self.layers:
            surface.blit(layer,pos)

CAMERA = Camera(2)

while ML_run:
    CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ML_run = False

    player.move(pygame.key.get_pressed())
    CAMERA.goto(player.pos.x,player.pos.y)

    position = FONT.render(f"{player.pos.x}:{player.pos.y}", True, (255,0,255))

    CAMERA.paint(tiling,(0,0))
    CAMERA.paint(player.image,player.pos,1)
    CAMERA.draw(SCREEN,(0,0))

    SCREEN.blit(position,(0,0))

    pygame.display.flip()

    CAMERA.clear_all()

pygame.quit()