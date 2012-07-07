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

    # M2Crypto probably optional
    install_requires = [
        'passlib==1.6',
        'SQLAlchemy==0.7.8',
        'celery==2.5.5',
        'M2Crypto==0.21.1',
    ],
    tests_require = [
    ],
)
