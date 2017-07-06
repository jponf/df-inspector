# -*- coding: utf-8 -*-


import abc

from .exceptions import SymbolNotDefinedExcepion


# Interfaces
##############################################################################


class Expression(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def eval(self, env: Environment):
        raise NotImplementedError("Abstract method")


class Environment(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def bind(self, symbol: Symbol, value) -> None:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def bind_global(self, symbol: Symbol, value) -> None:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def find(self, symbol: Symbol) -> Expression:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def extend(self):
        raise NotImplementedError("Abstract method")


# Nested && Null Environments
##############################################################################

class NestedEnvironment(Environment):

    def __init__(self, parent_env: Environment):
        self._parent_env = parent_env
        self._mapped_symbols = {}

    def bind(self, symbol: Symbol, value) -> None:
        self._mapped_symbols[symbol] = value

    def bind_global(self, symbol: Symbol, value) -> None:
        self._parent_env.bind_global(symbol, value)

    def find(self, symbol: Symbol) -> Expression:
        if symbol in self._mapped_symbols:
            return self._mapped_symbols[symbol]

        return self._parent_env.find(symbol)

    def extend(self):
        return NestedEnvironment(self)


class NullEnvironment(Environment):
    """Null pattern applied to evaluation environments.

    If no parent environment is defined, it must automatically be
    NullEnvironment, which always fails on find(...) and its globalBind(...)
    refers to its child bind(...).
    """

    def __init__(self, nested_env: NestedEnvironment):
        self._nested_env = nested_env

    def bind(self, symbol: Symbol, value) -> None:
        raise NotImplementedError("NullEnvironment cannot bint symbols")

    def bind_global(self, symbol: Symbol, value) -> None:
        return self._nested_env.bind(symbol, value)

    def find(self, symbol: Symbol) -> Expression:
        raise SymbolNotDefinedExcepion(
            "Symbol {0} is not defined".format(symbol))

    def extend(self):
        return NotImplementedError("NullEnvironment is not extensible")


# Symbol
##############################################################################

class Symbol(Expression):

    def __init__(self, name: str):
        self.name = name

    def eval(self, env: Environment):
        return env.find(self)

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "Symbol(name={0})".format(self.name)

    def __str__(self):
        return self.name
