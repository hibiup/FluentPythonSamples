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
