from unittest import TestCase


def make_average():
    count = 0
    total = 0

    def average():
        return total / count

    def add_new_values(new_value):
        # 数字或不可变类型做inplace(+=)操作等同 count = count + 1，会导致（缺省）生成一个新的本地变量，
        # 如果该变量不是本地变量，那么需要修饰成 global 或 nonlocal，否则会编译错误(name 'count' is not defined).
        # 或一个变通的方法（python2）是将它们绑定到可变变量（字典或实例）
        nonlocal count, total
        count += 1
        total += new_value

    return add_new_values, average


class TestClosure(TestCase):
    def test_nonlocal_from_closure(self):
        add, avg = make_average()

        add(10)
        assert(10 == avg())

        add(20)
        assert(15 == avg())
