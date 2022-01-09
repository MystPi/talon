from errors import *


class SymbolTable:
    __func  = 'functions'
    __sym   = 'symbols'
    __local = 'locals'

    __table = {__func: {}, __sym: {}, __local: []}

    def __is_local(self):
        return len(self.__table[self.__local]) > 0

    def table(self):
        return self.__table

    def get_local_table(self):
        return self.__table[self.__local][-1]

    def set_local(self, flag):
        if flag:
            self.__table[self.__local].append({})
        else:
            self.__table[self.__local].pop()

    def get_sym(self, sym):
        if self.__is_local():
            for table in reversed(self.__table[self.__local]):
                if sym in table:
                    return table[sym]

        if sym in self.__table[self.__sym]:
            return self.__table[self.__sym][sym]

        raise SymbolNotFound(f'Symbol "{sym}" not found')

    def set_sym(self, sym, val, new=False):
        if new and self.__is_local() and sym in self.get_local_table():
            raise SymbolExists(f'Cannot recreate variable "{sym}"')
        elif new and sym in self.__table[self.__sym] and not self.__is_local():
            raise SymbolExists(f'Cannot recreate variable "{sym}"')
        elif new:
            if self.__is_local():
                self.get_local_table()[sym] = val
            else:
                self.__table[self.__sym][sym] = val
        else:
            if self.__is_local():
                for table in reversed(self.__table[self.__local]):
                    if sym in table:
                        table[sym] = val
                        return
                if sym in self.__table[self.__sym]:
                    self.__table[self.__sym][sym] = val
                    return
                raise SymbolNotFound(f'Symbol "{sym}" not found')
            else:
                if sym in self.__table[self.__sym]:
                    self.__table[self.__sym][sym] = val
                else:
                    raise SymbolNotFound(f'Symbol "{sym}" not found')

    def get_func(self, func):
        if func in self.__table[self.__func]:
            return self.__table[self.__func][func]

        raise FunctionNotFound(f'Function "{func}" not found')

    def set_func(self, func, val):
        if func in self.__table[self.__func]:
            raise FunctionExists(f'Function "{func}" cannot be redefined')
        
        self.__table[self.__func][func] = val