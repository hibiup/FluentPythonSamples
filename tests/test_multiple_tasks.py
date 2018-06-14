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
    return do_something(timeout)

class TestConcurrentProcessing(TestCase):
    thread_number = 5
    time_slots = [timeout for timeout in random.sample(range(0, thread_number), thread_number)]

    def test_thread_pool_executor(self):
        with futures.ThreadPoolExecutor(self.thread_number) as executor:
            res = executor.map(do_something, self.time_slots)
            print("All thread submitted.")

            print(f"All threads {list(res)} are done!")

    def test_future(self):
        with futures.ThreadPoolExecutor(self.thread_number) as executor:
            future_list = [executor.submit(do_something, timeout) for timeout in self.time_slots]
            print("All thread submitted.")
            
            first_result = [ finished.result() for finished in futures.wait(future_list, return_when=futures.FIRST_COMPLETED).done]
            print(f"First future {first_result} is done!")

            completed_tasks = [ future.result() for future in futures.as_completed(future_list)]
            print(f"All threads {completed_tasks} are done!")

    def test_coroutine(self):
        # 并发提交
        coroutines = [do_something_with_coroutine(timeout) for timeout in self.time_slots]
        [next(coroutine) for coroutine in coroutines]
        print("All thread submitted.")

        # 但是一个一个地阻塞执行，不会并发执行
        print(datetime.datetime.utcnow())
        [print(f"Retuen with {next(coroutine)}") for coroutine in coroutines]

    def test_coroutine_with_thread(self):
        # 并发提交
        coroutines = [do_something_with_coroutine(timeout) for timeout in self.time_slots]
        [next(coroutine) for coroutine in coroutines]
        print("All thread submitted.")

        # 并发执行协程是可能的，coroutine 所属线程也会发生变化.
        with futures.ThreadPoolExecutor(self.thread_number) as executor:
            future_list = [executor.submit(lambda c: next(c), coroutine) for coroutine in coroutines]
            completed_tasks = [ future.result() for future in futures.as_completed(future_list)]
            print(f"All threads {completed_tasks} are done!")

    def test_asyncio(self):
        def future_callback(future):
            print(f"Thread[{threading.get_ident()}] - Future saying: {future.result()}")

        loop = asyncio.get_event_loop()

        tasks = [asyncio.Task(do_something_with_asyncio(timeout), loop=loop) for timeout in self.time_slots]
        print("All tasks are created!!")

        for task in tasks:
            task.add_done_callback(future_callback)
        print("Tasks' future are set.")

        loop.run_until_complete(asyncio.wait(tasks))

        loop.close()
        print(f"All threads {tasks} are done!")

        for task in tasks:
            print(task.result())
