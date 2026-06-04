import pygame
from modules.input import InputHandler

def get_axis(x_po:int,x_ne:int,y_po:int,y_ne:int):
    axis = pygame.Vector2(x_po - x_ne, y_po - y_ne)
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
        self.speed = 10
        self.action = None
        self.justTP = True

    def move(self,inputs:InputHandler) -> None:
        if self.action is None:
            axis = get_axis(inputs.lookup(pygame.K_RIGHT),inputs.lookup(pygame.K_LEFT),inputs.lookup(pygame.K_DOWN),inputs.lookup(pygame.K_UP)).rotate(-45) * self.speed
            self.action = ["walk",1,axis]

    def dash(self,inputs:InputHandler) -> None:
        if self.action is None:
            axis = get_axis(inputs.lookup(pygame.K_RIGHT), inputs.lookup(pygame.K_LEFT), inputs.lookup(pygame.K_DOWN),
                            inputs.lookup(pygame.K_UP)).rotate(-45) * 50
            self.action = ["dash",3,axis]

    def update(self,borders:list[pygame.Rect]) -> None:
        if self.action is not None:
            step = self.action[2]
            if inside(borders, self.rect.move(step)):
                self.rect.move_ip(step)
            self.action[1] -= 1
            if self.action[1] < 1:
                self.action = None