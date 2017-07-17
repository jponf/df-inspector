# -*- coding: utf-8 -*-

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 0

VERSION_BRANCH = 'alpha'

VERSION = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
VERSION_STR = ".".join(map(str, VERSION))

__version__ = VERSION_STR
