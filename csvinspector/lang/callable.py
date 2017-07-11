# -*- coding: utf-8 -*-

import typing

from .base import CallableSExpression, Environment, SExpression
from .exceptions import EvaluationException
from .symbol import SYM_NIL
from .types import ConsCell


# Function
##############################################################################

class Function(CallableSExpression):

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
