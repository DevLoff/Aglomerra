import pygame
import json

from modules.matrix import Matrix2
from modules.exit import Gate
from modules.player import Player

TILESET = {
    "blue" : pygame.image.load("images/default_blue.png"),
    "sky" : pygame.image.load("images/default_sky.png"),
    "default" : pygame.image.load("images/default_tile.png")
}

def rect_goto(rect,pos):
    rect.move_ip(pos.x-rect.center[0],pos.y-rect.center[1])

class Level:
    def __init__(self, filepath:str, basis:Matrix2) -> None:
        level_script = json.load(open(filepath))
        self.basis = basis
        self.surface = pygame.Surface(level_script["size"])
        self.center = pygame.Vector2(self.surface.get_rect().center)
        self.area, self.gates = [], []
        for gate in level_script["gates"]:
            self.gates.append(Gate(gate["level"], gate["coord"], gate["target"]))
        self.landscape = [b for b in sorted(level_script["blocks"], key=lambda b: basis.mult(pygame.Vector2(b["pos"][:2])).y)]
        for block in self.landscape:
            self.area.append(pygame.Rect(block["pos"][:2], (100, 100)))
            self.surface.blit(TILESET[block["tag"]], basis.mult(pygame.Vector2(block["pos"][:2])) + self.center)

    def hit_tp(self, char:Player) -> Gate|None:
        for gate in self.gates:
            if gate.exit(char):
                return gate
        return None

    def switch(self, char:Player):
        pinpoint = self.hit_tp(char)
        if pinpoint is None:
            char.justTP = False
            return self
        if char.justTP:
            return self
        char.justTP = True
        rect_goto(char.rect,pinpoint.pinpoint)
        return Level(pinpoint.level,self.basis)

    def save(self,filepath:str) -> None:
        json.dump(
            {
                "size": self.surface.get_size(),
                "blocks":self.landscape,
                "gates":[gate.save() for gate in self.gates]
            },
            open(filepath,'w')
        )