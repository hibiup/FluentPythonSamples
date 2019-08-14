from unittest import TestCase

"""
只要 Python 函数的定义体中有 yield 关键字，该函数就是生成器函数。调用生成器函数时，会返回一个生成器对象。也就是说，生成器函数是生成器工厂。
"""


class TestGenerator(TestCase):
    # Test 1
    def gen_AB(self):
        print('start')
        yield 'A'
        print('continue')
        yield 'B'
        print('end.')

    def test_yeild(self):
        """
        gen_AB() 方法返回一个带有 yeild 的结果，也就是一个生成器
        """
        gen_ab = self.gen_AB()    # gen_ab 是一个 generator
        for c in gen_ab:
            print('-->', c)

    # Test 2
    def target(self):
        print("Start")
        a = 1

        # 不等于 b = a+a；这里实际上是两条语义：
        #   １）返回 a+a 的值．
        #   ２）获取 send(n) 输入并赋值给 b.
        # 协程会停留在 yield 上，也就意味着这条语句会分两个阶段执行．
        b = yield a+a

        print("b =", b)
        return b+b

    def test_target(self):
        t1 = self.target()
        res1 = next(t1)
        print(res1)   # 第一阶段；返回 a+a 的值 2

        try:
            t1.send(3)   # 第二阶段：为 b 赋值 3
        except StopIteration as res2:
            print(res2.value)  # 得到 return 值 6

    # Test 3
    def parent_generator(self, results):  # 委派生成器
        def sub_generator():              # 子生成器
            print("sub generator")
            while True:
                # 子生成器在委派器 yield from 后接管了和客户端的对接，因此 yield 将直接获得来自客户端的 send 参数。
                a = yield
                if a is None:  # 子生成器需要一个标志来结束循环
                    break
                # 循环结束后将值通过 StopIteration 异常返回。
                return a+a

        print("parent generator")
        while True:
            """
            yield from 将任务委派给子生成器，子生成器将直接对接客户端，委派生成器暂时挂起直到委派生成器返回 StopIteration。
            委派生成器如果得到来自子生成器的 StopIteration，从中析出返回值返回给调用者，并结束自身。客户端不需要 catch StopIteration
            但是如果是其他异常则会被抛给调用者。
            """
            result = yield from sub_generator()  # 这个循环每次迭代时会新建一个 sub_generator 实例
            if result is not None:
                results.append(result)
        # 下面的 print 不会被执行到。委派生成器会因为得到来自子生成器的 StopIteration 而提前结束。
        print("end")

    def test_yield_from(self):
        results = []
        parent = self.parent_generator(results)
        next(parent)  # 启动委派生成器，运行到 yield from，然后委派生成器将迭代启动子生成器，运行到子生成器的 yield 处等待用户输入。

        for value in range(3):
            parent.send(value)

        parent.send(None)  # 给子生成器发送结束循环信号。
        print(results)
