#!/usr/bin/env python

from distutils.core import setup

setup(name='vnodectrl',
      version='3.0',
      description='Virtual Node Control scripts',
      author='Anders Olsson',
      author_email='anders@nodeoen.se',
      url='http://github.com/logaritmisk/vnodectrl',
      packages=['vnodectrl', 'vnodectrl.plugins'],
      scripts=['scripts/vnodectrl']
)
