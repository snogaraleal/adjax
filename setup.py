#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='django-adjax',
    version='0.5',
    description='Django AJAX RPC.',
    long_description=('Easy-to-use AJAX-based RPC mechanism for Django with '
                      'extensible serialization.'),
    url='http://adjax.io',
    license='MIT',
    author='Sebastian Nogara',
    author_email='snogaraleal@gmail.com',
    packages=find_packages(),
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
        'Programming Language :: Python :: 2',
        'Framework :: Django',
    ]
)
