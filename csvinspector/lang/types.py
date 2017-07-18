# -*- coding: utf-8 -*-

import abc
import pandas as pd
import typing

from .base import CallableSExpression, Environment, SExpression
from .exceptions import EvaluationException
from .symbol import SYM_NIL


# Numbers
##############################################################################

class BaseNumber(metaclass=abc.ABCMeta):

    @property
    @abc.abstractclassmethod
    def value(self):
        raise NotImplementedError("Abstract property")


class Integer(BaseNumber, SExpression):

    def __init__(self, value: int):
        self._value = int(value)

    @property
    def info(self) -> str:
        return "Integer expression with value {0}".format(self._value)

    @property
    def value(self):
        return self._value

    def eval(self, env: Environment) -> SExpression:
        return self

    def __eq__(self, other):
        return isinstance(other, Integer) and self.value == other.value

    def __hash__(self):
        return hash(self._value)

    def __repr__(self):
        return "Integer({0})".format(self._value)

    def __str__(self):
        return str(self._value)


class Real(BaseNumber, SExpression):

    def __init__(self, value: float):
        self._value = float(value)

    @property
    def info(self) -> str:
        return "Real expression with value {0}".format(self._value)

    @property
    def value(self):
        return self._value

    def eval(self, env: Environment) -> SExpression:
        return self

    def __eq__(self, other):
        return isinstance(other, Real) and self.value == other.value

    def __hash__(self):
        return hash(self._value)

    def __repr__(self):
        return "Integer({0})".format(self._value)

    def __str__(self):
        return str(self._value)


# String
##############################################################################

class String(SExpression):

    def __init__(self, value: str):
        self._value = value

    @property
    def info(self) -> str:
        return 'String expression: "{0}"'.format(self._value)

    @property
    def value(self):
        return self._value

    def eval(self, env: Environment) -> SExpression:
        return self

    def __eq__(self, other):
        return isinstance(other, String) and self.value == other.value

    def __hash__(self):
        return hash(self._value)

    def __repr__(self):
        return "String({0})".format(self._value)

    def __str__(self):
        return str(self._value)


# ConsCell
##############################################################################

class ConsCell(SExpression):

    def __init__(self, car: SExpression, cdr: SExpression):
        #assert isinstance(car, SExpression), "expected SExpression"
        #assert isinstance(cdr, SExpression), "expected SExpression"
        self._car = car
        self._cdr = cdr

    @property
    def info(self) -> str:
        return "ConsCell expression with value {0} that it is {1} the end" \
               " of a list".format(self._car,
                                   "" if self._cdr is SYM_NIL else "not")

    @property
    def car(self) -> SExpression:
        return self._car

    @property
    def cdr(self) -> SExpression:
        return self._cdr

    def eval(self, env: Environment):
        car_eval = self._car.eval(env)
        if isinstance(car_eval, CallableSExpression):
            cs_expr = typing.cast(CallableSExpression, car_eval)
            return cs_expr.apply(cs_expr.process_arguments(self.cdr, env), env)
        else:
            raise EvaluationException(
                "Error evaluating '{0}', which is not a callable "
                "s-expression".format(self.car))

    def __eq__(self, other):
        return isinstance(other, ConsCell) and self.car == other.car \
               and self.cdr == other.cdr

    def __hash__(self):
        return 31 * hash(self.car) + hash(self.cdr)

    def __iter__(self):
        cons_cell = self
        while cons_cell != SYM_NIL:
            yield cons_cell.car
            cons_cell = cons_cell.cdr

    def __repr__(self):
        return "ConsCell(car={0}, cdr={1})".format(repr(self.car),
                                                   repr(self.cdr))

    def __str__(self):
        return "({0})".format(", ".join(map(str, self)))


# DataFrame
##############################################################################

class DataFrame(SExpression):

    @staticmethod
    def from_csv_file(file_path: str):
        return DataFrame(pd.read_csv(file_path))

    @property
    def info(self):
        return "Expression that is a binding to a Pandas DataFrame object"

    def __init__(self, df: pd.DataFrame):
        self._df = df

    @property
    def data_frame(self):
        return self._df

    def eval(self, env: Environment) -> SExpression:
        return self

    def __eq__(self, other):
        return isinstance(other, DataFrame) and self._df == other.data_frame

    def __hash__(self):
        return hash(self._df)

    def __repr__(self):
        return repr(self._df)

    def __str__(self):
        return str(self._df)
