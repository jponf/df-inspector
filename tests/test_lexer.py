
import unittest

from csvinspector.lexer import  StrLexer, TOKEN_EOF


#
##############################################################################

class LexerText(unittest.TestCase):

    def test_empty_string(self):
        lexer = StrLexer("")
        self.assertEqual(TOKEN_EOF, lexer.next_token())
