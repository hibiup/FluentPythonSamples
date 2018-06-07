class A:
    def __new__(cls, *args, **kwargs):
        print(f"A.__new__({args}, {kwargs})")
        return B(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        print(f"A.__init__({args}, {kwargs})")
    
    def __repr__(self):
        return "I'm A"

class B:
    def __new__(cls, *args, **kwargs):
        print(f"B.__new__({args}, {kwargs})")
        return super(B, cls).__new__(cls)
    
    def __init__(self, *args, **kwargs):
        print(f"B.__init__({args}, {kwargs})")

    def __repr__(self):
        return "I'm B"


from unittest import TestCase
class TestHash(TestCase):
    def test_a_creation(self):
        a = A(1, a=2)
        print(a)
