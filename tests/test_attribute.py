from unittest import TestCase

'''
访问属性( 如 f.x )的时候，Python 解释器会调用特殊的方法（如 __getattr__ 和 __setattr__）计算属性，”，当访问不存在的属性时
才返回属性的值。
'''
class Foo:
    y = 100
    def __init__(self, x):
        self.x = x

    def __getattr__(self, name):
        '''
        当 __getattribute__() 失效时调用，如果不存在则抛出 AttributeError
        '''
        print("__getattr__() is called")
        return name

    def __getattribute__(self, name):
        '''
        无论如何都会首先调用，即便存在 f.x，也会返回改函数的结果
        '''
        print("__getattribute__() is called")
        if name == 'bar':
            raise AttributeError   # f.bar 会抛出这个异常，但是因为存在 __getattr__()，因此 python 会重新尝试
        return 'getattribute'

class TestAttribute(TestCase):
    def test_Foo(self):
        f = Foo(10)
        print(f"f.x => {f.x}")        # 不会返回期待中的 10，因为被 __getattribute__ 截获
        print(f"f.y => {f.y}")        # 不会返回期待中的 100，因为被 __getattribute__ 截获
        print(f"f.baz => {f.baz}")    # 被 __getattribute__ 截获
        print(f"f.bar => {f.bar}")    # 被 __getattribute__ 截获, 抛出的异常再次被 __getattr__ 截获，最终返回 __getattr__ 的结果
        print(f.__dict__)             # 甚至 __dict__ 也会被 __getattribute__ 截获，返 __getattribute__ 的值
        print(Foo.__dict__)           # 直接访问类才可以得到所有方法，但是原始类没有 x (存在实例中)，只有 y
