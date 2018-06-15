class Meter(object):
    def __init__(self, value=0.0):
        self.value = float(value)

    def __get__(self, instance, owner):
        '''
        具有 Decriber 方法的类实例被引用 ( refer.property ) 的时候，会被转换成:
        type(refer).__dict__['property'].__get__(refer, type(refer)) 调用:
        '''
        print("Meter.__get__() is called", instance, owner)
        return self.value

    def __set__(self, instance, value):
        '''
        接受 number 类型参数，然后转换成 float，这也意味这，这个类(Meter)的实例被赋值的时候必须接受 number 类型，而不是它本身的类型
        '''
        print("Meter.__set__() is called", instance, value)
        self.value = float(value)

class Foot(object):
    def __get__(self, instance, owner):
        '''
        当 describer 方法被触发的时候，instance 指向引用者(Distance)的实例，owner 则是引用类，因此我们可以从 instance 
        中获得 Meter的实例然后做转换。当然这也会递归触发 Metter.__get__()
        '''
        print("Foot.__get__() is called", instance, owner)
        return instance.meter * 3.2808

    def __set__(self, instance, value):
        print("Foot.__set__() is called", instance, value)
        instance.meter = float(value) / 3.2808

class Distance(object):
    meter = Meter()                      # class 自己调用自己的属性，不会触发 describer 方法
    foot = Foot()                        # class 自己调用自己的属性，不会触发属性的 describer 方法
    def __init__(self, number):
        # 接受一个 number 而不是 Meter，因为 __set__() 会转换数据类型
        self.meter = float(number)       # 调用类属性会触发 describer 方法
        self.new_meter = float(number)   # 非类属性不会触发 describer 方法


from unittest import TestCase
class TestDescriber(TestCase):
    def test_Distance(self):
        d =  Distance(10)       # 通过 __init__() 间接触发 __set__()
        d.meter=100             # 直接触发 __set__()
        print(f"[d.meter] Visit class property will trigger describer method: {d.meter}")             # 触发 __get__()
        print(f"[d.foot] Visit class property will trigger describer method: {d.foot}")               # 触发 __get__()
        print(f"[d.new_meter] Visit instance property will not trigger describer method: {d.new_meter}")    # 不会触发 __get__()
