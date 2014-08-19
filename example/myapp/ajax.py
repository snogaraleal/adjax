from adjax.registry import registry
from adjax.serializer import serializer, ObjectType


class CustomObject(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


@registry.register
def func1(request, a, b, c=1):
    return {
        'a': a,
        'b': b,
        'c': c,

        'custom': CustomObject(1, 2),
    }


@registry.register
def func2(request, a=1, b=2, c=3):
    return bool(a > b > c)


@serializer.enable
class CustomType(ObjectType):
    name = 'custom'
    cls = CustomObject

    @classmethod
    def encode(cls, value):
        return {
            'x': value.x,
            'y': value.y,
        }

    @classmethod
    def decode(cls, value):
        return CustomObject(value['x'], value['y'])
