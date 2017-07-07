# -*- coding: utf-8 -*-


class ParserException(Exception):
    """Exception raised when the parser encounters an error."""


class EvaluationException(Exception):
    """Exception raised when the language evaluation fails."""


class SymbolNotDefinedException(EvaluationException):
    """Exception raised when a symbol has not been defined."""
