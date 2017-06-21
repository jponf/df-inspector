#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys


#
##############################################################################

def main():
    args = parse_command_line_args(sys.argv[1:])

    

#
##############################################################################

def parse_command_line_args(args):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    return parser.parse_args(args)


#
##############################################################################

if __name__ == '__main__':
    main()
