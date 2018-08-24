from abc import ABCMeta
from unittest import TestCase
from types import MethodType


class Bird(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Bird:
            if any("__has_wing__" in B.__dict__ for B in C.__mro__):   # C 是提请判断的对象在 isinstance 请求中是实例
                return True
        return NotImplemented
    pass


class Duck:
    """ 鸭类原形 """
    __has_wing__ = True   # Bird 将借助这个标志来判断 Duck/duck 是否是它的子类
    speed = 1
    sound = "What's a duck say! quack! quack!!"
    movement = "A duck must can ~~~ swimming ~~~ at speed"


def say(self):
    print("My id is:", id(self))
    print(self.sound)


def move(self):
    print("My id is:", id(self))
    print(self.movement, self.speed)


def refill(self):
    print("My id is:", id(self))
    self.speed += 1
    print("Speed gauge increasing to:", self.speed)


def fly(self):
    print("My id is:", id(self))
    print("I'm learning how to fly")


class TestDucktyping(TestCase):
    def test_duck_typing(self):

        # 类型组装
        Duck.speak = say
        Duck.move = move
        Duck.eat = refill

        # 判定一下类型:
        assert(issubclass(Duck, Bird) is True)  # issubclass() 给 Bird.__subclasshook__(cls, C) 方法传递的 C 是 Duck

        # 新建一个实例
        duck = Duck()
        assert(isinstance(duck, Bird) is True)  # issubclass() 给 Bird.__subclasshook__(cls, C) 方法传递的 C 是 duck

        # 走起！
        print("A duck's id is:", id(duck))
        duck.speak()
        duck.move()
        duck.eat()  # 修改数据，增加速度
        duck.move()
        duck.eat()
        duck.move()

        # 实例组装
        duck.fly = MethodType(fly, duck)
        duck.fly()
