import unittest

from csvinspector.lang import listops
from csvinspector.lang.environment import NestedEnvironment
from csvinspector.lang.symbol import SYM_NIL
from csvinspector.lang.types import Integer
from csvinspector.primitives import FunctionAdd, FunctionSubtract


class TestFunctionAdd(unittest.TestCase):

    def setUp(self):
        self.env = NestedEnvironment()
        self.f_add = FunctionAdd('+')

    def test_base_add(self):
        result = self.f_add.apply(SYM_NIL, self.env)
        self.assertEqual(result, Integer(0))

    def test_addition_of_two_integers(self):
        op = listops.from_list([Integer(2), Integer(3)])
        result = self.f_add.apply(op, self.env)
        self.assertEqual(result, Integer(5))

    def test_addition_of_more_integers(self):
        op = listops.from_list([Integer(2), Integer(3),
                                Integer(4), Integer(5)])
        result = self.f_add.apply(op, self.env)
        self.assertEqual(result, Integer(14))

    def test_addition_of_negative_numbers(self):
        op = listops.from_list([Integer(-2), Integer(-3)])
        result = self.f_add.apply(op, self.env)
        self.assertEqual(result, Integer(-5))


class TestFunctionSubtract(unittest.TestCase):

    def setUp(self):
        self.env = NestedEnvironment()
        self.f_subtract = FunctionSubtract('-')

    def test_base_subtract(self):
        result = self.f_subtract.apply(SYM_NIL, self.env)
        self.assertEqual(result, Integer(0))

    def test_subtraction_of_two_integers(self):
        op = listops.from_list([Integer(2), Integer(3)])
        result = self.f_subtract.apply(op, self.env)
        self.assertEqual(result, Integer(-1))

    def test_subtraction_of_more_integers(self):
        op = listops.from_list([Integer(2), Integer(3),
                                Integer(4), Integer(5)])
        result = self.f_subtract.apply(op, self.env)
        self.assertEqual(result, Integer(-10))

    def test_subtraction_of_negative_numbers(self):
        op = listops.from_list([Integer(-2), Integer(-3)])
        result = self.f_subtract.apply(op, self.env)
        self.assertEqual(result, Integer(1))
