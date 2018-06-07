from unittest import TestCase

'''
只要 Python 函数的定义体中有 yield 关键字，该函数就是生成器函数。调用生成器函数时，会返回一个生成器对象。也就是说，生成器函数是生成器工厂。
'''
def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end.')


class TestGenerator(TestCase):
    def test_yeild(self):
        '''
        gen_AB() 方法返回一个带有 yeild 的结果，也就是一个生成器
        '''
        gen_ab = gen_AB()    # gen_ab 是一个 generator
        for c in gen_ab:
            print('-->', c)
