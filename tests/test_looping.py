from unittest import TestCase

import datetime, time
import numpy as np
import pandas as pd


class TestLooping(TestCase):
    def __random_date(self, from_date, to_date, number):

        start = time.mktime(from_date.timetuple())
        end = time.mktime(to_date.timetuple())

        return [datetime.datetime.fromtimestamp(n) for n in np.random.randint(start,end, size=(number,1))]
    
    def __prepare_df(self):
        from_date = datetime.datetime(2011, 10, 21, 0, 0)
        to_date = datetime.datetime(2018, 10, 21, 0, 0)
        df = pd.DataFrame(self.__random_date(from_date, to_date, 500000), columns=['activation_date'])
        return df.activation_date.apply(pd.to_datetime)

    def __test_yield(self, df_raw):
        for x in df_raw:
            yield x.week

    def __test_for_loop(self, df_raw):
        week_list = [x.week for x in df_raw]
        return week_list

    def __test_list_generator(self, df_raw):
        week_gen = (x.week for x in df_raw)
        return week_gen

    def __test_dataframe_apply(self, df_raw):
        week_series = df_raw.apply(lambda x : x.week)
        return week_series

    def __test_map(self, df_raw):
        week_map = map(lambda x: x.week, df_raw)
        return week_map

    def test_apply(self):
        df_raw = self.__prepare_df()
        t1 = time.time()
        self.__test_yield(df_raw)
        t2 = time.time()
        self.__test_map(df_raw)
        t3 = time.time()
        self.__test_list_generator(df_raw)
        t4 = time.time()
        self.__test_for_loop(df_raw)
        t5 = time.time()
        self.__test_dataframe_apply(df_raw)
        t6 = time.time()
        print("Result:")
        print("yield spent: " + str(t2 - t1))
        print("map spent: " + str(t3 - t2))
        print("list generator spent: " + str(t4 - t3))
        print("for loop spent: " + str(t5 - t4))
        print("DataFrame apply spent: " + str(t6 - t5))

    def test_map_vs_loop(self):
        """
        timeit模块提供了一种简便的方法来为 Python 中的小块代码进行计时：
          * 第一个参数为要执行计时的语句（statement）。按字符串的形式传入要执行的代码。
          * 第二个参数setup用于构建代码环境，可以用来导入需要的模块。
          * 最后的number指定了运行的次数。
        """
        import timeit

        TIMES = 10000

        SETUP = """
symbols = 'ABCDEF'
def non_ascii(c):
    return c > 127
        """

        def clock(label, cmd):
            res = timeit.repeat(cmd, setup=SETUP, number=TIMES)
            print(label, *('{:.3f}'.format(x) for x in res))

        clock('listcomp        :', '[ord(s) for s in symbols if ord(s) > 127]')
        clock('listcomp + func :', '[ord(s) for s in symbols if non_ascii(ord(s))]')
        clock('filter + lambda :', 'list(filter(lambda c: c > 127, map(ord, symbols)))')
        clock('filter + func   :', 'list(filter(non_ascii, map(ord, symbols)))')
