#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='rivr-rest',
    version='0.1.0',
    description='Library for building REST apis.',
    url='https://github.com/rivrproject/rivr-rest',
    packages=find_packages(),
    install_requires=[
        'rivr',
        'uritemplate',
        'negotiator',
    ],
    author='Kyle Fuller',
    author_email='inbox@kylefuller.co.uk',
    license='BSD',
    classifiers=(
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.2',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'License :: OSI Approved :: BSD License',
    )
)

