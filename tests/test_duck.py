from abc import ABCMeta
from unittest import TestCase
from types import MethodType


class Duck:
    """ 鸭类原形 """
    __has_wing__ = True   # Bird 将借助这个标志来判断 Duck/duck 是否是它的子类
    speed = 1
    sound = "What's a duck say! quack! quack!!"
    movement = "A duck must can ~~~ swimming ~~~ at speed"


def twit(self):
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


class TestDuckTyping(TestCase):
    @classmethod
    def do_duck(cls, super_class):
        # 类型组装
        Duck.twit = twit
        Duck.move = move
        Duck.eat = refill

        # 判定一下类型:
        assert(issubclass(Duck, super_class) is True)  # issubclass() 给 Bird.__subclasshook__(cls, C) 方法传递的 C 是 Duck

        # 新建一个实例
        duck = Duck()
        assert(isinstance(duck, super_class) is True)  # issubclass() 给 Bird.__subclasshook__(cls, C) 方法传递的 C 是 duck

        # 走起！
        print("A duck's id is:", id(duck))
        duck.twit()
        duck.move()
        duck.eat()  # 修改数据，增加速度
        duck.move()
        duck.eat()
        duck.move()

        # 实例组装
        duck.fly = MethodType(fly, duck)
        duck.fly()

        return duck

    def test_duck_typing_with_ABC(self):
        """
        借助 ABCMeta 的 __subclasshook__，我们可以接获"子类"的 issubclass() 和 isinstance() 方法。
        """
        # 定义父类
        class Bird(metaclass=ABCMeta):
            @classmethod
            def __subclasshook__(cls, C):
                if cls is Bird:
                    if any("__has_wing__" in B.__dict__ for B in C.__mro__):   # C 是提请判断的对象在 isinstance 请求中是实例
                        return True
                return NotImplemented
            pass

        # 测试
        TestDuckTyping.do_duck(Bird)

    def test_duck_typing_with_ABC_register(self):
        """
        更简单的办法是直接使用 ABCMeta 的 register() 方法注册子类
        """
        # 定义父类
        class Bird(metaclass=ABCMeta):
            from abc import abstractmethod
            greeting = "Hello, World!s"
            @abstractmethod
            def speak(self):
                print("My id is:", id(self))
                print(self.greeting)

        # 注册子类
        Bird.register(Duck)

        # 测试
        duck = TestDuckTyping.do_duck(Bird)

        # register 不会让子类出现在 MRO (Method Resolution Order)中，故而也不能通过 super() 来调用父类的方法。
        # 而且即便子类没有实现抽象方法，实例化也不会报错，只有在调用时候才会报错。
        parent = super(Duck, duck).__init__()
        assert(parent is None)
        if parent is not None:
            parent.speak()   # 不会被执行到
            duck.speak()     # 子类也不存在该方法

    def test_duck_typing_with_metaclass(self):
        """
        __subclasscheck__() 和 __instancecheck__() 也可以起到相同的效果，但是它们只能定义在"父类"的 MetaClass 中
        这总方法不常见
        """
        # 定义父类的 MetaClasss
        class BirdMetaClass(type):
            @classmethod
            def __subclasscheck__(cls, C):
                if cls is Bird:
                    if any("__has_wing__" in B.__dict__ for B in C.__mro__):   # C 是提请判断的对象在 isinstance 请求中是实例
                        return True
                return NotImplemented

            @classmethod
            def __instancecheck__(cls, C):
                if cls is Bird:
                    if any("__has_wing__" in B.__dict__ for B in C.__mro__):   # C 是提请判断的对象在 isinstance 请求中是实例
                        return True
                return NotImplemented

        # 定义父类
        class Bird(metaclass=BirdMetaClass):
            pass

        # 测试
        TestDuckTyping.do_duck(Bird)
