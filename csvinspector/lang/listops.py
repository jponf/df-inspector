# -*- coding: utf-8 -*-

import typing

from .base import SExpression
from .symbol import SYM_NIL
from .types import ConsCell


#
##############################################################################


def from_args(*args: [SExpression]):
    return from_list(args)


def from_list(elements: [SExpression]):
    head = SYM_NIL
    for e in reversed(elements):
        head = ConsCell(e, head)
    return head


def to_list(s_expr_list: SExpression, start=0, stop=None) -> [SExpression]:
    iterator = iterate(s_expr_list, start, stop)
    return list(iterator)


def iterate(s_expr_list: SExpression, start=0, stop=None):
    i, index = 0, s_expr_list

    while index != SYM_NIL and (stop is None or i < stop):
        if i >= start:
            cc_index = typing.cast(ConsCell, index)
            index = cc_index.cdr
            yield cc_index.car
        i += 1


def length(s_expr_list: SExpression) -> int:
    l = 0
    for _ in iterate(s_expr_list):
        l += 1
    return l


def nth(s_expr_list: SExpression, pos: int) -> SExpression:
    cur = typing.cast(ConsCell, s_expr_list)
    while pos > 0:
        cur = cur.cdr
        pos -= 1
    return cur.car


def is_list_of(s_expr_list: SExpression, klass: type, stop=None) -> bool:
    for car in iterate(s_expr_list, start=0, stop=stop):
        if not isinstance(car, klass):
            return False
    return True
