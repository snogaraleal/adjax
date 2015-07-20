from datetime import datetime, timedelta

from adjax.registry import registry
from adjax.utils.types import typed

from .models import CustomObject


@registry.register
@typed({'a': int})
def func1(request, a, b, c=1):
    return {
        'a': a,
        'b': b,
        'c': c,

        'custom': CustomObject(1, 2),
    }


@registry.register
@typed({'a': int, 'b': int, 'c': int, 'return': CustomObject})
def func2(request, a=1, b=2, c=3):
    return CustomObject(1, 2)


@registry.register
@typed({'some_date': datetime, 'return': datetime})
def func3(request, some_date):
    return some_date + timedelta(days=2)
