#!/usr/bin/env python3
import os
from setuptools import setup
import sys


def enforce_command_blacklist():
    """
    Sanity check to ensure we DO NOT allow publishing our private library
    to the public pypi. Remove this and replace with a custom repository if
    we ever have one, but make sure you are careful not to allow pushing to
    public pypi.
    """
    for cmd in sys.argv[1:]:
        if cmd in ('register', 'upload'):
            raise Exception('You must not publish this library to public pypi')


def readme_content():
    dir = os.path.abspath(os.path.dirname(__file__))
    desc = None
    with open(os.path.join(dir, 'README.md'), 'r') as f:
        desc = f.read()

    return desc


enforce_command_blacklist()

setup(
    name='record_uploader',
    version='0.0.1',
    packages=['record_uploader'],
    entry_points={
        'console_scripts': [
            'record_uploader=record_uploader.cli:main'
        ]
    },
    install_requires=['psycopg2-binary>=2.7.7', 'boto3>=1.9.101'],
    python_requires='>=3.2',
    long_description=readme_content(),
    long_description_content_type='text/markdown'
)
