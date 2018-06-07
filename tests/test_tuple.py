from unittest import TestCase

import collections
Card = collections.namedtuple('CARD', ['RANK', 'SUIT'])
def fake(self):
    return str(self)
Card.fake = fake

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

    def __init__(self):
        self._cards = [Card(Rank, Suit) for Suit in self.suits
                                        for Rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    # All [] metnods will be past to this function.
    def __getitem__(self, position):
        return self._cards[position]

    def __repr__(self):
        return str(self._cards)   # call to list.__str__()

    @classmethod
    def spades_high(clazz, card:Card):
        rank_value = FrenchDeck.ranks.index(card.RANK)
        return rank_value * len(FrenchDeck.suit_values) + FrenchDeck.suit_values[card.SUIT]


class TestCard(TestCase):
    def test_shuf_cards(self):
        import random
        deck = FrenchDeck()
        print(deck)                   # call __repr__() or __str__()

        print(len(deck))              # call __len__()
        print(random.choice(deck))    # call desk[] -> __getitem__()

        #print(desk._cards)
        for card in deck:             # call desk[] -> __getitem__()
            print(card)

        for card in sorted(deck, key=FrenchDeck.spades_high):  # sorted 可以根据 key 参数的返回值排序。
            print(card)
    
    def test_add_method(self):
        card = Card("A1","B2")
        print(card.fake())
    
class TestTuple(TestCase):
    '''
    tuple 可以当作不可变数据库使用
    '''
    def test_tuple(self):
        from collections import namedtuple
        Coordinate = namedtuple('COORDINATE', 'LATITUDE LONGITUDE')
        City = namedtuple('CITY', 'NAME COUNTRY POPULATION COORDINATE')

        metro_areas = [
            City('Tokyo','JP',36.933, Coordinate(35.689722, 139.691667)),     # 城市,国家,人口数,(经纬度)
            City('Delhi NCR', 'IN', 21.935, Coordinate(28.613889, 77.208889)),
            City('Mexico City', 'MX', 20.142, Coordinate(19.433333, -99.133333)),
            City('New York-Newark', 'US', 20.104, Coordinate(40.808611, -74.020386)),
            City('Sao Paulo', 'BR', 19.649, Coordinate(-23.547778, -46.635833)),
        ]

        print(City._fields)

        print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
        for name, *_, (latitude, longitude) in metro_areas:   # “*_” 由两个通配符组成 “*” 表示任意个数。“_” 表示匿名，在这里表示忽略中间两个元素
            if longitude <= 0:
                print('{:15} | {:9.4f} | {:9.4f}'.format(name, latitude, longitude))

        print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
        for city in metro_areas:
            if city.COORDINATE.LONGITUDE <= 0:
                print('{:15} | {:9.4f} | {:9.4f}'.format(city.NAME, city.COORDINATE[0], city.COORDINATE[1]))
    
    def test_increase(self):
        # tuple, 是不可变类型，没有 inner add:  __iadd__() 方法，+ 操作会导致一个新的变量产生
        t = (1, 2, 3)
        before = (t)
        t += (4,5)
        after = id(t)
        assert(before != after)

        # list 是可变类型，有 __iadd__() 方法，+ 操作不会导致新的变量产生
        l = [1, 2, 3]
        before = id(l)
        l += [4, 5]
        after = id(l)
        assert(before == after)

        t = (1, 2, [30, 40])
        t[2] += [50, 60]

    def test_bisect(self):
        import bisect
        import sys
        HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
        NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]

        print("Start:")
        ROW_FMT = '{0:2d}@{1:2d} +   {2}{0:<2d}'
        
        print('haystack->', ' '.join('%2d' % n for n in HAYSTACK))
        for needle in reversed(NEEDLES):
            position = bisect.bisect(HAYSTACK, needle)
            offset = position * '  |'
            print(ROW_FMT.format(needle, position, offset))

        print('haystack->', ' '.join('%2d' % n for n in HAYSTACK))
        for needle in reversed(NEEDLES):
            position = bisect.bisect_left(HAYSTACK, needle)
            offset = position * '  |'
            print(ROW_FMT.format(needle, position, offset))
        
        print('haystack->', HAYSTACK)
        for needle in reversed(NEEDLES):
            bisect.insort(HAYSTACK, needle)
            print(HAYSTACK)

    def test_memoryview(self):
        import array
        numbers = array.array('h', [-2, -1, 0, 1, 2])  # 'h': signed_int
        memv = memoryview(numbers)
        print(memv.tolist())       # 打印出 [-2, -1, 0, 1, 2]

        memv_oct = memv.cast('B')  # 'B': Convert to unsigned_short_int
        print(memv_oct.tolist())   # 打印出 [254, 255, 255, 255, 0, 0, 1, 0, 2, 0].
                                   # 每个 signed_int 被解释成 [low, hight] 两个 unsigned_short_int

        memv_oct[5] = 4            # 修改原 0 -> 0, 0 的高位，变成 0, 4 (00, 10)
        print(memv.tolist())       # 输出 [-2, -1, 1024, 1, 2]

    def test_dictcomp(self):
        '''
        字典推导（dict comprehension）可以从任何以键值对作为元素的可迭代对象中构建出字典。
        '''
        DIAL_CODES = [
            (86, 'China'),
            (91, 'India'),
            (1,  'United States'),
            (62, 'Indonesia'),
            (55, 'Brazil'),
            (92, 'Pakistan'),
            (880,'Bangladesh'),
            (234,'Nigeria'),
            (7,  'Russia'),
            (81, 'Japan')
        ]
        country_code = {country: code for code, country in DIAL_CODES}
        print(country_code)

    def test_mapping_proxy(self):
        from types import MappingProxyType
        d = {1:'A'}
        d_proxy = MappingProxyType(d)
        assert(d == d_proxy)

        d[2] = 'B'
        assert(d_proxy[2] == d[2])

    def test_set_speed(self):
        '''
         比较在一个集合中查找与另一个集合重复的元素的速度
        '''

        from timeit import timeit
        print()

        DATA_SET_1 = '''
s1 = set([n for n in range(1000)])
s2 = set([n for n in range(500)])
'''
        DATA_SET_2 = '''
s1 = set([n for n in range(10000)])
s2 = set([n for n in range(5000)])
'''
        DATA_SET_3 = '''
s1 = set([n for n in range(100000)])
s2 = set([n for n in range(50000)])
'''
        set_end_opt = '''s = s1 & s2'''
        print("set_end_opt() with 1,000 data:   ", timeit(set_end_opt, setup=DATA_SET_1, number=1))
        print("set_end_opt() with 10,000 data:  ", timeit(set_end_opt, setup=DATA_SET_2, number=1))
        print("set_end_opt() with 100,000 data: ", timeit(set_end_opt, setup=DATA_SET_3, number=1))

        set_loop_opt = '''
found = 0
for n in s2:
    if n in s1:
        found += 1
print(found)
'''
        print("set_loop_opt() with 1,000 data:   ", timeit(set_loop_opt, setup=DATA_SET_1, number=1))
        print("set_loop_opt() with 10,000 data:  ", timeit(set_loop_opt, setup=DATA_SET_2, number=1))
        print("set_loop_opt() with 100,000 data: ", timeit(set_loop_opt, setup=DATA_SET_3, number=1))


    def test_list_speed(self):
        '''
         比较在一个 List 中查找与另一个 List 重复的元素的速度，速度明显慢于Set，因为 List 是可变列表，可变列表没有 hash 支持。
        '''
        print()
        from timeit import timeit
        DATA_LIST_1 = '''
l1 = [n for n in range(1000)]
l2 = [n for n in range(500)]
'''
        DATA_LIST_2 = '''
l1 = [n for n in range(10000)]
l2 = [n for n in range(5000)]
'''
        DATA_LIST_3 = '''
l1 = [n for n in range(100000)]
l2 = [n for n in range(50000)]
'''
        list_loop_opt = '''
found = 0
for n in l2:
    if n in l1:
        found += 1
print(found)
'''
        print("list_loop_opt() with 1,000 data:   ", timeit(list_loop_opt, setup=DATA_LIST_1, number=1))
        print("list_loop_opt() with 10,000 data:  ", timeit(list_loop_opt, setup=DATA_LIST_2, number=1))
        print("list_loop_opt() with 100,000 data: ", timeit(list_loop_opt, setup=DATA_LIST_3, number=1))

        convert_list_to_set_then_loop = '''
s1 = set(l1)
s2 = set(l2)
found = len(s1 & s2)
print(found)
'''
        print("convert_list_to_set_then_loop() with 1,000 data:   ", timeit(convert_list_to_set_then_loop, 
            setup=DATA_LIST_1, number=1))
        print("convert_list_to_set_then_loop() with 10,000 data:  ", timeit(convert_list_to_set_then_loop, 
            setup=DATA_LIST_2, number=1))
        print("convert_list_to_set_then_loop() with 100,000 data: ", timeit(convert_list_to_set_then_loop,
            setup=DATA_LIST_3, number=1))

        convert_list_to_dict_then_loop = '''
d1 = {l:l for l in l1}
d2 = {l:l for l in l2}
found = 0
for n in d2:
    if n in d1:
        found += 1
print(found)
'''
        print("convert_list_to_dict_then_loop() with 1,000 data:   ", timeit(convert_list_to_dict_then_loop, 
            setup=DATA_LIST_1, number=1))
        print("convert_list_to_dict_then_loop() with 10,000 data:  ", timeit(convert_list_to_dict_then_loop, 
            setup=DATA_LIST_2, number=1))
        print("convert_list_to_dict_then_loop() with 100,000 data: ", timeit(convert_list_to_dict_then_loop,
            setup=DATA_LIST_3, number=1))

        convert_list_to_tuple_then_loop = '''
t1 = tuple(l1)
t2 = tuple(l2)
found = 0
for n in t2:
    if n in t1:
        found += 1
print(found)
'''
        print("convert_list_to_tuple_then_loop() with 1,000 data:   ", timeit(convert_list_to_tuple_then_loop, 
            setup=DATA_LIST_1, number=1))
        print("convert_list_to_tuple_then_loop() with 10,000 data:  ", timeit(convert_list_to_tuple_then_loop, 
            setup=DATA_LIST_2, number=1))
        print("convert_list_to_tuple_then_loop() with 100,000 data: ", timeit(convert_list_to_tuple_then_loop,
            setup=DATA_LIST_3, number=1))
