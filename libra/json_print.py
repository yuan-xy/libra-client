import json

class LibraEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.hex()
        return json.JSONEncoder.default(self, obj)

def json_dumps(obj):
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
    else:
        maps = vars(obj)
    return json.dumps(maps, cls=LibraEncoder, sort_keys=True, indent=4)

def json_print(obj):
    print(json_dumps(obj))
