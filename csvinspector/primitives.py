# -*- coding: utf-8 -*-

import itertools
import logging
import typing

from .lang import listops
from .lang.base import Environment, SExpression
from .lang.callable import Function, Special
from .lang.exceptions import EvaluationException, ArgumentsException
from .lang.symbol import SYM_NIL, SYM_FALSE, SYM_TRUE, Symbol
from .lang.types import BaseNumber, DataFrame, Integer, String

from .lang import arithmetic

#
##############################################################################

_log = logging.getLogger("predicates")


# Basic functions
##############################################################################

class FunctionCompose(Function):

    def apply(self, args: SExpression, env: Environment) -> SExpression:
        check_exact_number_of_arguments(args, 2, self.name)
        match_types(args, itertools.repeat(Function))

        class ComposedFunction(Function):

            def __init__(self, f: Function, g: Function):
                super().__init__("{0}∘{1}".format(f.name, g.name))
                self._f = f
                self._g = g

            def apply(self, a: SExpression, e: Environment) -> SExpression:
                g_res = self._g.apply(self._g.process_arguments(a, e), e)
                f_args = listops.from_args(g_res)
                return self._f.apply(self._g.process_arguments(f_args, e), e)

        return ComposedFunction(typing.cast(Function, listops.nth(args, 0)),
                                typing.cast(Function, listops.nth(args, 1)))


class FunctionPrint(Function):

    def apply(self, args: SExpression, env: Environment) -> SExpression:
        print(*list(listops.iterate(args)))
        return SYM_NIL


# Arithmetic Functions
##############################################################################

class FunctionAdd(Function):

    def apply(self, args: SExpression, env: Environment) -> SExpression:
        match_types(args, itertools.repeat(BaseNumber))
        base = Integer(0)
        for arg in listops.iterate(args):
            base = arithmetic.add(base, arg)
        return base


class FunctionSubtract(Function):

    def apply(self, args: SExpression, env: Environment) -> SExpression:
        match_types(args, itertools.repeat(BaseNumber))
        if SYM_NIL == args:
            return Integer(0)
        values = listops.iterate(args)
        base = next(values)
        for v in values:
            base = arithmetic.subtract(base, v)
        return base


class FunctionMultiply(Function):

    def apply(self, args: SExpression, env: Environment) -> SExpression:
        match_types(args, itertools.repeat(BaseNumber))
        base = Integer(1)
        for arg in listops.iterate(args):
            base = arithmetic.multiply(base, arg)
        return base


class FunctionDivide(Function):

    def apply(self, args: SExpression, env: Environment) -> SExpression:
        match_types(args, itertools.repeat(BaseNumber))
        try:
            values = listops.iterate(args)
            base = Integer(1) if SYM_NIL == args else next(values)
            for v in values:
                base = arithmetic.divide(base, v)
            return base
        except ZeroDivisionError:
            raise EvaluationException("Trying to divide by 0!")


# Data frame IO functions
##############################################################################

class FunctionReadCSV(Function):

    def apply(self, args: SExpression, env: Environment) -> SExpression:
        check_exact_number_of_arguments(args, 1, self.name)
        match_types(args, [String])

        csv_path = typing.cast(String, listops.nth(args, 0))
        return DataFrame.from_csv_file(csv_path.value)


# Special symbols
##############################################################################

class SpecialLet(Special):

    def apply(self, args: SExpression, env: Environment) -> SExpression:
        check_exact_number_of_arguments(args, 2, self.name)
        sym = listops.nth(args, 0)
        if not isinstance(sym, Symbol):
            raise ArgumentsException("{0}: first argument must be a symbol")

        env.bind(sym, listops.nth(args, 1).eval(env))
        return SYM_NIL


# Utilities
##############################################################################

def match_types(args_list: SExpression, types: [type]):
    args = listops.iterate(args_list)
    for i, (arg, t) in enumerate(zip(args, types)):
        if not isinstance(arg, t):
            raise ArgumentsException("Argument index {0} expected type {1}"
                                     " but got {2}".format(i, t, type(arg)))


def check_exact_number_of_arguments(args, expected_len, symbol_name):
    l = listops.length(args)
    if l != expected_len:
        raise ArgumentsException("{0} expected {1} but received {2}".format(
            symbol_name, expected_len, l))


# Module functions
##############################################################################

def load_all(env: Environment):
    _log.debug("Loading all system primitives")
    load_default_symbols(env)
    load_basic_functions(env)
    load_arithmetic_functions(env)
    load_data_frame_io_functions(env)
    load_special_operations(env)


def load_default_symbols(env: Environment):
    _log.debug("Loading default symbols: %s, %s and %s",
               str(SYM_NIL), str(SYM_FALSE), str(SYM_TRUE))
    env.bind_global(SYM_NIL, SYM_NIL)
    env.bind_global(SYM_FALSE, SYM_FALSE)
    env.bind_global(SYM_TRUE, SYM_TRUE)


def load_basic_functions(env: Environment):
    _log.debug("Loading basic functions")
    env.bind_global(Symbol("."), FunctionCompose("."))
    env.bind_global(Symbol("print"), FunctionPrint("print"))


def load_arithmetic_functions(env: Environment):
    _log.debug("Loading arithmetic functions")
    env.bind_global(Symbol("+"), FunctionAdd("+"))
    env.bind_global(Symbol("-"), FunctionSubtract("-"))
    env.bind_global(Symbol("*"), FunctionMultiply("*"))
    env.bind_global(Symbol("/"), FunctionDivide("/"))


def load_data_frame_io_functions(env: Environment):
    _log.debug("Loading data frame IO functions")
    env.bind_global(Symbol("read_csv"), FunctionReadCSV("read_csv"))


def load_special_operations(env: Environment):
    _log.debug("Loading special operations")
    env.bind_global(Symbol("let"), SpecialLet("let"))
