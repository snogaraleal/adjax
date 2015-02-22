#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='django-adjax',
    version='0.1a1',
    description='Django AJAX RPC.',
    long_description=('Easy-to-use AJAX-based RPC mechanism for Django with '
                      'extensible serialization.'),
    url='http://adjax.io',
    license='MIT',
    author='Sebastian Nogara',
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
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ]
)
