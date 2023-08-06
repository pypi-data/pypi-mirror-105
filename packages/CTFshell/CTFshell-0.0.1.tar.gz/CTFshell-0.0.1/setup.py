#!/usr/bin/env python

try:
    from setuptools import setup
except Exception:
    from distutils.core import setup

CTF_SHELL_VERSION = "0.0.1"
#                    | | |
#             +------+ | +---+
#             |        |     |
#          current:revision:age
#             |        |     |
#             |        |     +- increment if interfaces have been added
#             |        |        set to zero if interfaces have been removed
#             |        |        or changed
#             |        +- increment if source code has changed
#             |           set to zero if current is incremented
#             +- increment if interfaces have been added, removed or changed


with open('README.rst', 'r') as f:
    README = f.read()

setup(name='CTFshell',
      version=CTF_SHELL_VERSION,
      description='Client CLI for the Cryptotronix CTF server.',
      author='Cryptotronix LLC',
      author_email='hello@cryptotronix.com',
      url='https://github.com/cryptotronix/python-ctf-server',
      scripts=['CTFshell'],
      license="AGPL V3",
      long_description=README,
      install_requires=[
          "prompt_toolkit>=3.0.5",
          "pygments>=2.2.0",
          "thrift>=0.13.0",
          "texttable>=1.6.2",
          "sqlalchemy>=1.3.13",
          "requests>=2.22.0"
      ],
      )
