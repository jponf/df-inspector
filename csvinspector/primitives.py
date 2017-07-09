# -*- coding: utf-8 -*-

import logging

from .lang.data import Environment, CallableSExpression

#
##############################################################################

_log = logging.getLogger("predicates")


# Functions
##############################################################################


# Special symbols
##############################################################################


# Module functions
##############################################################################

def load(env: Environment):
    _log.debug("Loading system primitives")
