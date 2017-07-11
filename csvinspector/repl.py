# -*- coding: utf-8 -*-

import logging

from . import primitives
from .lang.exceptions import EvaluationException
from .lang.environment import Environment, NestedEnvironment
from .lang.parser import Parser, ParserException
from .lang.lexer import StrLexer, LexerException


#
##############################################################################

EXIT_CMD = ":exit"

_log = logging.getLogger('repl')


#
##############################################################################

def run(env: Environment=NestedEnvironment()):
    show_banner()
    primitives.load_all(env)

    while True:
        input_str = read_input()
        if EXIT_CMD == input_str:
            break

        try:
            p = Parser(StrLexer(input_str))
            s_expr = p.parse_next()
            result = s_expr.eval(env)
            print(">>>>>", result)
        except (EvaluationException, LexerException, ParserException) as e:
            print("~~~~~", e)

    print("Bye!")


def show_banner():
    print("Welcome to csv-inspector. Inspect csv files using a lisp like")
    print("language")
    print("")
    print("Type the expression to evaluate:")
    print("\t* interpet waits for parentheses to balance")
    print("\t* or for an empty line")
    print("\t* type: :exit to exit the REPL")
    print("")


def read_input():
    try:
        line = input("> ")
        parentheses_balance = compute_parentheses_balance(line)
        buf = line + '\n'

        while line and parentheses_balance != 0:
            buf += line
            buf += '\n'
            line = input("# ")
            parentheses_balance += compute_parentheses_balance(line)

        return buf.strip()
    except KeyboardInterrupt:
        _log.info("Captured interruption, submitting command '%s'", EXIT_CMD)
        return EXIT_CMD


def compute_parentheses_balance(text: str):
    balance = 0
    for c in text:
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
    return balance
