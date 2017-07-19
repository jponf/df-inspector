# -*- coding: utf-8 -*-

import abc

from .exceptions import SymbolLockedException


# Interfaces
##############################################################################


class SExpression(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def info(self) -> str:
        """String that explains what the s-expression is:
            * how it behaves
            * what is its value
            * ...
        """
        raise NotImplementedError("Abstract property")

    @abc.abstractmethod
    def eval(self, env: 'Environment') -> 'SExpression':
        raise NotImplementedError("Abstract method")


class CallableSExpression(SExpression):

    @abc.abstractmethod
    def process_arguments(self, args: SExpression,
                          env: 'Environment') -> SExpression:
        raise NotImplementedError("Abstract property")

    @abc.abstractclassmethod
    def apply(self, args: SExpression, env: 'Environment') -> SExpression:
        raise NotImplementedError("Abstract method")


class Environment(metaclass=abc.ABCMeta):

    class BindSymbolHandler(object):

        def __init__(self, env: 'Environment', symbol: SExpression):
            self._env = env
            self._sym = symbol

        def lock(self):
            self._env.lock(self._sym)

    def __init__(self):
        self._locked = set()

    def lock(self, symbol: SExpression):
        self._locked.add(symbol)

    def check_locked(self, symbol: SExpression):
        if symbol in self._locked:
            raise SymbolLockedException("Symbol {0} cannot be defined".format(
                symbol))

    @abc.abstractclassmethod
    def bind(self, symbol: SExpression, value: SExpression) \
            -> BindSymbolHandler:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def bind_global(self, symbol: SExpression, value: SExpression) \
            -> BindSymbolHandler:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def find(self, symbol: SExpression) -> SExpression:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def extend(self) -> 'Environment':
        raise NotImplementedError("Abstract method")
