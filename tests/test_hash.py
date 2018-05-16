class Vector2d:
    __slots__ = ('__x', '__y')

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __eq__(self, other):
        return hash(self)==hash(other)

    def __repr__(self):
        return 'Vector({},{})'.format(self.__x, self.__y)

from unittest import TestCase
class TestHash(TestCase):
    def test_hash(self):
        v1 = Vector2d(1, 2)
        print(v1)
        print("hash(v1)="  + str(hash(v1)))

        v2 = Vector2d(2, 1)
        print("hash(v2)="  + str(hash(v2)))

        assert(v2 == v1)       # compare eq() -> hash()
        assert(v2 is not v1)   # compare id()
