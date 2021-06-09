#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tilt_logger',
      version='0.1',
      description='TILT to Pg logging tool',
      author='Florent Dosso',
      author_email='dosso.florent@gmail.com',
      package_dir={'tilt_logger': 'src'},
      packages=find_packages('tilt_logger'),
      install_requires=[
          'aiopg',
          'aioblescan',
          'python-dateutil'
        ]
     )