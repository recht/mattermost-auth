#!/usr/bin/env python
from setuptools import setup
from setuptools import find_packages

setup(
    name='mattermost-auth',
    version='1.0.0',
    description=(
        'Utility program for extracting Mattermost auth tokens'
    ),
    author='Joakim Recht',
    author_email='joakim@braindump.dk',
    license='MIT',
    install_requires=['cefpython3', 'click', 'requests'],
    entry_points={
        'console_scripts': [
            'mattermost-auth = mattermost_auth.auth:main'
        ]
    },
)
