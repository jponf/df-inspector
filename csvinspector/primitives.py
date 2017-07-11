# -*- coding: utf-8 -*-

import logging

from .lang import listops
from .lang.base import Environment, SExpression
from .lang.callable import Function
from .lang.exceptions import EvaluationException
from .lang.symbol import SYM_NIL, SYM_FALSE, SYM_TRUE, Symbol
from .lang.types import Integer

from .lang import arithmetic

#
##############################################################################

_log = logging.getLogger("predicates")


# Functions
##############################################################################

class FunctionAdd(Function):

    def apply(self, args: SExpression, env: 'Environment') -> SExpression:
        base = Integer(0)
        for arg in listops.iterate(args):
            base = arithmetic.add(base, arg)
        return base


class FunctionSubtract(Function):

    def apply(self, args: SExpression, env: 'Environment') -> SExpression:
        if SYM_NIL == args:
            return Integer(0)

        values = listops.iterate(args)
        base = next(values)
        for v in values:
            base = arithmetic.subtract(base, v)
        return base


class FunctionMultiply(Function):

    def apply(self, args: SExpression, env: 'Environment') -> SExpression:
        base = Integer(1)
        for arg in listops.iterate(args):
            base = arithmetic.multiply(base, arg)
        return base


class FunctionDivide(Function):

    def apply(self, args: SExpression, env: 'Environment') -> SExpression:
        if SYM_NIL == args:
            return Integer(1)
        try:
            values = listops.iterate(args)
            base = next(values)
            for v in values:
                base = arithmetic.divide(base, v)
            return base
        except ZeroDivisionError:
            raise EvaluationException("Trying to divide by 0!")


# Special symbols
##############################################################################


# Module functions
##############################################################################

def load_all(env: Environment):
    _log.debug("Loading all system primitives")
    load_default_symbols(env)
    load_arithmetic_functions(env)


def load_default_symbols(env: Environment):
    _log.debug("Loading default symbols: %s, %s and %s",
               str(SYM_NIL), str(SYM_FALSE), str(SYM_TRUE))
    env.bind_global(SYM_NIL, SYM_NIL)
    env.bind_global(SYM_FALSE, SYM_FALSE)
    env.bind_global(SYM_TRUE, SYM_TRUE)


def load_arithmetic_functions(env: Environment):
    _log.debug("Loading arithmetic functions")
    env.bind_global(Symbol("+"), FunctionAdd())
    env.bind_global(Symbol("-"), FunctionSubtract())
    env.bind_global(Symbol("*"), FunctionMultiply())
    env.bind_global(Symbol("/"), FunctionDivide())
