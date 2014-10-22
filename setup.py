from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup


setup(
    name='adjax',
    version='0.0.1',
    description='Django AJAX framework.',
    long_description=('Django AJAX framework.'),
    url='http://adjax.io',
    license='MIT',
    author='Sebastián Nogara',
    author_email='snogara@sophilabs.com',
    packages=[
        'adjax',
        'adjax/conf',
        'adjax/static',
        'adjax/templates',
        'adjax/templatetags',
        'adjax/tests',
        'adjax/utils',
    ],
    install_requires=[
        'Django>1.6.5',
        'flake8>2.1.0',
        'pep8>1.5.7',
        'pyflakes>0.8.1',
        'six>1.6.1',
        'django-nose>1.2',
        'coverage>3.7.1',
    ],
    include_package_data=True,
    zip_safe=False,
)
