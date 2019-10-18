import json
from pygments import highlight, lexers, formatters
from canoser.base import Base

class LibraEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.hex()
        return json.JSONEncoder.default(self, obj)


def to_json_serializable(obj):
    if hasattr(obj, "json_print_fields"):
        maps = {}
        names = obj.json_print_fields()
        for name in names:
            components = name.split('.')
            if len(components) == 0:
                raise TypeError(f"{names} contain empty string.")
            if len(components) > 2 :
                raise TypeError(f"{names} has more than one level nested fields.")
            value = getattr(obj, components[0])
            if len(components) == 2:
                if isinstance(value, list):
                    value = [getattr(x, components[1]) for x in value]
                else:
                    value = getattr(x, components[1])
            maps[name] = value
        return maps
    elif hasattr(obj, "ListFields"):
        maps = {}
        fds = obj.ListFields()
        for fd, value in fds:
            maps[fd.name] = value
        return maps
    elif isinstance(obj, Base):
        return obj.to_json_serializable()
    else:
        return obj


def json_dumps(obj, sort_keys=False):
    to_dump = to_json_serializable(obj)
    return json.dumps(to_dump, cls=LibraEncoder, sort_keys=sort_keys, indent=4)

def json_print(obj, sort_keys=False, color=False, bgcolor=None):
    jsonstr = json_dumps(obj, sort_keys)
    # from pygments.styles import get_all_styles
    # styles = list(get_all_styles())
    if color:
        if bgcolor is not None:
            jsonstr = bgcolor + jsonstr + '\033[0m'
        else:
            term = formatters.Terminal256Formatter(style='fruity')
            jsonstr = highlight(jsonstr, lexers.JsonLexer(), term)
    print(jsonstr)
