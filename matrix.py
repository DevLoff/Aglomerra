import pygame

class Matrix2:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def mult(self,vector):
        return pygame.Vector2(
            self.a * vector.x + self.b * vector.y,
            self.c * vector.x + self.d * vector.y,
        )