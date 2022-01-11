import math, random, re, tinted
from . import nodes, talon


def format(string, list):
    def repl(match):
        if match[0][0:2] == '%%':
            return match[0][1:]
        return str(list[int(match[1])])

    string = re.sub(r'%?%(-?\d+)', repl, string)
    return string


def colored(string):
    return tinted.tint(string)


def printf(string, list):
    print(format(string, list))


def printc(string):
    print(colored(string))


def import_(name):
    with open(name, 'r') as f:
        talon.transform(talon.parse(f.read())).eval()


def define_builtins():
    table = nodes.symbols
    b = nodes.BuiltinFunc

    table.set_func('print', b(print))
    table.set_func('printf', b(printf))
    table.set_func('printc', b(printc))
    table.set_func('getstr', b(input))
    table.set_func('format', b(format))
    table.set_func('colored', b(colored))
    table.set_func('import', b(import_))

    # Math
    table.set_func('int', b(int))
    table.set_func('float', b(float))
    table.set_func('round', b(round))
    table.set_func('log', b(math.log))
    table.set_func('sqrt', b(math.sqrt))
    table.set_func('sin', b(math.sin))
    table.set_func('cos', b(math.cos))
    table.set_func('tan', b(math.tan))
    table.set_func('asin', b(math.asin))
    table.set_func('acos', b(math.acos))
    table.set_func('atan', b(math.atan))
    table.set_func('atan2', b(math.atan2))
    table.set_func('random', b(random.random))
    table.set_func('randomint', b(random.randint))

    # Strings
    table.set_func('str', b(str))
    table.set_func('len', b(len))
    table.set_func('ord', b(ord))
    table.set_func('chr', b(chr))
    table.set_func('lower', b(str.lower))
    table.set_func('upper', b(str.upper))
    table.set_func('startswith', b(str.startswith))
    table.set_func('endswith', b(str.endswith))
    table.set_func('replace', b(str.replace))
    table.set_func('split', b(str.split))

    # Lists
    table.set_func('list', b(list))
    table.set_func('append', b(lambda l, e: l.append(e)))
    table.set_func('pop', b(lambda l: l.pop()))
    table.set_func('push', b(lambda l, e: l.push(e)))
    table.set_func('remove', b(lambda l, e: l.remove(e)))
    table.set_func('reverse', b(lambda l: l.reverse()))
    table.set_func('sort', b(lambda l: l.sort()))
