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

    def det(self):
        return self.a * self.d - self.b * self.c

    def inv(self):
        coef = self.det()
        assert coef != 0, "Cannot invert matrix"
        return Matrix2(
            self.d / coef,
            - self.b / coef,
            - self.c / coef,
            self.a / coef,
        )