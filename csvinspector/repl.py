# -*- coding: utf-8 -*-

import logging

from . import primitives, VERSION_STR
from .lang.base import SExpression
from .lang.exceptions import EvaluationException
from .lang.environment import Environment, NestedEnvironment
from .lang.lexer import StrLexer, LexerException
from .lang.parser import Parser, ParserException
from .lang.symbol import SYM_NIL


#
##############################################################################

EXIT_CMD = ":exit"
HELP_CMD = ":help"
INFO_CMD = ":info"
VERSION_CMD = ":version"

_log = logging.getLogger('repl')


#
##############################################################################

def run_repl(env: Environment=NestedEnvironment()):
    show_banner()
    primitives.load_all(env)

    while True:
        input_str = read_input()
        if EXIT_CMD == input_str:
            break
        elif HELP_CMD == input_str:
            show_help()
        elif input_str.startswith(INFO_CMD):
            process_input_and_show_info(input_str[len(INFO_CMD):], env)
        elif VERSION_CMD == input_str:
            print(VERSION_STR)
        else:
            process_input(input_str, env, show_result=True)

    print("Exiting... Bye!")


def show_banner():
    print("Welcome to csv-inspector. Inspect csv files using a lisp like")
    print("language")
    print("")
    print("Type the expression to evaluate:")
    print("\t* waits for parentheses to balance or an empty line")
    print("\t* type {0} to exit the REPL".format(EXIT_CMD))
    print("\t* type {0} to get information of any expression".format(
        INFO_CMD))
    print("")


def show_help():
    print("This interpreter uses a lisp like syntax, some expressions you")
    print(" play with to get used to it are:")
    print("\t* Arithmetic operations:")
    print("\t  (+ 3 5), (* 5 -9), (/ 2 5.0), ...")
    print("\t* Bind values to names:")
    print("\t  (let a 3) (let b 5) (+ a b)")


def read_input():
    try:
        line = input("> ")
        parentheses_balance = compute_parentheses_balance(line)
        buf = line

        while line and parentheses_balance != 0:
            buf += '\n'
            line = input("# ")
            buf += line
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


def process_input(text: str, env: Environment, show_result: bool) \
        -> SExpression or None:
    try:
        p = Parser(StrLexer(text))
        result = SYM_NIL
        while p.has_next():
            s_expr = p.parse_next()
            result = s_expr.eval(env)
        if show_result and SYM_NIL != result:
            print(">>>>>", result)
        return result
    except (EvaluationException, LexerException,
            ParserException) as e:
        print("~~~~~", e)

    return None


def process_input_and_show_info(text: str, env: Environment):
    r = process_input(text, env, show_result=False)
    if r is not None:
        print(r.info)
