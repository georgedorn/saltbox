# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='saltbox',
    version='0.1',
    description='Simple Password Storage',
    long_description=readme,
    author='Gordon Morehouse <gordon@morehouse.me>',
    packages=find_packages(exclude=('tests', 'docs')),

    install_requires = [
        'passlib==1.6',
        'SQLAlchemy==0.7.8',
    ],
    tests_require = [
    ],
)
