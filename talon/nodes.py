from types import LambdaType
from . import symbols as s
import operator

symbols = s.SymbolTable()


class Instructions:
    def __init__(self, children):
        if children is None or children == [None]:
            children = []
        self.children = children

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __repr__(self):
        return f'<Instructions {self.children!r}>'

    def eval(self):
        ret = []
        for node in self:
            if isinstance(node, ExitInstruction):
                return node

            result = node.eval()

            if isinstance(result, ExitInstruction):
                return result
            elif result is not None:
                ret.append(result)

        return ret


class BaseExpr:
    def eval(self):
        return NotImplementedError()


class CallableExpr:
    def eval(self):
        return NotImplementedError()


class ExitInstruction(BaseExpr):
    def __iter__(self):
        return []

    def eval(self):
        pass


class ReturnInstruction(ExitInstruction):
    def __init__(self, expression: BaseExpr):
        self.expression = expression

    def __repr__(self):
        return f'<ReturnInstruction expression={self.expression!r}>'

    def eval(self):
        return full_eval(self.expression)


class BreakInstruction(ExitInstruction):
    def __repr__(self):
        return f'<BreakInstruction>'

    def eval(self):
        return None


def full_eval(expression: BaseExpr):
    while isinstance(expression, BaseExpr):
        expression = expression.eval()

    return expression


class Primitive(BaseExpr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<Primitive {self.value!r} ({self.value.__class__.__name__})>'

    def eval(self):
        return self.value


class Identifier(BaseExpr):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Identifier {self.name}>'

    def assign(self, value, new=False):
        symbols.set_sym(self.name, value, new=new)

    def eval(self):
        return symbols.get_sym(self.name)


class List(BaseExpr):
    def __init__(self, values: Instructions):
        self.values = values

    def __repr__(self):
        return f'<List length={len(self.values)} items={self.values!r}>'

    def eval(self):
        return self.values.eval()


class ListAccess(BaseExpr):
    def __init__(self, list: BaseExpr, index: BaseExpr):
        self.list = list
        self.index = index

    def __repr__(self):
        return f'<List list={self.list!r} index={self.index!r}>'

    def eval(self):
        return self.list.eval()[self.index.eval()]


class ListAssign(BaseExpr):
    __ops = {
        '+=': operator.iadd,
        '-=': operator.isub,
        '*=': operator.imul,
        '/=': operator.itruediv,
        '%=': operator.imod,
        '^=': operator.ipow
    }

    def __init__(self, list: BaseExpr, index: BaseExpr, op: BaseExpr, value: BaseExpr):
        self.list = list
        self.index = index
        self.op = op
        self.value = value

    def __repr__(self):
        return f'<List list={self.list!r} index={self.index!r} op={self.op!r} value={self.value!r}>'

    def eval(self):
        list = self.list.eval()
        index = self.index.eval()
        value = self.value.eval()
        if self.op == '=':
            list[index] = value
        else:
            list[index] = self.__ops[self.op](list[index], value)


class ListSlice(BaseExpr):
    def __init__(self, list: BaseExpr, start: BaseExpr, end: BaseExpr):
        self.list = list
        self.start = start
        self.end = end

    def __repr__(self):
        return f'<ListSlice list={self.list!r} start={self.start!r} end={self.end!r}>'

    def eval(self):
        if self.start is not None and self.end is not None:
            return self.list.eval()[self.start.eval():self.end.eval()]
        elif self.start is None and self.end is not None:
            return self.list.eval()[:self.end.eval()]
        elif self.start is not None and self.end is None:
            return self.list.eval()[self.start.eval():]
        else:
            return self.list.eval()


class Range(BaseExpr):
    def __init__(self, start: BaseExpr, end: BaseExpr, inclusive: bool):
        self.start = start
        self.end = end
        self.inclusive = inclusive

    def __repr__(self):
        return f'<Range start={self.start!r} end={self.end!r} inclusive={self.inclusive}>'

    def eval(self):
        if self.inclusive:
            return list(range(self.start.eval(), self.end.eval() + 1))
        else:
            return list(range(self.start.eval(), self.end.eval()))


class Assignment(BaseExpr):
    def __init__(self, identifier: Identifier, value: BaseExpr, new=False):
        self.identifier = identifier
        self.value = value
        self.new = new

    def __repr__(self):
        return f'<Assignment new={self.new} identifier={self.identifier!r} value={self.value!r}>'

    def eval(self):
        self.identifier.assign(self.value.eval(), new=self.new)


class CompOp(BaseExpr):
    __ops = {
        '+=': operator.iadd,
        '-=': operator.isub,
        '*=': operator.imul,
        '/=': operator.itruediv,
        '%=': operator.imod,
        '^=': operator.ipow
    }

    def __init__(self, identifier: Identifier, op: str, value: BaseExpr):
        self.identifier = identifier
        self.op = op
        self.value = value

    def __repr__(self):
        return f'<CompOp identifier={self.identifier!r} op={self.op!r} value={self.value!r}>'

    def eval(self):
        left = self.identifier.eval()
        right = self.value.eval()

        try:
            self.identifier.assign(self.__ops[self.op](left, right))
        except TypeError:
            raise TypeError(f'Type error: ({left}: {left.__class__.__name__}) {self.op} ({right}: {right.__class__.__name__}) is not allowed')


class BinOp(BaseExpr):
    __ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': operator.pow,
        '%': operator.mod,
        '==': operator.eq,
        '!=': operator.ne,
        '<': operator.lt,
        '>': operator.gt,
        '<=': operator.le,
        '>=': operator.ge,
        '&&': lambda a, b: a.eval() and b.eval(),
        '||': lambda a, b: a.eval() or b.eval()
    }

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f'<BinOp op={self.op!r} left={self.left!r} right={self.right!r}>'

    def eval(self):
        left = None
        right = None

        try:
            op = self.__ops[self.op]

            if isinstance(op, LambdaType):
                return op(self.left, self.right)

            left = self.left.eval()
            right = self.right.eval()

            return op(left, right)
        except TypeError:
            # TODO: custom error
            raise TypeError(f'Type error: ({left}: {left.__class__.__name__}) {self.op} ({right}: {right.__class__.__name__}) is not allowed')


class UnaryOp(BaseExpr):
    __ops = {
        '-': operator.neg,
        '+': operator.abs,
        '!': operator.not_
    }

    def __init__(self, op, value: BaseExpr):
        self.op = op
        self.value = value

    def __repr__(self):
        return f'<UnaryOp op={self.op!r} value={self.value!r}>'

    def eval(self):
        return self.__ops[self.op](self.value.eval())


class If(BaseExpr):
    def __init__(self, condition: BaseExpr, true_branch: Instructions, false_branch: Instructions = None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __repr__(self):
        return f'<If condition={self.condition!r} true_branch={self.true_branch!r} false_branch={self.false_branch!r}>'

    def eval(self):
        if self.condition.eval():
            return self.true_branch.eval()
        elif self.false_branch is not None:
            return self.false_branch.eval()


class For(BaseExpr):
    def __init__(self, var: Identifier, sequence: BaseExpr, body: Instructions):
        self.var = var
        self.sequence = sequence
        self.body = body

    def __repr__(self):
        return f'<For var={self.var!r} sequence={self.sequence!r} body={self.body!r}>'

    def eval(self):
        for value in self.sequence.eval():
            self.var.assign(value)
            val = self.body.eval()
            if isinstance(val, ReturnInstruction):
                return val
            elif isinstance(val, BreakInstruction):
                break


class While(BaseExpr):
    def __init__(self, condition: BaseExpr, body: Instructions):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f'<While condition={self.condition!r} body={self.body!r}>'

    def eval(self):
        while self.condition.eval():
            val = self.body.eval()
            if isinstance(val, ReturnInstruction):
                return val
            elif isinstance(val, BreakInstruction):
                break


class Function(CallableExpr):
    def __init__(self, params: Instructions, body: Instructions):
        self.params = params
        self.body = body

    def __repr__(self):
        # TODO: Improve string representation
        return f'<Function params={len(self.params)!r}>'

    def eval(self, args=None):
        if args is None:
            return self

        symbols.set_local(True)

        for key, value in args.items():
            symbols.set_sym(key, value, new=True)

        try:
            result = self.body.eval()

            if isinstance(result, ReturnInstruction):
                return result.eval()
        finally:
            symbols.set_local(False)

        return None


class FunctionCall(BaseExpr):
    def __init__(self, value, params: Instructions):
        self.value = value
        self.params = params

    def __repr__(self):
        return f'<Function call value={self.value!r} called_with_params={len(self.params)!r}>'

    def __builtin_func(self):
        func = self.value.eval()
        args = []

        for param in self.params:
            args.append(full_eval(param))

        return func.eval(args)

    def __user_func(self):
        func = self.value.eval()
        args = {}

        length1 = len(func.params)
        length2 = len(self.params)

        if length1 != length2:
            raise NameError(f'Invalid amount of args for "{self.value}". Got {length2}, expected {length1}')

        for param, value in zip(func.params, self.params):
            args[param.name] = full_eval(value)

        return func.eval(args)

    def eval(self):
        func = self.value.eval()

        if not isinstance(func, CallableExpr):
            raise TypeError(f'{self.value!r} is not a function')

        if isinstance(func, BuiltinFunc):
            return self.__builtin_func()

        return self.__user_func()


class BuiltinFunc(CallableExpr):
    def __init__(self, func):
        self.func = func

    def __repr__(self):
        return f'<Builtin func {self.func!r}>'

    def eval(self, args=None):
        if args is None:
            return self

        return self.func(*args)