from datetime import datetime, timedelta

from adjax.registry import registry
from adjax.utils.types import typed

from .models import CustomObject


@registry.register
@typed()
def func1(request, a: int, b, c=1):
    return {
        'a': a,
        'b': b,
        'c': c,

        'custom': CustomObject(1, 2),
    }


@registry.register
@typed()
def func2(request, a: int=1, b: int=2, c: int=3) -> CustomObject:
    return CustomObject(1, 2)


@registry.register
@typed()
def func3(request, some_date: datetime) -> datetime:
    return some_date + timedelta(days=2)
