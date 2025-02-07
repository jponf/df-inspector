#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys


from csvinspector import primitives
from csvinspector import VERSION_BRANCH, VERSION_STR, interpreter
from csvinspector.lang.environment import NestedEnvironment


#
##############################################################################

LOGGING_LEVELS = {
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}

DEFAULT_LOGGING_LEVEL = 'error'


#
##############################################################################

def main():
    args = parse_command_line_args(sys.argv[1:])
    set_up_logging(args)

    env = NestedEnvironment()
    primitives.load_all(env)

    if args.script is not None:
        interpreter.run_file(env, args.script)
    else:
        interpreter.run_repl(env)


# Setup
##############################################################################

def set_up_logging(args):
    date_fmt = '%Y/%m/%d %H:%M:%S'
    msg_fmt = '[%(levelname)s - %(asctime)s] %(message)s'
    # msg_fmt = '[%(levelname)s - %(name)s - %(asctime)s] %(message)s'

    logging.basicConfig(datefmt=date_fmt, format=msg_fmt,
                        level=LOGGING_LEVELS[args.verbosity],
                        stream=sys.stderr)


# Command line
##############################################################################

def parse_command_line_args(args):
    parser = argparse.ArgumentParser(
        prog='csv-inspector',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--version', action='version',
                        version="%(prog)s {0} {1}".format(
                            VERSION_STR, VERSION_BRANCH))

    parser.add_argument('-v', '--verbosity', action='store',
                        choices=LOGGING_LEVELS.keys(),
                        default=DEFAULT_LOGGING_LEVEL)

    parser.add_argument('script', nargs='?', type=str, default=None,
                        help="Script file to execute")

    return parser.parse_args(args)


# Entry point
##############################################################################

if __name__ == '__main__':
    main()
