# -*- coding: utf-8 -*-

from .base import Environment, SExpression


# Symbol
##############################################################################

class Symbol(SExpression):

    def __init__(self, name: str):
        self.name = name

    def eval(self, env: Environment):
        return env.find(self)

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "Symbol(name={0})".format(self.name)

    def __str__(self):
        return self.name


SYM_NIL = Symbol('nil')
SYM_TRUE = Symbol('true')
SYM_FALSE = Symbol('false')
