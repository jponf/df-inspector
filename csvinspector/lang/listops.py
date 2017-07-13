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


def iterate(s_expr_list: SExpression):
    index = s_expr_list
    while index != SYM_NIL:
        cc_index = typing.cast(ConsCell, index)
        index = cc_index.cdr
        yield cc_index.car


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


def is_list_of(s_expr_list: SExpression, klass: type) -> bool:
    for car in iterate(s_expr_list):
        if not isinstance(car, klass):
            return False
    return True
