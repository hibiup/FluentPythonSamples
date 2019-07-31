class A:
    def ping(self):
        print('ping:', self)


class B(A):
    def pong(self):
        print('pong from B:', self)


class C(A):
    def pong(self):
        print('PONG FROM C:', self)


class D(C, B):
    pass


from unittest import TestCase


class DiamondTest(TestCase):
    def test_diamond(self):
        '''
        对于多重继承，子类缺省采用从左到右的顺序来解决冲突。
        '''
        d = D()
        d.pong()

        '''
        子类也可以明确使用类名限定的方式来明确调用哪个父类
        '''
        D.pong = lambda self: B.pong(self)
        d.pong()
