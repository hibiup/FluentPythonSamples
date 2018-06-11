import contextlib

@contextlib.contextmanager
def looking_glass():
    '''
    Test @contextmanager decorator, and surround `yield` with `try...except` for save
    '''
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])
    sys.stdout.write = reverse_write
    msg = ''

    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)

from unittest import TestCase
class TestContextManager(TestCase):
    def test_context_manager(self):
        with looking_glass() as lg:
            print("Reverse string")
            print("Test divide to zero!" + str(1/0))   # Make exception
