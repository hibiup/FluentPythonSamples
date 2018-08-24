from unittest import TestCase

import array
import numpy


class TestListComprehension(TestCase):
    def test_list_set_generator(self):
        # list comprehension - 能生成 list s和 set；生成全部元素, not iterable, 没有 __next__()
        l = [x for x in range(0, 10)]    # 得到 list, __iter__ 返回 list_iterable 对象
        assert(l[3] == 3)

        s = {x for x in range(0, 10)}    # 得到 set,　__iter__ 返回 set_iterablor 对象
        assert(list(s)[3] == 3)

        g = (x for x in range(0, 10))    # 得到 generator，不是 list 或 set, __iter__返回的仍然是 generator
        assert(next(g) == 0)

    def test_array_and_numpy(self):
        # list 和 set 可被用于 array，没有区别
        a = array.array('h', [x for x in range(0, 10)])  #_iter__ 返回 arrayiterablor 对象
        a1 = array.array('h', {x for x in range(0, 10)})
        assert(a[3] == a1[3])

        # numpy 则有区别
        n = numpy.array([x for x in range(0, 10)])       #__iter__ 返回 iterablor 对象
        n1 = numpy.arange(0, 10)
        assert(n[3] == n1[3])

        # 而 set 用于 numpy 得到的是只包含一个 set 元素的 array
        ns = numpy.array({x for x in range(0, 10)})
        ns_set = ns.item(0)
        assert(type(ns_set) == set)
        lns = list(ns.item(0))
        assert(lns[3] == n1[3])

        # generator 用于 array.array 和 numpy.array 也不同
        # array.array 会调用 generater，得到 array.array，和直接使用 list 或 set 一样
        aa = array.array('h', (x for x in range(0, 10)))
        assert(aa[3] == a[3])

        # 但是 numpy 视其为包含一个 generater 的单元素 numpy array
        na = numpy.array((x for x in range(0, 10)))
        # assert(na[3] == 3 )  #　理坏乐崩!
        g_na = na.item(0)
        assert(next(g_na) == 0)
        assert(next(g_na) == 1)
