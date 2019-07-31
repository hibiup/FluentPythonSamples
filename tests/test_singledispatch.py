from functools import singledispatch
from collections import abc
import numbers
import html

"""
@singledispatch 实现函数方法的重载。可以用于取代 if/elif/else 或 switch/case 控制。
"""

# 1) 用 singledispatch 定义一个缺省函数
@singledispatch
def htmlize(obj):                       # 处理缺省数据类型
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)

# 2) 然后用 <缺省函数名>.register() 注册要另外做处理的对象的数据类型.
@htmlize.register(str)                  # 处理 str。
def _(text):                            # 因为这函数服从它的主要函数，因此身的名称没有必要，可以使用匿名函数“_"来代替
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)

@htmlize.register(numbers.Integral)      # 处理 int
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)

# 装饰器叠放,等同于: singledispatch(singledispatch(htmlize()))
@htmlize.register(tuple)                  # tuple
@htmlize.register(abc.MutableSequence)    # list 
def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'


from unittest import TestCase


class TestSingledispatch(TestCase):
    def test_singledispatch(self):
        print(htmlize({1, 2, 3}))       # 调用缺省obj处理函数
        print(htmlize(23))              # int
        print(htmlize(1.23))            # 浮点数不是int，因此也只能调用缺省
        print(htmlize([1, 2, 3]))       # list 会调用 abc.MutableSequence
        print(htmlize((1, 2, 3)))
