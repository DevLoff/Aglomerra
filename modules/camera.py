import pygame
type Position = pygame.Vector2|tuple[int|float,int|float]

def safe_subfill(canva:pygame.Surface,target:pygame.Rect) -> pygame.Surface:
    body = canva.get_rect()
    safe_target = target.clip(body)
    if body.contains(safe_target):
        return canva.subsurface(safe_target)
    return pygame.Surface((0,0))

class Camera:
    def __init__(self, n:int = 1) -> None:
        size = pygame.display.get_surface().get_size()
        self.layers = [pygame.Surface(size)] + [pygame.Surface(size, pygame.SRCALPHA) for _ in range(n-1)]
        self.rect = pygame.Rect((0, 0), size)

    def goto(self, x:int|float, y:int|float) -> None:
        self.rect.move_ip(x - self.rect.center[0], y - self.rect.center[1])

    def paint(self, surface:pygame.Surface, pos:Position, layer:int = 0) -> None:
        self.layers[layer].blit(surface, pygame.Vector2(pos) - pygame.Vector2(self.rect.topleft))

    def capture(self, surface:pygame.Surface, layer:int = 0) -> None:
        to_be_blited = safe_subfill(surface,self.rect)
        self.layers[layer].blit(to_be_blited, (0,0))

    def clear(self, layer:int = 0) -> None:
        self.layers[layer].fill((0,0,0,0))

    def clear_all(self) -> None:
        for i in range(len(self.layers)):
            self.clear(i)

    def draw(self, surface:pygame.Surface, pos:Position) -> None:
        for layer in self.layers:
            surface.blit(layer,pos)