#!/usr/bin/env python3

from setuptools import setup
from os.path import abspath, join, dirname

with open(join(dirname(abspath(__file__)), 'requirements.txt')) as f:
    requirements = f.readlines()

setup(
    name='padaos',
    version='0.1.5',
    description='A rigid, lightweight, dead-simple intent parser',
    url='http://github.com/MatthewScholefield/padaos',
    author='Matthew Scholefield',
    author_email='matthew331199@gmail.com',
    license='MIT',
    install_requires=requirements,
    py_modules=[
        'padaos'
    ],
    zip_safe=True
)

