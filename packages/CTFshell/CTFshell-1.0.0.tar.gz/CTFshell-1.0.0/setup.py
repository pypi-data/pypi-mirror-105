#!/usr/bin/env python

try:
    from setuptools import setup
except Exception:
    from distutils.core import setup

CTF_SHELL_VERSION = None
with open('ctfshell', 'r') as f:
    line = f.readline()
    while line:
        if line.find("CTF_SHELL_VERSION = ") >= 0:
            start = line.find("\"")
            end = line.find("\"", start + 1)
            if start >= 0 and end >= 0:
                CTF_SHELL_VERSION = line[start+1:end]
            line = None
        else:
            line = f.readline()


with open('README.rst', 'r') as f:
    README = f.read()

setup(name='CTFshell',
      version=CTF_SHELL_VERSION,
      description='Client CLI for the Cryptotronix CTF server.',
      author='Cryptotronix LLC',
      author_email='hello@cryptotronix.com',
      url='https://github.com/cryptotronix/python-ctf-server',
      scripts=['ctfshell'],
      license="AGPL V3",
      long_description=README,
      install_requires=[
          "prompt_toolkit>=3.0.5",
          "pygments>=2.2.0",
          "texttable>=1.6.2",
          "sqlalchemy>=1.3.13",
          "requests>=2.22.0"
      ],
      )
