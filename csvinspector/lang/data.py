# -*- coding: utf-8 -*-


import abc

from .exceptions import EvaluationException, \
    SymbolNotDefinedException


# Interfaces
##############################################################################


class SExpression(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def eval(self, env: 'Environment') -> 'SExpression':
        raise NotImplementedError("Abstract method")


class CallableSExpression(SExpression):

    @property
    @abc.abstractmethod
    def evaluation_strategy(self):
        raise NotImplementedError("Abstract property")

    @abc.abstractclassmethod
    def apply(self, env: 'Environment', args: 'SExpression'):
        raise NotImplementedError("Abstract method")


class Environment(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def bind(self, symbol: 'Symbol', value: SExpression) -> None:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def bind_global(self, symbol: 'Symbol', value: SExpression) -> None:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def find(self, symbol: 'Symbol') -> SExpression:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def extend(self) -> 'Environment':
        raise NotImplementedError("Abstract method")


# Nested && Null Environments
##############################################################################

class NestedEnvironment(Environment):

    def __init__(self, parent_env: Environment):
        self._parent_env = parent_env
        self._mapped_symbols = {}

    def bind(self, symbol: 'Symbol', value: SExpression) -> None:
        self._mapped_symbols[symbol] = value

    def bind_global(self, symbol: 'Symbol', value: SExpression) -> None:
        self._parent_env.bind_global(symbol, value)

    def find(self, symbol: 'Symbol') -> SExpression:
        if symbol in self._mapped_symbols:
            return self._mapped_symbols[symbol]

        return self._parent_env.find(symbol)

    def extend(self) -> Environment:
        return NestedEnvironment(self)


class NullEnvironment(Environment):
    """Null pattern applied to evaluation environments.

    If no parent environment is defined, it must automatically be
    NullEnvironment, which always fails on find(...) and its globalBind(...)
    refers to its child bind(...).
    """

    def __init__(self, nested_env: NestedEnvironment):
        self._nested_env = nested_env

    def bind(self, symbol: 'Symbol', value: SExpression) -> None:
        raise NotImplementedError("NullEnvironment cannot bint symbols")

    def bind_global(self, symbol: 'Symbol', value: SExpression) -> None:
        return self._nested_env.bind(symbol, value)

    def find(self, symbol: 'Symbol') -> SExpression:
        raise SymbolNotDefinedException(
            "Symbol {0} is not defined".format(symbol))

    def extend(self) -> Environment:
        raise NotImplementedError("NullEnvironment is not extensible")


# Symbol
##############################################################################

class Symbol(SExpression):

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


SYM_NIL = Symbol('nil')


# ConsCell
##############################################################################

class ConsCell(SExpression):

    def __init__(self, car: SExpression, cdr: SExpression):
        assert isinstance(car, SExpression), "expected SExpression"
        assert isinstance(cdr, SExpression), "expected SExpression"
        self.car = car
        self.cdr = cdr

    def eval(self, env: Environment):
        if isinstance(self.car, CallableSExpression):
            self.car.apply(env, self.car.evaluation_strategy(self.cdr))
        else:
            raise EvaluationException("Error evaluating {0}, which is not a"
                                      " callable s-expression")

    def __eq__(self, other):
        return isinstance(other, ConsCell) and self.car == other.car \
            and self.cdr == other.cdr

    def __hash__(self):
        return 31 * hash(self.car) + hash(self.cdr)

    def __iter__(self):
        s_expr = self.car
        while s_expr != SYM_NIL:
            yield s_expr
            s_expr = self.cdr

    def __repr__(self):
        return "ConsCell(car={0}, cdr={1})".format(repr(self.car),
                                                   repr(self.cdr))

    def __str__(self):
        return "({0})".format(", ".join(map(str, self)))
