import re
import pprint


def array_parser(data):
    parse_list = []
    if data[0] != '[':
        return None
    data = data[1:].strip()
    while len(data) > 0:
        res = all_parsers(string_parser, number_parser, boolean_parser,
                          null_parser, array_parser, object_parser)(data)
        if res is None:
            return None
        parse_list.append(res[0])
        data = res[1].strip()
        res = comma_parser(data)
        if res is not None:
            data = res[1].strip()
        elif not res and data and data[0].strip() != ']':
            return None
        if data[0] == ']':
            return [parse_list, data[1:].strip()]


def boolean_parser(data):
    if data[0:4] == 'true':
        return [True, data[4:].strip()]
    elif data[0:5] == 'false':
        return [False, data[5:].strip()]


def colon_parser(data):
    if data[0] == ':':
        return [data[0], data[1:].lstrip()]


def comma_parser(data):
    if data and data[0] == ',':
        return [data[0], data[1:].strip()]


def null_parser(data):
    if data[0:4] == 'null':
        return [None, data[4:].strip()]


def number_parser(data):
    if not data:
        return None
    regex_find = re.findall("^(-?(?:[0-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)",
                            data)
    if not regex_find:
        return None
    pos = len(regex_find[0])
    try:
        return [int(regex_find[0]), data[pos:].strip()]
    except ValueError:
        try:
            return [float(regex_find[0]), data[pos:].strip()]
        except ValueError:
            return [regex_find, data[pos:].strip()]


def object_parser(data):
    parse_dict = {}
    if data[0] != '{':
        return None
    data = data[1:].strip()
    while data[0] != '}':
        res = string_parser(data)
        if res is None:
            return None
        id = res[0]
        res = colon_parser(res[1].strip())
        if res is None:
            return None
        res = all_parsers(string_parser, number_parser, boolean_parser,
                          null_parser, array_parser, object_parser)(res[1].strip())
        if res is None:
            return None
        parse_dict[id] = res[0]
        data = res[1].lstrip()
        res = comma_parser(data)
        if res:
            data = res[1].strip()
        elif data[0] != '}':
            return None
    return [parse_dict, data[1:]]


def string_parser(data):
    if data[0] == '"':
        data = data[1:]
        pos = data.find('"')
        while data[pos - 1] == '\\':
            pos += data[pos + 1:].find('"') + 1
        return [data[:pos], data[pos + 1:].strip()]


def all_parsers(*args):
    def specific_parser(data):
        for each_parser in args:
            res = each_parser(data)
            if res:
                return res
    return specific_parser


def main():
    with open("ex3.json", "r") as f:
        data = f.read()

    res = all_parsers(object_parser, array_parser)(data.strip())
    try:
        pprint.pprint(res[0])
    except TypeError:
        print(None)


if __name__ == '__main__':
    main()
