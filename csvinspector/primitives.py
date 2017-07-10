# -*- coding: utf-8 -*-

import logging

from .lang.data import SYM_NIL, SYM_FALSE, SYM_TRUE, Environment,\
    CallableSExpression

#
##############################################################################

_log = logging.getLogger("predicates")


# Functions
##############################################################################


# Special symbols
##############################################################################


# Module functions
##############################################################################

def load_all(env: Environment):
    _log.debug("Loading all system primitives")
    load_default_symbols(env)


def load_default_symbols(env: Environment):
    _log.debug("Loading default symbols: %s, %s and %s",
               str(SYM_NIL), str(SYM_FALSE), str(SYM_TRUE))
    env.bind_global(SYM_NIL, SYM_NIL)
    env.bind_global(SYM_FALSE, SYM_FALSE)
    env.bind_global(SYM_TRUE, SYM_TRUE)
