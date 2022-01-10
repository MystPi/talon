from lark import Lark, UnexpectedInput
from transformer import Transformer
import pickle, os, tinted, environment


def parse(code):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'syntax.lark'), 'r') as f:
        syntax = f.read()
    parser = Lark(syntax)
    try:
        return parser.parse(code)
    except UnexpectedInput as e:
        print(tinted.tint(f'[red][bold]Syntax error[/][/] at [blue][bold]line[/][/] {e.line}, [blue][bold]column[/][/] {e.column}\n\n{e.get_context(code)}'))
        exit(1)


def transform(tree):
    transformer = Transformer()
    return transformer.transform(tree)


def execute(transformed):
    environment.define_builtins()
    return transformed.eval()


def talon(inputfile: str, compile=False, outputfile=None):
    if inputfile.endswith('.tal'):
        with open(inputfile, 'r') as input:
            code = input.read()
            temp = transform(parse(code))
    elif inputfile.endswith('.talc'):
        with open(inputfile, 'rb') as f:
            temp = pickle.load(f)
    try:
        if compile:
            if outputfile is None:
                outputfile = inputfile + 'c'
            else:
                if not outputfile.endswith('.talc'):
                    outputfile += '.talc'
            with open(outputfile, 'wb') as f:
                pickle.dump(temp, f)
        else:
            execute(temp)

    except Exception as e:
        print(tinted.tint(f'[red][bold]{str(e.__class__.__name__)}[/][/]: {str(e)}'))
        exit(1)


def main():
    import sys
    if len(sys.argv) == 2:
        talon(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == '-c':
        talon(sys.argv[2], compile=True)
    elif len(sys.argv) == 5 and sys.argv[1] == '-c' and sys.argv[3] == '-o':
        talon(sys.argv[2], compile=True, outputfile=sys.argv[4])
    else:
        print('Usage: talon [-c] <input.tal[c]> [-o <output.talc>]')


if __name__ == '__main__':
    main()