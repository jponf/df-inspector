
import unittest

from csvinspector.lexer import LexerException, StrLexer, TOKEN_EOF,\
    new_atom, new_integer, new_real


#
##############################################################################

class LexerText(unittest.TestCase):

    def test_empty_string(self):
        lexer = StrLexer("")
        self.assertEqual(TOKEN_EOF, lexer.next_token())

    def test_one_atom(self):
        self.assert_tokens("hydrogen", new_atom("hydrogen"))

    def test_one_integer(self):
        self.assert_tokens("42", new_integer("42"))

    def test_one_real(self):
        self.assert_tokens("5.0", new_real("5.0"))

    def test_operand_assign(self):
        self.assert_tokens("=", new_atom("="))

    def test_atom_with_operand_in_between(self):
        with self.assertRaises(LexerException):
            self.assert_tokens("h=i")

    def assert_tokens(self, text, *tokens):
        lexer_tokens = run_lexer(text)
        self.assertEqual(lexer_tokens, tokens)


def run_lexer(text):
    lexer = StrLexer(text)
    token = lexer.next_token()
    tokens = []
    while token != TOKEN_EOF:
        tokens.append(token)
        token = lexer.next_token()
    return tuple(tokens)
