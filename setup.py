#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
    have_setuptools = True
except ImportError:
    from distutils.core import setup
    have_setuptools = False

import csvinspector

# comma separated list of names
authors='Josep Pon, Eduard Torres'

# comma separated list of emails, following authors ordering
emails='jponfarreny@diei.udl.cat, eduard.torres@udl.cat'

# Short description
description= ""

# Long description
with open('README.md') as f:
    readme = f.read()

# Requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


# Additional keyword arguments
if have_setuptools:
    kwargs = {
        'entry_points': {
            'console_scripts': ['csvi = csvinspector.__main__:main']
        },
        'install_requires': requirements,
    }
else:
    pass
    # kwargs = dict(
    #     scripts = ['scripts/dgga']
    # )



##############################################################################

setup(
    name='pydgga',
    version=csvinspector.VERSION_STR,
    description=description,
    long_description=readme,
    author=authors,
    author_email=emails,
    url="https://arcadia.hardlog.udl.cat/hlog-res/pydgga",
    license="",
    keywords = 'distributed genetic algorithm configurator gga dgga',
    packages=['pydgga'],
    platforms='any',
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    **kwargs
)