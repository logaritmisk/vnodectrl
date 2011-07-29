#!/usr/bin/env python

from distutils.core import setup
from shutil import copyfile
import os.path

files = []
if not os.path.isfile('/etc/vnodectrl/vnodectrl.conf'):
    # Create a vnodectrl.conf file out of the
    # vnodectrl.conf.dist file.
    copyfile('vnodectrl.conf.dist', 'vnodectrl.conf')
    files.append(('/etc/vnodectrl', ['vnodectrl.conf']))

setup(name='vnodectrl',
      version='3.0',
      description='Virtual Node Control scripts',
      author='Anders Olsson',
      author_email='anders@nodeone.se',
      url='http://github.com/logaritmisk/vnodectrl',
      packages=['vnodectrl', 'vnodectrl.plugins'],
      scripts=['scripts/vnodectrl', 'scripts/vnodectrl-ec2-ssh'],
      # This configuration file will be used for users
      # that don't have their own configuration in their .vnodectrl
      # folder.
      data_files=files
)
