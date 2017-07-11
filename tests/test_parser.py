# -*- coding: utf-8 -*-

import unittest

from csvinspector.lang import listops
from csvinspector.lang.lexer import StrLexer
from csvinspector.lang.parser import Parser
from csvinspector.lang.symbol import Symbol
from csvinspector.lang.types import Integer, Real, String


#
##############################################################################

SYMBOL = Symbol("SYMBOL")
INTEGER = Integer(1234)
REAL = Real(12.34)


#
##############################################################################

class TestParser(unittest.TestCase):

    def test_read_one_symbol(self):
        s_expr = Parser(StrLexer("SYMBOL")).parse_next()
        self.assertEqual(s_expr, SYMBOL)

    def test_read_one_symbol_with_spaces(self):
        s_expr = Parser(StrLexer("    SYMBOL  ")).parse_next()
        self.assertEqual(s_expr, SYMBOL)

    def test_read_one_integer(self):
        s_expr = Parser(StrLexer("1234")).parse_next()
        self.assertEqual(s_expr, INTEGER)

    def test_read_one_integer_with_spaces(self):
        s_expr = Parser(StrLexer("    1234  ")).parse_next()
        self.assertEqual(s_expr, INTEGER)

    def test_read_one_real(self):
        s_expr = Parser(StrLexer("12.34")).parse_next()
        self.assertEqual(s_expr, REAL)

    def test_read_one_real_with_spaces(self):
        s_expr = Parser(StrLexer("    12.34  ")).parse_next()
        self.assertEqual(s_expr, REAL)

    def test_read_one_string(self):
        s_expr = Parser(StrLexer('"hello"')).parse_next()
        self.assertEqual(s_expr, String("hello"))

    def test_read_one_string_with_escaped_characters(self):
        s_expr = Parser(StrLexer(r'"hello \"me\""')).parse_next()
        self.assertEqual(s_expr, String('hello "me"'))

    def test_read_one_string_with_spaces(self):
        s_expr = Parser(StrLexer('  "hello"   ')).parse_next()
        self.assertEqual(s_expr, String("hello"))

    def test_read_simple_list(self):
        s_expr = Parser(StrLexer("    (1234 SYMBOL)")).parse_next()
        self.assertEqual(listops.from_args(INTEGER, SYMBOL), s_expr)

    def test_multilevel_list_left(self):
        s_expr = Parser(StrLexer("((1234) SYMBOL)")).parse_next()
        left = listops.from_args(INTEGER)
        self.assertEqual(listops.from_args(left, SYMBOL), s_expr)

    def test_multilevel_list_right(self):
        s_expr = Parser(StrLexer("(1234 (SYMBOL))")).parse_next()
        right = listops.from_args(SYMBOL)
        self.assertEqual(listops.from_args(INTEGER, right), s_expr)

    def test_multilevel_list_both(self):
        s_expr = Parser(StrLexer(" ( (1234) (SYMBOL) ) ")).parse_next()
        left = listops.from_args(INTEGER)
        right = listops.from_args(SYMBOL)
        self.assertEqual(listops.from_args(left, right), s_expr)
