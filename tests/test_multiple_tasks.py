from unittest import TestCase

import time
import random
import threading
from concurrent import futures
import datetime
import asyncio


def do_something(timeout):
    thread_id = threading.get_ident()
    print(f"Thread[{thread_id}]: will runs for {timeout+1} second(s).")
    time.sleep(timeout+1)
    print(f"[{datetime.datetime.utcnow()}] - Thread - {thread_id}: is done")
    return thread_id, timeout


def do_something_with_coroutine(timeout):
    thread_id = threading.get_ident()    # 取得 thread id
    print(f"Thread[{threading.get_ident()}]: will runs for {timeout+1} second(s).")
    yield
    new_thread_id = threading.get_ident()    # 再次取得 thread id 会发现在多线程状态下，coroutine 会"漂移"到新的线程中去
    time.sleep(timeout+1)
    print(f"[{datetime.datetime.utcnow()}] - Thread[{new_thread_id}]: is done")
    yield f"{thread_id} -> {new_thread_id}", timeout   # 返回（新旧）线程 ID 和 timeout 以示区别


async def do_something_with_asyncio(timeout):
    '''
    这个函数和 do_something() 非常类似，但是使用了 非阻塞 asyncio.sleep() 来挂起协程，
    await 关键字在遇到非阻塞调用的时候会让出当前协程，因此我们可以看到其他并行的协程会获得继续执行的机会。
    '''
    thread_id = threading.get_ident()
    print(f"Thread[{thread_id}]: will runs for {timeout+1} second(s).")
    await asyncio.sleep(timeout)  # 非阻塞式 time.sleep()
    print(f"[{datetime.datetime.utcnow()}] - Thread - {thread_id}: is done")
    return thread_id, timeout


class TestConcurrentProcessing(TestCase):
    thread_number = 5
    parameters = [timeout for timeout in random.sample(range(0, thread_number), thread_number)]

    def test_thread_pool_executor(self):
        with futures.ThreadPoolExecutor(self.thread_number) as executor:
            res = executor.map(do_something, self.parameters)
            print("All thread submitted.")

            print(f"All threads {list(res)} are done!")

    def test_future(self):
        with futures.ThreadPoolExecutor(self.thread_number) as executor:
            future_list = [executor.submit(do_something, timeout) for timeout in self.parameters]
            print("All thread submitted.")
            
            first_result = [ finished.result() for finished in futures.wait(future_list, return_when=futures.FIRST_COMPLETED).done]
            print(f"First future {first_result} is done!")

            completed_tasks = [ future.result() for future in futures.as_completed(future_list)]
            print(f"All threads {completed_tasks} are done!")

    def test_asyncio(self):
        '''
        （良好的例子）并发协程：总是按执行时间快慢输出结果，但是输入的顺序未必是按时间排序的。因为使用了异步 io（asyncio），因此协程之间不会互相阻塞

        参考：http://python.jobbole.com/87310/
        '''
        loop = asyncio.get_event_loop()

        # 随即定义任务顺序
        tasks = [asyncio.ensure_future(do_something_with_asyncio(timeout), loop=loop) for timeout in self.parameters]
        print("All tasks are created!!")

        # 可选: 为 Future 设置 callback
        def future_callback(future):
            print(f"Thread[{threading.get_ident()}] - Future saying: {future.result()}")

        for task in tasks:
            task.add_done_callback(future_callback)
        print("Tasks' future are set.")

        # 执行并发协程，会看到任务按时间循序完成输出
        async def run_loop(tasks, process):
            for task in asyncio.as_completed(tasks):
                result = await task
                process(result)

        loop.run_until_complete(run_loop(tasks, lambda x: print(x)))

        # 结束
        loop.close()
        print(f"All threads {tasks} are done!")

    def test_coroutine(self):
        '''
        （不好的例子）非并发协程：因为没有使用异步 asyncio.sleep() 来暂停程序，因此任务会一个一个以阻塞方式执行
        '''
        # 并发提交
        coroutines = [do_something_with_coroutine(timeout) for timeout in self.parameters]
        [next(coroutine) for coroutine in coroutines]
        print("All thread submitted.")

        # 但是一个一个地阻塞执行，不会并发执行
        print(datetime.datetime.utcnow())

        # 结束
        [print(f"Retuen with {next(coroutine)}") for coroutine in coroutines]

    def test_coroutine_with_thread(self):
        '''
        如果我们必须在协程中调用阻塞调用，一个改进的作法是使用 loop.run_in_executor() 方法和线程池结合
        这种情况下实际上等于多线程
        '''
        with futures.ThreadPoolExecutor(self.thread_number) as executor:
            loop = asyncio.get_event_loop()

            # run_in_executor() 将阻塞调用包装成 Future
            tasks = [loop.run_in_executor(executor, do_something, timeout) for timeout in self.parameters]

            '''
            然后可以交由 run_until_complete(), run_until_complete() 调用的时候会启动线程来执行

            注意: run_until_complete() 本身是阻塞的，因此5个线程都执行完后才会进入下一指令，可以就像 test_asyncio() 
            一样将该循环包装成另一个协程 (async def ...)，然后使用 await asyncio.as_completed() 逐个获得以非阻塞方式获取结果，
            '''
            loop.run_until_complete(asyncio.wait(tasks))
            for task in tasks:
                print(task.result())

            loop.close()
