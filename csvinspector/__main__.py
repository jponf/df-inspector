#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys

from . import VERSION_BRANCH, VERSION_STR, primitives


#
##############################################################################

LOGGING_LEVELS = {
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}


#
##############################################################################

def main():
    args = parse_command_line_args(sys.argv[1:])
    set_up_logging(args)


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

    return parser.parse_args(args)


# Entry point
##############################################################################

if __name__ == '__main__':
    main()
