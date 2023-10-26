from common.utils import mandatory_key, optional_key


def mandatories(*keys):
    def decorate(func):
        def wrapper(View, *args, **kwargs):
            mandatory = dict()
            for key in keys:
                data = mandatory_key(View.request, key)
                mandatory[key] = data
            return func(View, m=mandatory, *args, **kwargs)

        return wrapper

    return decorate


def optionals(*keys):
    def decorate(func):
        def wrapper(View, *args, **kwargs):
            optional = dict()
            for arg in keys:
                for key, val in arg.items():
                    data = optional_key(View.request, key, val)
                    optional[key] = data
            return func(View, o=optional, *args, **kwargs)

        return wrapper

    return decorate
