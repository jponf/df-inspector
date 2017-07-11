# -*- coding: utf-8 -*-

import abc


# Interfaces
##############################################################################


class SExpression(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def eval(self, env: 'Environment') -> 'SExpression':
        raise NotImplementedError("Abstract method")


class CallableSExpression(SExpression):

    @abc.abstractmethod
    def process_arguments(self, env: 'Environment',
                          args: SExpression) -> SExpression:
        raise NotImplementedError("Abstract property")

    @abc.abstractclassmethod
    def apply(self, args: SExpression, env: 'Environment') -> SExpression:
        raise NotImplementedError("Abstract method")


class Environment(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def bind(self, symbol: SExpression, value: SExpression) -> None:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def bind_global(self, symbol: SExpression, value: SExpression) -> None:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def find(self, symbol: SExpression) -> SExpression:
        raise NotImplementedError("Abstract method")

    @abc.abstractclassmethod
    def extend(self) -> 'Environment':
        raise NotImplementedError("Abstract method")
