# -*- coding: utf-8 -*-

from . import listops
from .exceptions import ParserException
from .lexer import Lexer, TokenType
from .symbol import Symbol
from .types import ConsCell, Integer, Real, String, SExpression


#
##############################################################################

class Parser(object):

    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._lookahead = None
        self._consume()

    def parse_next(self) -> SExpression:
        if self._lookahead.type is TokenType.ATOM:
            return self._atom()
        elif self._lookahead.type is TokenType.REAL:
            return self._real()
        elif self._lookahead.type is TokenType.INTEGER:
            return self._integer()
        elif self._lookahead.type is TokenType.STRING:
            return self._string()
        elif self._lookahead.type is TokenType.LPAREN:
            return self._list()

        raise ParserException("Expected Atom, Real, Integer or List,"
                              " found {0}".format(self._lookahead.type.name))

    def _atom(self) -> Symbol:
        self._match(TokenType.ATOM)
        s_expr = Symbol(self._lookahead.text)
        self._consume()
        return s_expr

    def _real(self) -> Real:
        self._match(TokenType.REAL)
        s_expr = Real(float(self._lookahead.text))
        self._consume()
        return s_expr

    def _integer(self) -> Integer:
        self._match(TokenType.INTEGER)
        s_expr = Integer(int(self._lookahead.text))
        self._consume()
        return s_expr

    def _string(self) -> String:
        self._match(TokenType.STRING)
        s_expr = String(self._lookahead.text)
        self._consume()
        return s_expr

    def _list(self) -> ConsCell:
        elements = []
        self._match_and_consume(TokenType.LPAREN)
        while self._lookahead.type != TokenType.RPAREN:
            elements.append(self.parse_next())
        self._match_and_consume(TokenType.RPAREN)
        return listops.from_list(elements)

    def _consume(self) -> None:
        self._lookahead = self._lexer.next_token()

    def _match(self, token_type: TokenType) -> None:
        if self._lookahead.type is not token_type:
            raise ParserException('Expected {0}, found {1}'.format(
                token_type.name, self._lookahead.type.name))

    def _match_and_consume(self, token_type: TokenType) -> None:
        self._match(token_type)
        self._consume()
