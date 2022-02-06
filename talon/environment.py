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

    table.set_global('print', b(print))
    table.set_global('printf', b(printf))
    table.set_global('printc', b(printc))
    table.set_global('getstr', b(input))
    table.set_global('format', b(format))
    table.set_global('colored', b(colored))
    table.set_global('import', b(import_))

    # Math
    table.set_global('int', b(int))
    table.set_global('float', b(float))
    table.set_global('round', b(round))
    table.set_global('log', b(math.log))
    table.set_global('sqrt', b(math.sqrt))
    table.set_global('sin', b(math.sin))
    table.set_global('cos', b(math.cos))
    table.set_global('tan', b(math.tan))
    table.set_global('asin', b(math.asin))
    table.set_global('acos', b(math.acos))
    table.set_global('atan', b(math.atan))
    table.set_global('atan2', b(math.atan2))
    table.set_global('random', b(random.random))
    table.set_global('randomint', b(random.randint))

    # Strings
    table.set_global('str', b(str))
    table.set_global('len', b(len))
    table.set_global('ord', b(ord))
    table.set_global('chr', b(chr))
    table.set_global('lower', b(str.lower))
    table.set_global('upper', b(str.upper))
    table.set_global('startswith', b(str.startswith))
    table.set_global('endswith', b(str.endswith))
    table.set_global('replace', b(str.replace))
    table.set_global('split', b(lambda s, d: s.split(d)))

    # Lists
    table.set_global('list', b(list))
    table.set_global('append', b(lambda l, e: l.append(e)))
    table.set_global('pop', b(lambda l: l.pop()))
    table.set_global('remove', b(lambda l, e: l.remove(e)))
    table.set_global('reverse', b(lambda l: l.reverse()))
    table.set_global('sort', b(lambda l: l.sort()))
