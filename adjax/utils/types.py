from functools import wraps
from inspect import getfullargspec


class typed(object):
    """ Decorator that does type checks according to annotations.

    @typed(strict=True)
    def do_something(a: bool, b: int = 3) -> bool:
        return False
    """

    def __init__(self, strict=False):
        self.strict = strict

    def is_instance(self, instance, cls):
        """ Check that instance is of type cls.
        """
        if self.strict:
            return type(instance) == cls
        else:
            return isinstance(instance, cls)

    def __call__(self, func):
        """ Decorate function.
        """

        argspec = getfullargspec(func)

        defaults = {}
        if argspec.defaults:
            defaults = dict(zip(reversed(argspec.args),
                                reversed(argspec.defaults)))

        return_cls = argspec.annotations.get('return')

        @wraps(func)
        def wrapper(*args, **kwargs):
            values = defaults.copy()
            values.update(dict(zip(argspec.args, args)))
            values.update(kwargs)

            for argname, argcls in argspec.annotations.items():
                if argname == 'return':
                    continue

                argvalue = values[argname]
                if not self.is_instance(argvalue, argcls):
                    raise TypeError(
                        'Value {0} of type {1} is not a {2} instance'.format(
                            argvalue, type(argvalue), argcls))

            value = func(*args, **kwargs)

            if (return_cls is not None and
                    not self.is_instance(value, return_cls)):
                raise TypeError(
                    'Returned {0} of type {1} instead of {2}'.format(
                        value, type(value), return_cls))

            return value

        return wrapper
