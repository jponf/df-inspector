# -*- coding: utf-8 -*-

import logging
import readline  # TODO: Check if it works on Mac and Windows

from . import VERSION_STR
from .lang.base import SExpression
from .lang.exceptions import EvaluationException
from .lang.environment import Environment
from .lang.lexer import FileLexer, StrLexer, LexerException
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

def run_file(env: Environment, file_path: str):
    try:
        lexer = FileLexer(file_path=file_path)
        p = Parser(lexer)
        while p.has_next():
            s_expr = p.parse_next()
            _ = s_expr.eval(env)
    except IOError as e:
        _log.critical(e)
    except (LexerException, ParserException) as e:
        _log.error("Lexer/Parser error: %s", str(e))
    except EvaluationException as e:
        _log.error("Evaluation error: %s", str(e))


#
##############################################################################

def run_repl(env: Environment):
    show_banner()

    # TODO: Completion of language words
    readline.parse_and_bind('tab: complete')
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
    print("Welcome to the df-inspector Read-Eval-Print-Loop.")
    print("Inspect data files (csv, xls, xlsx, ...) effortlessly")
    print("")
    print("Tips:")
    print("\t* the REPL waits for parentheses to balance or an empty line")
    print("\t* type {0} to exit the REPL".format(EXIT_CMD))
    print("\t* type {0} to get information of any expression".format(
        INFO_CMD))
    print("")


def show_help():
    print("This interpreter uses a lisp like syntax, some expressions you")
    print("can play with to get used to it are:")
    print("\t* Arithmetic operations:")
    print("\t  (+ 3 5), (* 5 -9), (/ 2 5.0), ...")
    print("\t* Bind values to names:")
    print("\t  (let a 3) (let b 5) (+ a b)")
    print("")
    print("Additionally the REPL supports the following special instructions:")
    print("\t* {0}: exit the REPL".format(EXIT_CMD))
    print("\t* {0}: prints information of any expression".format(INFO_CMD))
    print("\t* {0}: prints this message".format(HELP_CMD))
    print("\t* {0}: prints the system version".format(VERSION_CMD))


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
