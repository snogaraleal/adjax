from functools import wraps

from .inspect import get_full_arg_spec


class typed(object):
    """ Decorator that does type checks according to annotations.

    @typed(strict=True)
    def do_something(a: bool, b: int = 3) -> bool:
        return False
    """

    def __init__(self, annotations=None, strict=False):
        self.strict = strict
        self.annotations = annotations

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
        argnames, defaults, annotations = get_full_arg_spec(func)
        annotations = self.annotations or annotations

        return_cls = annotations.get('return')

        @wraps(func)
        def wrapper(*args, **kwargs):
            values = defaults.copy()
            values.update(dict(zip(argnames, args)))
            values.update(kwargs)

            for argname, argcls in annotations.items():
                if argname == 'return':
                    continue

                argvalue = values[argname]
                if not self.is_instance(argvalue, argcls):
                    raise TypeError(
                        'Value {} of type {} is not a {} instance'.format(
                            argvalue, type(argvalue), argcls))

            value = func(*args, **kwargs)

            if (return_cls is not None and
                    not self.is_instance(value, return_cls)):
                raise TypeError(
                    'Returned {} of type {} instead of {}'.format(
                        value, type(value), return_cls))

            return value

        if not hasattr(wrapper, '__wrapped__'):
            wrapper.__wrapped__ = func

        return wrapper
