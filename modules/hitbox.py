import pygame

def dist(p1 : pygame.Vector2, p2 : pygame.Vector2) -> float:
    return (p1 - p2).length()

class Hitbox:
    def __init__(self,offset,radius) -> None:
        self.pos : pygame.Vector2 = pygame.Vector2(offset)
        self.radius : int = radius

    def collide(self, hitbox) -> bool:
        return dist(self.pos,hitbox.pos) < self.radius + hitbox.radius

    def tex(self) -> pygame.Surface:
        tex = pygame.Surface((2*self.radius, 2*self.radius),pygame.SRCALPHA)
        pygame.draw.circle(tex, (255,225,255,100), (self.radius, self.radius), 2*self.radius)
        return tex


class Frame:
    def __init__(self, change):
        self.diff : pygame.Vector2 = pygame.Vector2(change)
        self.hitbox : list[Hitbox] = []
        self.hurtbox: list[Hitbox] = []
        self.next = None

    def tex(self):
        comb = self.hitbox + self.hurtbox
        if len(comb) > 0:
            xes = [box.pos.x for box in comb]
            ys = [box.pos.y for box in comb]
            sizeOff = pygame.Vector2(max([box.radius for box in comb]))
            minVec = pygame.Vector2(min(xes),min(ys))
            maxVec = pygame.Vector2(max(xes),max(ys))
            posOff = sizeOff - minVec
            tex = pygame.Surface(maxVec+posOff+sizeOff,pygame.SRCALPHA)
            for box in self.hitbox:
                pygame.draw.circle(tex,(255,255,255,100),box.pos+posOff,box.radius)
            for box in self.hurtbox:
                pygame.draw.circle(tex,(255,0,0,100),box.pos+posOff,box.radius)
            return tex,posOff
        return None