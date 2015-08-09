import sys


if sys.version_info >= (3, 0):
    from inspect import getfullargspec

    def get_arg_spec(func):
        argspec = getfullargspec(func)
        return argspec.args, argspec.defaults or {}, argspec.annotations
else:
    def get_arg_spec(func):
        argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
        return argnames, func.func_defaults or {}, {}


def get_full_arg_spec(func):
    argnames, defaults, annotations = get_arg_spec(func)

    if defaults:
        defaults = dict(zip(reversed(argnames), reversed(defaults)))

    return list(argnames), defaults, annotations
