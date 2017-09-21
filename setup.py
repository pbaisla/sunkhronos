from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sunkhronos',

    version='0.0.1',

    description='Keep two folders on different devices in sync',

    long_description=long_description,

    url='https://github.com/pbaisla/sunkhronos',

    author='Prashant Baisla',
    author_email='prashantbaisla@gmail.com',

    license='License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

    classifiers=[
        'Development Status :: 3 - Alpha',
    ],

    keywords='folder directory sync',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'twisted',
        'watchdog'
    ],

    python_requires='>=3',

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'sunkhronos=sunkhronos:main',
        ],
    },
)

