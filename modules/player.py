import pygame

def get_axis(x_po:int,x_ne:int,y_po:int,y_ne:int):
    axis = pygame.Vector2(x_po - x_ne, y_po - y_ne)
    if axis.length() > 0:
        axis = axis.normalize()
    return axis

def get_axis_l(polars):
    axis = pygame.Vector2(polars[0] - polars[1], polars[2] - polars[3])
    if axis.length() > 0:
        axis = axis.normalize()
    return axis

def inside(collection:list[pygame.Rect],hitbox:pygame.Rect)->bool:
    cnt = 0
    for rect in collection:
        for point in [hitbox.topleft,hitbox.topright,hitbox.bottomleft,hitbox.bottomright]:
            if rect.collidepoint(point):
                cnt += 1
    if cnt == 4:
        return True
    return False

class Player:
    def __init__(self) -> None:
        self.image = pygame.Surface((50,50))
        self.image.fill((0,50,255))
        self.rect = pygame.Rect(0,0,50,50)
        self.facing = pygame.Vector2(1,0)
        self.action = None
        self.justTP = True

    def move(self,frame):
        if self.action is None:
            self.action = frame

    def update(self) -> None:
        if self.action is not None:
            self.rect.move_ip(self.action.diff)
            self.action = self.action.next