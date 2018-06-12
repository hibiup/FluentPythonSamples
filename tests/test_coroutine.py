from unittest import TestCase
from inspect import getgeneratorstate

class TestCoroutine(TestCase):
    def simple_coroutine(self, a):
        print('-> Started: a =', a)
        b = yield a
        print('-> Received: b =', b)
        c = yield a + b
        print('-> Received: c =', c)
    
    def test_simple_coroutine(self):
        '''
        新建两个协程
        '''
        coroutines = [self.simple_coroutine(i) for i in range(2)]

        '''
        Primer
        '''
        for coro in coroutines:
            ret = 0
            print(getgeneratorstate(coro))

            ret = next(coro)      # Start coroutine and run to the first yield
            print(getgeneratorstate(coro))
            print("Return " + str(ret))

        '''
        模拟并发。修改一下即可实现事件驱动，例如通过循环检查 coroutine primer 的时候的返回值，来决定何时进一步激活哪个 coroutine。
        参考 test_texi.py 的例子
        '''
        for coro in coroutines:
            ret = 0
            try:
                ret = coro.send(28)   # return a + b
                print("Return " + str(ret))

                coro.send(99)         # Will have StopIteration exception because coroutine has been finished.
            except StopIteration:
                pass
            finally:
                print(getgeneratorstate(coro))


class TestException(TestCase):
    class DemoException(Exception):
        pass
    
    def __except_handling(self):
        print('-> coroutine started')
        while True:
            try:
                x = yield
                if x == 0:
                    return x
            except self.DemoException:
                print('*** DemoException handled. Continuing...')
            else:
                print('-> coroutine received: {!r}'.format(x))

    def test_except_handling(self):
        exc_coro = self.__except_handling()
        next(exc_coro)

        exc_coro.send(11)
        exc_coro.send(22)

        exc_coro.throw(self.DemoException)

        #exc_coro.close()
        print(getgeneratorstate(exc_coro))

        try:
            '''
            Coroutine 的返回值会被包含在 StopIteration 异常中返回给调用方。
            '''
            x = exc_coro.send(0)
        except StopIteration as stop_exc:
            print(stop_exc.value)
        print(getgeneratorstate(exc_coro))
