import lupa
from functools import wraps


def check_is_lua_table(val):
    if lupa.lua_type(val) == "table":
        val = dict(val.items())
    if type(val) in [list, tuple]:
        vals = []
        for i in val:
            _val = check_is_lua_table(i)
            vals.append(_val)
        val = vals
    elif type(val) == dict:
        vals = {}
        for k in val.keys():
            _val = check_is_lua_table(val[k])
            vals[k] = _val
        val = vals
    return val


def unpacks_lua_table(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = list(args)
        for i in range(len(args)):
            args[i] = check_is_lua_table(args[i])
        for k, v in kwargs.items():
            kwargs[k] = check_is_lua_table(v)
        return func(*args, **kwargs)

    return wrapper
