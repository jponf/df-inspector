# -*- coding: utf-8 -*-

import abc
import collections
import enum

from .exceptions import LexerException


#
##############################################################################

Token = collections.namedtuple("Token", ["type", "text"])


class TokenType(enum.Enum):
    EOF = 0
    ATOM = 1
    REAL = 2
    INTEGER = 3
    STRING = 4
    LPAREN = 5
    RPAREN = 6
    CLINE = 7


TOKEN_EOF = Token(TokenType.EOF, "")
TOKEN_LPAREN = Token(TokenType.LPAREN, "")
TOKEN_RPAREN = Token(TokenType.RPAREN, "")
TOKEN_CLINE = Token(TokenType.CLINE, "")


def new_atom(text: str) -> Token:
    return Token(TokenType.ATOM, text)


def new_integer(text: str) -> Token:
    return Token(TokenType.INTEGER, text)


def new_real(text: str) -> Token:
    return Token(TokenType.REAL, text)


def new_string(text: str) -> Token:
    return Token(TokenType.STRING, text)


#
##############################################################################

_NUM_SIGNS = frozenset(['-', '+'])
OPERANDS = frozenset(['=', '+', '-', '*', '/', '^', '.', '$'])


class Lexer(metaclass=abc.ABCMeta):

    EOF = None

    def __init__(self):
        self._ch = None

    @property
    def current_character(self):
        return self._ch

    @current_character.setter
    def current_character(self, character):
        if character is not Lexer.EOF and len(character) != 1:
            raise ValueError("Only one character is accepted")
        self._ch = character

    @abc.abstractmethod
    def consume(self):
        raise NotImplementedError("Abstract method!")

    def is_eof(self):
        return self._ch is Lexer.EOF

    def is_whitespace(self):
        return not self.is_eof() and self._ch.isspace()

    def is_alnum(self):
        return not self.is_eof() and self._ch.isalnum()

    def is_alpha(self):
        return not self.is_eof() and self._ch.isalpha()

    def is_number(self):
        return not self.is_eof() and self._ch.isnumeric()

    def is_full_stop(self):
        return not self.is_eof() and self._ch == '.'

    def is_operand(self):
        return self._ch in OPERANDS

    def is_number_sign(self):
        return self._ch in _NUM_SIGNS

    def next_token(self) -> Token:
        while not self.is_eof():
            if self._ch.isspace():
                self.skip_whitespace()
            elif self._ch == '(':
                self.consume()
                return TOKEN_LPAREN
            elif self._ch == ')':
                self.consume()
                return TOKEN_RPAREN
            elif self._ch == '#':
                self.consume()
                return TOKEN_CLINE
            elif self._ch == '"':
                return self.parse_string()
            elif self.is_number_sign():
                return self.parse_atom_or_number("")
            elif self.is_alpha() or self.is_operand():
                return self.parse_atom("")
            elif self.is_number():
                return self.parse_number("")
            else:
                self.raise_invalid_character()

        return TOKEN_EOF

    def parse_string(self):
        if self._ch != '"':
            self.raise_expected_character('"')

        self.consume()
        buf, escape = "", False
        while not self.is_eof() and (escape or self._ch != '"'):
            if escape or self._ch != '\\':
                buf += self._ch
                escape = False
            else:
                escape = True
            self.consume()

        if self._ch == '"':
            self.consume()
            return new_string(buf)

        self.raise_expected_character('"')

    def parse_atom_or_number(self, buf):
        if self.is_number_sign():
            buf += self._ch
            self.consume()

        if self.is_number():
            return self.parse_number(buf)
        else:
            return self.parse_atom(buf)

    def parse_atom(self, buf):
        if self.is_operand():
            buf += self._ch
            self.consume()

        while self.is_alnum() or self._ch == '_':
            buf += self._ch
            self.consume()

        if self.is_eof() or self.is_whitespace() or self._ch == ')':
            return new_atom(buf)

        self.raise_invalid_character()

    def parse_number(self, buf):
        is_decimal = False
        while self.is_number() or (self.is_full_stop() and not is_decimal):
            if self.is_full_stop():
                is_decimal = True
            buf += self._ch
            self.consume()

        if self.is_eof() or self.is_whitespace() or self._ch == ')':
            return new_real(buf) if is_decimal else new_integer(buf)

        self.raise_invalid_character()

    def skip_whitespace(self):
        while self.is_whitespace():
            self.consume()

    def raise_expected_character(self, expected):
        raise LexerException("Expected '{0}' but found '{1}'".format(
            expected, "EOF" if self._ch is Lexer.EOF else self._ch))

    def raise_invalid_character(self):
        raise LexerException("Invalid character '{0}'".format(self._ch))


#
##############################################################################

class StrLexer(Lexer):

    def __init__(self, str_input: str):
        super().__init__()
        self._input = str_input or " "
        self._index = 0
        self.current_character = self._input[self._index]

    def consume(self):
        self._index += 1
        self.current_character = self._input[self._index] \
            if self._index < len(self._input) else Lexer.EOF



class FileLexer(Lexer):

    def __init__(self, file_path: str):
        super().__init__()
        self._input = open(file_path, 'r')
        self.consume()

    def consume(self):
        ch = self._input.read(1)
        self.current_character = ch if ch else Lexer.EOF
