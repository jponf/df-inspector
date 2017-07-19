# -*- coding: utf-8 -*-


class ParserException(Exception):
    """Exception raised when the parser encounters an error."""


class LexerException(Exception):
    """Raised when the lexer cannot understand the input."""


class EvaluationException(Exception):
    """Exception raised when the language evaluation fails."""


class SymbolNotDefinedException(EvaluationException):
    """Exception raised when a symbol has not been defined."""


class SymbolLockedException(EvaluationException):
    """Exception raised when setting the value of a locked symbol."""


class ArgumentsException(EvaluationException):
    """Exception raised when there is a problem with the arguments
    of a function."""
