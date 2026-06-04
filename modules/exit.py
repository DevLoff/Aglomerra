import pygame

from modules.player import Player

class Gate:
    def __init__(self, target:str, hitbox:tuple[int,int,int,int], pinpoint:tuple[int,int]) -> None:
        self.level:str = target
        self.hitbox:pygame.Rect = pygame.Rect(hitbox)
        self.pinpoint:pygame.Vector2 = pygame.Vector2(pinpoint)

    def exit(self, char:Player) -> bool:
        if char.rect.colliderect(self.hitbox):
            return True
        return False