# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

SCRIPTS = [os.path.join('bin',fn) for fn in os.listdir('bin') if fn.endswith('.py')]
REQUIRED = open('requirements.txt').readlines()

setup(name='social_collector',
    version='0.1',
    description='',
    install_requires=REQUIRED,
    packages=find_packages(),
    #test_suite='test.tests',
    scripts=SCRIPTS,
)