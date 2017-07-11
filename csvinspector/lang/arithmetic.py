# -*- coding: utf-8 -*-

from .data import BaseNumber, Integer, Real

#
##############################################################################

_BINARY_RESULT_TYPE = {(Integer, Integer): Integer,
                       (Integer, Real): Real,
                       (Real, Integer): Real,
                       (Real, Real): Real}


#
##############################################################################

def add(op1: BaseNumber, op2: BaseNumber) -> BaseNumber:
    types = (type(op1), type(op2))
    return _BINARY_RESULT_TYPE[types](op1.value + op2.value)


def subtract(op1: BaseNumber, op2: BaseNumber) -> BaseNumber:
    types = (type(op1), type(op2))
    return _BINARY_RESULT_TYPE[types](op1.value - op2.value)


def multiply(op1: BaseNumber, op2: BaseNumber) -> BaseNumber:
    types = (type(op1), type(op2))
    return _BINARY_RESULT_TYPE[types](op1.value * op2.value)


def divide(op1: BaseNumber, op2: BaseNumber) -> BaseNumber:
    types = (type(op1), type(op2))
    return _BINARY_RESULT_TYPE[types](op1.value / op2.value)


def power(op1: BaseNumber, op2: BaseNumber) -> BaseNumber:
    types = (type(op1), type(op2))
    return _BINARY_RESULT_TYPE[types](op1.value ** op2.value)
