from multiprocessing import Process, Queue, Pool
from unittest import TestCase
import time


"""
Multiple processing 会复制堆，因此是多任务安全的。
"""

name = 'John'


class TestMultipleProcessing(TestCase):
    """
    目标函数可以是 staticmethod classmethod 或 global function, 但是不可以是一般类方法
    """
    @staticmethod
    def target_func_1(param):
        time.sleep(1)
        """不会受到主进程修改变量的影响。"""
        print('Sub process: Hello', name, 'and', param)
        return 'Sub process: Hello', name, 'and', param

    def test_multiple_processing(self):
        global name

        """参数通过 args 传入(可选) """
        p = Process(target=TestMultipleProcessing.target_func_1, args=('Angular',))
        p.start()
        print('Main process: Hello', name)

        """ 主进程修改了变量，但是Multiple processing 会复制堆，因此不会受到影响。 """
        name = "Merry"
        print('Main process: Hello', name)

        p.join()



    @staticmethod
    def target_func_2(param, q):
        q.put('Sub process: Hello {0}'.format(param))


    """
    测试通过 Queue 返回返回值
    """
    queue = Queue()

    def test_queue_for_return_value(self):
        """
        因为 Process 会重建堆和当前栈，所以如果直接引用已经定义的 Queue，那么实际上将各自连到两个不同的实例。
        所以必须将 Queue 通过参数传递给新的 Process，这样才能将相同的实例注入不同的栈中，
        """
        pro1 = Process(target=self.target_func_2, args=('Angular', self.queue))
        pro2 = Process(target=self.target_func_2, args=('React', self.queue))

        pro1.start()
        pro2.start()

        pro1.join()
        print("q is ", self.queue.get())

        pro2.join()
        print("another q is ", self.queue.get())
