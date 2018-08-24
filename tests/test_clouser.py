from unittest import TestCase


def make_average(offset):
    count = 0
    total = 0
    o = offset

    def average():
        return total / count

    def add_new_values(new_value):
        # 数字或不可变类型做inplace(+=)操作等同 count = count + 1，会导致（缺省）生成一个新的本地变量，
        # 如果该变量不是本地变量，那么需要修饰成 global 或 nonlocal，否则会编译错误(name 'count' is not defined).
        # 或一个变通的方法（python2）是将它们绑定到可变变量（字典或实例）
        nonlocal count, total, o
        count += 1
        total += new_value - o

    return add_new_values, average


who = "Jeff"
def lambda_target(msg):
    print(f"{who}: {msg}")


class TestClosure(TestCase):
    def test_nonlocal_from_closure(self):
        offset = 1
        add, avg = make_average(offset)

        add(10)
        assert(9 == avg())

        add(20)
        assert(14 == avg())

    def test_lambda(self):
        mesage = "Print lambda"
        who = "Bob"

        def lambda_caller(lambda_target):
            lambda_target(mesage)

        lambda_caller(lambda s: lambda_target(s))
        lambda_caller(lambda s: print(who))