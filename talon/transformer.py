import lark
from . import nodes


class Transformer(lark.Transformer):
    def start(self, args):
        return nodes.Instructions(args)

    def codeblock(self, args):
        return nodes.Instructions(args)

    def num(self, args):
        return nodes.Primitive(int(args[0]))

    def string(self, args):
        s = args[0][1:-1]
        s = bytes(s, "utf-8").decode("unicode_escape")
        return nodes.Primitive(s)

    def var(self, args):
        return nodes.Identifier(args[0])

    def true(self, args):
        return nodes.Primitive(True)

    def false(self, args):
        return nodes.Primitive(False)

    def list(self, args):
        return nodes.List(nodes.Instructions(args))

    def list_access(self, args):
        return nodes.ListAccess(args[0], args[1])

    def list_slice(self, args):
        return nodes.ListSlice(args[0], args[1], args[2])

    def list_assign(self, args):
        return nodes.ListAssign(nodes.Identifier(args[0].value), args[1], args[3])

    def range_incl(self, args):
        return nodes.Range(args[0], args[1], True)

    def range_excl(self, args):
        return nodes.Range(args[0], args[1], False)

    def neg(self, args):
        return nodes.UnaryOp('-', args[0])

    def abs(self, args):
        return nodes.UnaryOp('+', args[0])

    def not_(self, args):
        return nodes.UnaryOp('!', args[0])

    def add(self, args):
        return nodes.BinOp('+', args[0], args[1])

    def sub(self, args):
        return nodes.BinOp('-', args[0], args[1])

    def mul(self, args):
        return nodes.BinOp('*', args[0], args[1])

    def div(self, args):
        return nodes.BinOp('/', args[0], args[1])

    def mod(self, args):
        return nodes.BinOp('%', args[0], args[1])

    def pow(self, args):
        return nodes.BinOp('^', args[0], args[1])

    def eq(self, args):
        return nodes.BinOp('==', args[0], args[1])

    def neq(self, args):
        return nodes.BinOp('!=', args[0], args[1])

    def lt(self, args):
        return nodes.BinOp('<', args[0], args[1])

    def gt(self, args):
        return nodes.BinOp('>', args[0], args[1])

    def lteq(self, args):
        return nodes.BinOp('<=', args[0], args[1])

    def gteq(self, args):
        return nodes.BinOp('>=', args[0], args[1])

    def and_(self, args):
        return nodes.BinOp('&&', args[0], args[1])

    def or_(self, args):
        return nodes.BinOp('||', args[0], args[1])

    def assign_var(self, args):
        # Variable assignments don't have to have a value, like in `this x`.
        # If they don't, the value of the assignment is None.
        if args[1] is None:
            args[1] = nodes.Primitive(None)
        return nodes.Assignment(nodes.Identifier(args[0]), args[1], new=True)

    def assign_value(self, args):
        if args[1] == '=':
            return nodes.Assignment(nodes.Identifier(args[0]), args[2])
        else:
            return nodes.CompOp(nodes.Identifier(args[0]), args[1].value, args[2])

    def if_(self, args):
        return nodes.If(args[0], args[1])

    def if_else(self, args):
        return nodes.If(args[0], args[1], args[2])

    def for_(self, args):
        return nodes.For(nodes.Identifier(args[0].value), args[1], args[2])

    def while_(self, args):
        return nodes.While(args[0], args[1])

    def break_(self, args):
        return nodes.BreakInstruction()

    def return_(self, args):
        return nodes.ReturnInstruction(args[0])

    def fun_def(self, args):
        id = nodes.Identifier(args[0].value)
        id.is_func = True
        return nodes.Assignment(id, nodes.Function(args[1], args[2]), new=True)

    def fun_args(self, args):
        # args[0] can be None, meaning there are no arguments
        if args[0] is None:
            temp = None
        else:
            temp = [nodes.Identifier(arg.value) for arg in args]
        return nodes.Instructions(temp)

    def fun_call(self, args):
        id = nodes.Identifier(args[0].value)
        id.is_func = True
        return nodes.FunctionCall(id, nodes.Instructions(args[1:]))