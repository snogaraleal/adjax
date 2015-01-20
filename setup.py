#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='adjax',
    version='0.0.1',
    description='Django AJAX RPC.',
    long_description=('Django AJAX RPC.'),
    url='http://adjax.io',
    license='MIT',
    author='Sebastián Nogara',
    author_email='snogaraleal@gmail.com',
    packages=[
        'adjax',
        'adjax/conf',
        'adjax/static',
        'adjax/templatetags',
        'adjax/templates',
        'adjax/tests',
        'adjax/utils',
    ],
    package_data={
        '': [
            'templates/adjax/*',
            'static/adjax/*',
        ],
    },
    install_requires=[
        'Django>=1.6.5',
        'six>=1.6.1',
    ],
    include_package_data=True,
    zip_safe=False,
)
