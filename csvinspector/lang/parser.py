# -*- coding: utf-8 -*-

from .exceptions import ParserException
from .data import ConsCell, Integer, Real, Symbol
from .lexer import Lexer, TokenType


#
##############################################################################

class Parser(object):

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.lookahead = None

    def sexpr(self):
        if self.lookahead.type is TokenType.ATOM:
            return self._atom()
        elif self.lookahead.type is TokenType.REAL:
            return self._real()
        elif self.lookahead.type is TokenType.INTEGER:
            return self._integer()
        elif self.lookahead.type is TokenType.LPAREN:
            return self._list()

        raise ParserException("Expected Atom, Real, Integer or List,"
                              " found {0}".format(self.lookahead.type.name))

    def _atom(self):
        self._match(TokenType.ATOM)
        s_expr = Symbol(self.lookahead.text)
        self._consume()
        return s_expr

    def _real(self):
        self._match(TokenType.REAL)
        s_expr = Real(float(self.lookahead.text))
        self._consume()
        return s_expr

    def _integer(self):
        self._match(TokenType.INTEGER)
        s_expr = Real(int(self.lookahead.text))
        self._consume()
        return s_expr

    def _list(self):
        pass

    def _consume(self):
        self.lookahead = self.lexer.consume()

    def _match(self, token_type: TokenType):
        if self.lookahead.type is not token_type:
            raise ParserException('Expected {0}, found {1}'.format(
                token_type.name, self.lookahead.type.name))
