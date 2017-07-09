# -*- coding: utf-8 -*-

import unittest

from csvinspector.lang.data import Symbol, Integer, Real
from csvinspector.lang.lexer import StrLexer
from csvinspector.lang.parser import Parser


#
##############################################################################

SYMBOL = Symbol("SYMBOL")
INTEGER = Integer(1234)
REAL = Real(12.34)


#
##############################################################################

class TestParser(unittest.TestCase):

    def test_read_one_symbol(self):
        s_expr = Parser(StrLexer("SYMBOL")).symbolic_expr()
        self.assertEqual(s_expr, SYMBOL)

    def test_read_one_symbol_with_spaces(self):
        s_expr = Parser(StrLexer("    SYMBOL  ")).symbolic_expr()
        self.assertEqual(s_expr, SYMBOL)

    def test_read_one_integer(self):
        s_expr = Parser(StrLexer("1234")).symbolic_expr()
        self.assertEqual(s_expr, INTEGER)

    def test_read_one_integer_with_spaces(self):
        s_expr = Parser(StrLexer("    1234  ")).symbolic_expr()
        self.assertEqual(s_expr, INTEGER)

    def test_read_one_real(self):
        s_expr = Parser(StrLexer("12.34")).symbolic_expr()
        self.assertEqual(s_expr, REAL)

    def test_read_one_real_with_spaces(self):
        s_expr = Parser(StrLexer("    12.34  ")).symbolic_expr()
        self.assertEqual(s_expr, REAL)
