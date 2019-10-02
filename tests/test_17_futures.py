from unittest import TestCase
import threading
import time
import datetime
import random


def callback(results):
    print(f"Callback function received {results}")
    return results


class ConcurrentFuture(TestCase):
    @classmethod
    def do_something(cls, timeout):
        """
        模拟延迟并打印时间戳的函数
        """
        thread_id = threading.get_ident()
        print(f"[{datetime.datetime.utcnow()}] - [Thread - {thread_id}]: task will runs for {timeout+1} second(s).")
        time.sleep(timeout+1)
        print(f"[{datetime.datetime.utcnow()}] - [Thread - {thread_id}]: task is done")
        return thread_id, timeout

    @classmethod
    def do_something_with_callback(cls, timeout, callback):
        """
        模拟延迟并将结果返回给 callback 函数
        """
        return callback(cls.do_something(timeout))

    thread_number = 5

    def test_multiple_threading(self):
        from concurrent import futures

        with futures.ThreadPoolExecutor(self.thread_number) as executor:
            # 可以用 executor.map 代替 for comprehension.(参考 test_tasks.py 中的案例)
            res = [executor.submit(self.do_something, timeout) for timeout in random.sample(range(0, self.thread_number), self.thread_number)]
            print("All thread submitted.")

            # list 会导致阻塞等待返回．并非最好的获取结果的方式，参考下面 callback 的例子
            print(f"All threads {list(res)} are done!")

    def test_multiple_processing(self):
        """
        concurrent.futures 支持 Thread 和 Process
        """
        from concurrent import futures

        with futures.ProcessPoolExecutor(self.thread_number) as executor:
            res = [executor.submit(self.do_something, timeout) for timeout in random.sample(range(0, self.thread_number), self.thread_number)]
            print("All thread submitted.")
            print(f"All threads {list(res)} are done!")

    def test_multiple_threading_with_callback(self):
        """
        通过显示为函数指定 callback 来获取返回值
        """
        from concurrent import futures

        with futures.ThreadPoolExecutor(self.thread_number) as executor:
            # 传递一个　callback 函数给r任务
            res = [executor.submit(self.do_something_with_callback, timeout, callback) for timeout in random.sample(range(0, self.thread_number), self.thread_number)]
            print("All thread submitted.")

    def test_multiple_threading_as_complete(self):
        """
        也可以通过　futures.as_completed 函数来捕获返回值
        """
        from concurrent import futures

        with futures.ThreadPoolExecutor(self.thread_number) as executor:
            # 对于没有显示 callback 参数的函数，可以通过 as_completed 还获取返回值．（as_completed 也可以捕获异常）
            results = [executor.submit(self.do_something, timeout) for timeout in random.sample(range(0, self.thread_number), self.thread_number)]
            print("All thread submitted.")

            # 捕获返回值
            for f in futures.as_completed(results):
                print(callback(f.result()))

    def test_multiple_process_as_complete(self):
        """
        也可以通过　futures.as_completed 函数来捕获返回值
        """
        from concurrent import futures

        with futures.ProcessPoolExecutor(self.thread_number) as executor:
            """ 
            注意：在 Multiple Proces 中传递一个　callback 函数给r任务, 如果希望得到返回值，这个 callback 必须是独立函数。
            Multiple Thread 则没有这个问题，因为 Thread 之间共享调用栈。
            """
            f1 = executor.submit(self.do_something_with_callback, 1, callback)
            print("One job submitted.")
            futures.as_completed(f1)
            print("Job in multiple process pool returns", f1.result())

            """
            例如以下代码在 Multiple Process 中会出现错误：
               Error: Can't pickle local object ...
            """
            f2 = executor.submit(self.do_something_with_callback, 1, lambda out: "World")
            print("One job submitted.")
            futures.as_completed(f2)
            print("Job in multiple process pool returns", f2.result())


class AsyncIOFuture(TestCase):
    """
    asyncio 的 futures 用法略有不同，asyncio　通过＂协程＂来实现多任务．协程通过关键词 async 来定义．async 产生一个称为 Future 的数据
    结构来描述协程，然后将它交给 Event loop 等待协程调度器轮询，协程调度器通过 Task 结构来管理每一个 Future，最后的结果可以通过 await 取得．
    """
    @classmethod
    async def do_something(cls, timeout):
        import asyncio
        """
        模拟延迟并打印时间戳的函数. 注意 thread id 都是一样的，因为这是协程。
        """
        thread_id = threading.get_ident()
        print(f"[{datetime.datetime.utcnow()}] - [Thread - {thread_id}]: task will runs for {timeout+1} second(s).")

        # 协程内也该遵守非阻塞的原则使用支持 async 的函数。
        # asyncio.sleep 是一个 async 的 Future 函数，因此如果希望阻塞取值必须使用 await。(await 只能使用在 async 函数中去获取另一个 async 函数的结果)
        await asyncio.sleep(timeout+1)

        print(f"[{datetime.datetime.utcnow()}] - [Thread - {thread_id}]: task is done")
        return thread_id, timeout

    @classmethod
    def __callback(cls, future_task):
        print(f"Callback received {future_task.result()}")

    thread_number = 5

    def test_asyncio_run(self):
        """
        asyncio 有三种方法来执行一个 Future 函数:

        1) asyncio.run 函数会逐个阻塞。这种方式和使用 await 没有太大不同. 区别是 await 必须使用在 async 函数中，因此以下用法是非法的，除非也将 test_asyncio_function 加上 async 关键词
            [await self.do_something(timeout) for timeout in random.sample(range(0, self.thread_number), self.thread_number)]
        """
        import asyncio

        [asyncio.run(self.do_something(timeout)) for timeout in random.sample(range(0, self.thread_number), self.thread_number)]

    def test_asyncio_loop(self):
        """
        2) create_task 则会以异步方式执行. loop.create_task 会异步建立任务，然后逐个执行，相比较前一方法，建立一个，执行一个要快的多．
        """
        import asyncio

        # 需要先获得 event loop
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(self.do_something(timeout)) for timeout in random.sample(range(0, self.thread_number), self.thread_number)]

        # 为任务添加 callback. add_done_callback 会将结果包含在 Task 结构中并将整个 Task 传给回调函数，回调函数通过 Task.result() 取出返回值．
        [task.add_done_callback(self.__callback) for task in tasks]

        # resp = [loop.run_until_complete(task) for task in tasks]
        resp = loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    def test_asyncio_ensure_future(self):
        """
        你可以不需要显式通过 loop 来提交运算，使用　asyncio.ensure_future 提交，最后在使用 loop 来获取结果．
        """
        import asyncio
        tasks = [asyncio.ensure_future(self.do_something(timeout)) for timeout in random.sample(range(0, self.thread_number), self.thread_number)]
        [task.add_done_callback(self.__callback) for task in tasks]

        # All "false", 显然异步任务还没有完成．
        [print(task.done()) for task in tasks]

        # 最后再得到 loop 来获取结果．
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    def test_asyncio_call_soon(self):
        import asyncio

        loop = asyncio.get_event_loop()
        tasks = [loop.call_soon(self.do_something, timeout) for timeout in random.sample(range(0, self.thread_number), self.thread_number)]
        f = asyncio.run_coroutine_threadsafe(asyncio.wait(tasks), loop)
        loop.close()
