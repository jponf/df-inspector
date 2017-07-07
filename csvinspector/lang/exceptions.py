# -*- coding: utf-8 -*-


class EvaluationException(Exception):
    """Exception raised when the language evaluation fails."""


class SymbolNotDefinedException(EvaluationException):
    """Exception raised when a symbol has not been defined."""
