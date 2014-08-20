from adjax.registry import registry

from .models import CustomObject


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
