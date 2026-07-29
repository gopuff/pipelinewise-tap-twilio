#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pipelinewise-tap-twilio',
      version='1.1.4',  # Quieter INFO logs for long-running syncs
      description='Singer.io tap for extracting data from the Twilio API - PipelineWise compatible',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='GoPuff',  # Claim your fork!
      url='https://github.com/gopuff/pipelinewise-tap-twilio',
      classifiers=[
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Programming Language :: Python :: 3 :: Only'
      ],
      py_modules=['tap_twilio'],
      install_requires=[
          'requests>=2.25.1',      # Unpinned to survive 3.12 and modern urllib3
          'singer-python>=5.13.0'  # Swapped the dead fork for the standard Singer library
      ],
      extras_require={
          'test': [
              'pylint>=2.9.0',
              'pytest>=6.2.0'
          ]
      },
      python_requires='>=3.8',     # Let Pants know modern Python is welcome
      entry_points='''
          [console_scripts]
          tap-twilio=tap_twilio:main
      ''',
      packages=find_packages(),
      package_data={
          'tap_twilio': [
              'schemas/*.json'
          ]
      })
