class Matrix2:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __mul__(self, other):
        if type(other) == Matrix2:
            return Matrix2(
                self.a * other.a + self.b * other.c,
                self.a * other.b + self.b * other.d,
                self.c * other.a + self.d * other.c,
                self.c * other.b + self.d * other.d,
            )
        elif type(other) == tuple[float, float] or type(other) == tuple[int, int]:
            return (
                self.a * other[0] + self.b * other[1],
                self.c * other[0] + self.d * other[1],
            )
        elif type(other) == float or type(other) == int:
            return Matrix2(
                self.a * other,
                self.b * other,
                self.c * other,
                self.d * other,
            )
        assert (0==1), "Matrix multiplication failed"

    def __add__(self, other):
        if type(other) == Matrix2:
            return Matrix2(
                self.a + other.a,
                self.b + other.b,
                self.c + other.c,
                self.d + other.d,
            )
        assert (0==1), "Matrix addition failed"

    def __sub__(self, other):
        if type(other) == Matrix2:
            return Matrix2(
                self.a - other.a,
                self.b - other.b,
                self.c - other.c,
                self.d - other.d,
            )
        assert (0==1), "Matrix substraction failed"