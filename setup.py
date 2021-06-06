#!/usr/bin/env python

from distutils.core import setup

setup(name='tilt_logger',
      version='0.1',
      description='TILT to Pg logging tool',
      author='Florent Dosso',
      author_email='dosso.florent@gmail.com',
      package_dir={'tilt_logger': 'src'},
      packages=['tilt_logger'],
      install_requires=[
          'psycopg2-binary',
          'aioblescan'
        ]
     )