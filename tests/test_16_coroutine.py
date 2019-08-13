from unittest import TestCase
from inspect import getgeneratorstate


def generator_semu(start, end):
    for x in range(start, end):
        yield x


class TestCoroutine(TestCase):
    def test_generator_semu(self):
        semu = generator_semu(1, 4)
        assert(next(semu) == 1)
        assert(next(semu) == 2)
        assert(next(semu) == 3)
        try:
            next(semu)
        except StopIteration:
            pass

    def simple_coroutine(self, a):
        print('-> Started: a =', a)
        b = yield a
        print('-> Received: b =', b)
        c = yield a + b
        print('-> Received: c =', c)
    
    def test_simple_coroutine(self):
        """
        新建两个协程
        """
        coroutines = [self.simple_coroutine(i) for i in range(2)]

        """
        察看协程的状态
        """
        for coro in coroutines:
            ret = 0
            # 返回 generator 的状态。
            print(getgeneratorstate(coro))

            ret = next(coro)      # SPrimer(预激). tart coroutine and run to the first yield
            print(getgeneratorstate(coro))
            print("Return " + str(ret))

        """
        模拟并发。修改一下即可实现事件驱动，例如通过循环检查 coroutine primer 的时候的返回值，来决定何时进一步激活哪个 coroutine。
        参考 test_texi.py 的例子
        """
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
    """
    用携程作为异常处理器的应用：

    我们可以将异常交给一个携程来处理
    """

    class DemoException(Exception):
        """
        定义一个即将由主程序抛出的异常
        """
        pass
    
    def __except_handling(self):
        """
        定义一个异常处理器（协程）
        :return:
        """
        print('-> coroutine started')
        while True:
            try:
                # yield 不仅可以接收正常输入（用send传入），还可以接收用 throw 传入的异常
                x = yield
                if x == 0:
                    return x
            # 如果 yield 接收到异常，则处理会被转到这里：
            except self.DemoException:
                print('*** DemoException handled. Continuing...')
            else:
                print('-> coroutine received: {!r}'.format(x))

    def test_except_handling(self):
        exc_coro = self.__except_handling()
        next(exc_coro)

        # 发送正常数据
        exc_coro.send(11)
        exc_coro.send(22)

        # 发送一个异常
        exc_coro.throw(self.DemoException)

        # 关闭协程
        exc_coro.close()
        print(getgeneratorstate(exc_coro))  # GEN_CLOSED

        try:
            """
            Coroutine 的返回值会被包含在 StopIteration 异常中返回给调用方。
            """
            x = exc_coro.send(0)
        except StopIteration as stop_exc:
            print(stop_exc.value)
        print(getgeneratorstate(exc_coro))


class TestReturnValue(TestCase):
    """
    测试从 coroutine 中获得返回值
    """
    from collections import namedtuple
    Result = namedtuple('Result', 'count average')

    def averager(self):
        total = 0.0
        count = 0
        average = None
        while True:
            term = yield
            if term is None:  # 循环直到输入 None
                break
            total += term
            count += 1
            average = total/count
        # 返回返回值
        return self.Result(count, average)

    def test_averager(self):
        coro_avg = self.averager()
        next(coro_avg)
        coro_avg.send(10)
        coro_avg.send(30)
        coro_avg.send(6.5)

        try:
            coro_avg.send(None)      # 捕获StopIteration
        except StopIteration as exc: # 得到返回值
            result = exc.value

        print(result)
