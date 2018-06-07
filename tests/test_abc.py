from abc import ABC, abstractmethod
from collections import namedtuple


Customer = namedtuple('Customer', 'name fidelity')

class Promotion(ABC) :     # 抽象基类
    @abstractmethod
    def discount(self, order):
        """返回折扣金额"""

class FidelityPromo(Promotion):
    """为积分为1000或以上的顾客提供5%折扣"""
    def discount(self, order):
        return order.spend * .05 if order.customer.fidelity >= 1000 else 1

class Cart:
    def __init__(self, customer, spend, promotion=None):
        self.customer = customer
        self.promotion = promotion
        self.spend = spend

    def due(self):
        if self.promotion is None:
            return self.spend
        else:
            return self.promotion.discount(self)

    def __call__(self):
        return self.due()


from unittest import TestCase
class AbstractClassTest(TestCase):
    def test_abc(self):
        ann = Customer('Ann Smith', 1100)
        cart = Cart(ann, spend = 123, promotion = FidelityPromo())
        print('<Order due: {:.2f}>'.format(cart()))

    def test_duck_class(self):
        '''
        duck class 指的是不关注类的基类，转而关注类支持的方法（特征）来判断它属于哪个基类
        '''

        # 定义一个任意类
        class Struggle:
            pass

        # 动态为它加上 __len__ 方法
        def __len(self):
            return 23
        Struggle.__len__= __len

        # 即可让 python 将它识别成 collections.abc.Sized 的子类
        from collections.abc import Sized
        assert(True == isinstance(Struggle(), Sized))

    def test_abc_register(self):
        '''
        也可以通过 register 方法来动态将一个类声明为某个类的子类
        '''

        # 注册一个基类
        from abc import ABCMeta
        import six
        @six.add_metaclass(ABCMeta)
        class Parent:
            pass

        # 定义一个任意类
        class DynSubClass:
            pass

        # 将 DynSubClass 类动态注册为 Parent 的子类
        Parent.register(DynSubClass)
        assert(True == isinstance(DynSubClass(), Parent))
