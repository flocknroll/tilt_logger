#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tilt_logger',
      version='0.1',
      description='TILT to Pg logging tool',
      author='Florent Dosso',
      author_email='dosso.florent@gmail.com',
      package_dir={'': 'src'},
      packages=find_packages(),
      install_requires=[
          'aiopg',
          'aioblescan',
          'python-dateutil'
      ],
      entry_points = {
          'console_scripts': ['tilt-logger=tilt_logger.__main__:main'],
      }
     )
