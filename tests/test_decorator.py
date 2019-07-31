import functools


class SampleZ(object):
    """
    类装饰器：

    类装饰器可能导致被装饰方法丢失 'self'。descriptor protocol
    (https://docs.python.org/3/reference/datamodel.html#implementing-descriptors) 可用于 “自我介绍”。因此
    定义一个 class decorator 可以通过重载 descriptor protocol 方法解决问题。

    参考：https://stackoverflow.com/questions/5469956/python-decorator-self-is-mixed-up
    """
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        '''
        装饰方法
        '''
        if (SqlExecutor.sample_number != -1):
            kwargs["sql"] = kwargs["sql"] + " sample %d" % SqlExecutor.sample_number
        self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        """
        __get__(): descriptor protocol 方法当 python 调用某个方法或属性时首先查找 __get__是否存在，
        然后才查找 __dict__，我们通过此方法修改 self

        functools.partial()：偏函数，将 __call__(self, ...) 的第一个参数绑定为 instance，也就是被装饰的类实例
        并返回新的 __call__()，解决了 self 问题
        """
        return functools.partial(self.__call__, instance)


def sample(func):
    """
    函数装饰器
    """
    def wrapper(*args, **kwargs):
        if (SqlExecutor.sample_number != -1):
            kwargs["sql"] = kwargs["sql"] + " sample %d" % SqlExecutor.sample_number
        func(*args, **kwargs)
    return wrapper


class SqlExecutor:
    sample_number = -1
    def __init__(self, sample=-1):
        SqlExecutor.sample_number = sample

    @SampleZ
    def target_func(self, sql):
        print(sql)
        print(self.sample_number)


from unittest import TestCase


class TestDecorator(TestCase):
    def test_decorator(self):
        sqlExecutor = SqlExecutor(sample=100)
        sqlExecutor.target_func(sql = "SELECT count(*) FROM dummy")
