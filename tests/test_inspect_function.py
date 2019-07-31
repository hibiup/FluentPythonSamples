def tag(name, *content, cls:'html class tag'=None, **attrs) -> str:
    """生成一个或多个HTML标签"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value)
            for attr, value
            in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)


from unittest import TestCase


class InspectTest(TestCase):
    def test_inspect(self):
        print("class annotations: ", tag.__annotations__)

        import inspect
        sig = inspect.signature(tag)
        my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
        bound_args = sig.bind(**my_tag)
        print("all arguments: ", bound_args)
        print("default argument: ", bound_args.args)
        print("key_only arguments: ", bound_args.kwargs)
