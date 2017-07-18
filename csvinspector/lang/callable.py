# -*- coding: utf-8 -*-

import typing

from .base import CallableSExpression, Environment, SExpression
from .exceptions import EvaluationException
from .symbol import SYM_NIL
from .types import ConsCell


#
##############################################################################

class Function(CallableSExpression):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def info(self):
        return "Generic function information - Name: {0}".format(self._name)

    def process_arguments(self, args: SExpression,
                          env: Environment) -> SExpression:
        if SYM_NIL == args:
            return args
        if isinstance(args, ConsCell):
            cc_args = typing.cast(ConsCell, args)
            head = cc_args.car.eval(env)
            tail = self.process_arguments(cc_args.cdr, env)
            return ConsCell(head, tail)

        raise EvaluationException("Arguments must be NIL or a ConsCell")

    def eval(self, env: Environment) -> SExpression:
        return self

    def __str__(self):
        return "<function {0}>".format(self._name)


class Special(CallableSExpression):

    def __init__(self, name):
        self._name = name

    @property
    def info(self):
        return "Generic specials form information - Name: {0}".format(
            self._name)

    @property
    def name(self):
        return self._name

    def process_arguments(self, args: SExpression,
                          env: 'Environment') -> SExpression:
        return args

    def eval(self, env: Environment) -> SExpression:
        return self

    def __str__(self):
        return "<special {0}>".format(self._name)
