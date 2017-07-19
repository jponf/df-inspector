# -*- coding: utf-8 -*-

from .base import Environment, SExpression
from .exceptions import SymbolNotDefinedException


# Nested && Null Environments
##############################################################################

class NullEnvironment(Environment):
    """Null pattern applied to evaluation environments.

    If no parent environment is defined, it must automatically be
    NullEnvironment, which always fails on find(...) and its globalBind(...)
    refers to its child bind(...).
    """

    def __init__(self, child_env: Environment):
        super().__init__()
        self._child_env = child_env

    def bind(self, symbol: SExpression, value: SExpression) \
            -> Environment.BindSymbolHandler:
        raise NotImplementedError("NullEnvironment cannot bind symbols")

    def bind_global(self, symbol: SExpression, value: SExpression) \
            -> Environment.BindSymbolHandler:
        return self._child_env.bind(symbol, value)

    def find(self, symbol: SExpression) -> SExpression:
        raise SymbolNotDefinedException(
            "Symbol {0} is not defined".format(symbol))

    def extend(self) -> Environment:
        raise NotImplementedError("NullEnvironment is not extensible")


class NestedEnvironment(Environment):

    def __init__(self, parent_env: Environment=None):
        super().__init__()
        self._parent_env = parent_env or NullEnvironment(self)
        self._mapped_symbols = {}

    def bind(self, symbol: SExpression, value: SExpression) \
            -> Environment.BindSymbolHandler:
        self.check_locked(symbol)
        self._mapped_symbols[symbol] = value
        return Environment.BindSymbolHandler(self, symbol)

    def bind_global(self, symbol: SExpression, value: SExpression) \
            -> Environment.BindSymbolHandler:
        return self._parent_env.bind_global(symbol, value)

    def find(self, symbol: SExpression) -> SExpression:
        if symbol in self._mapped_symbols:
            return self._mapped_symbols[symbol]

        return self._parent_env.find(symbol)

    def extend(self) -> Environment:
        return NestedEnvironment(self)
