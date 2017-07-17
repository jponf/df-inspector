# -*- coding: utf-8 -*-

import logging

from . import primitives, VERSION_STR
from .lang.exceptions import EvaluationException
from .lang.environment import Environment, NestedEnvironment
from .lang.lexer import StrLexer, LexerException
from .lang.parser import Parser, ParserException
from .lang.symbol import SYM_NIL


#
##############################################################################

HELP_CMD = ":help"
EXIT_CMD = ":exit"
VERSION_CMD = ":version"

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
        elif HELP_CMD == input_str:
            show_help()
        elif VERSION_CMD == input_str:
            print(VERSION_STR)
        else:
            try:
                p = Parser(StrLexer(input_str))
                s_expr = p.parse_next()
                result = s_expr.eval(env)
                if SYM_NIL != result:
                    print(">>>>>", result)
            except (EvaluationException, LexerException,
                    ParserException) as e:
                print("~~~~~", e)

    print("Exiting... Bye!")


def show_banner():
    print("Welcome to csv-inspector. Inspect csv files using a lisp like")
    print("language")
    print("")
    print("Type the expression to evaluate:")
    print("\t* interpet waits for parentheses to balance")
    print("\t* or for an empty line")
    print("\t* type :exit to exit the REPL")
    print("")


def show_help():
    print("TODO")


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
    except EOFError:
        _log.info("EOF found, submitting command '%s'", EXIT_CMD)
        return EXIT_CMD


def compute_parentheses_balance(text: str):
    balance = 0
    for c in text:
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
    return balance
