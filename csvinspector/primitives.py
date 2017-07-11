# -*- coding: utf-8 -*-

import logging

from .lang import listops
from .lang.base import Environment, SExpression
from .lang.callable import Function, Special
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

class SpecialLet(Special):

    def apply(self, args: SExpression, env: 'Environment') -> SExpression:
        check_exact_number_of_arguments(args, 2, self.name)
        sym = listops.nth(args, 0)
        if not isinstance(sym, Symbol):
            raise EvaluationException("{0}: first argument must be a symbol")

        env.bind(sym, listops.nth(args, 1).eval(env))
        return SYM_NIL


def check_exact_number_of_arguments(args, expected_len, symbol_name):
    l = listops.len(args)
    if l != expected_len:
        raise EvaluationException("{0} expected {1} but received {2}".format(
            symbol_name, expected_len, l))


# Module functions
##############################################################################

def load_all(env: Environment):
    _log.debug("Loading all system primitives")
    load_default_symbols(env)
    load_arithmetic_functions(env)
    load_special_operations(env)


def load_default_symbols(env: Environment):
    _log.debug("Loading default symbols: %s, %s and %s",
               str(SYM_NIL), str(SYM_FALSE), str(SYM_TRUE))
    env.bind_global(SYM_NIL, SYM_NIL)
    env.bind_global(SYM_FALSE, SYM_FALSE)
    env.bind_global(SYM_TRUE, SYM_TRUE)


def load_arithmetic_functions(env: Environment):
    _log.debug("Loading arithmetic functions")
    env.bind_global(Symbol("+"), FunctionAdd("+"))
    env.bind_global(Symbol("-"), FunctionSubtract("-"))
    env.bind_global(Symbol("*"), FunctionMultiply("*"))
    env.bind_global(Symbol("/"), FunctionDivide("/"))


def load_special_operations(env: Environment):
    _log.debug("Loading special operations")
    env.bind_global(Symbol("let"), SpecialLet("let"))
