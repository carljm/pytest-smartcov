from os.path import join
from setuptools import setup


long_description = (
    open('README.rst').read() + '\n\n' + open('CHANGES.rst').read())


def get_version():
    with open('smartcov.py') as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip().strip('"\'')


setup(
    name='pytest-smartcov',
    version=get_version(),
    description="Smart coverage plugin for pytest.",
    long_description=long_description,
    author='Carl Meyer',
    author_email='carl@oddbird.net',
    url='https://github.com/carljm/pytest-smartcov/',
    py_modules=['smartcov'],
    install_requires=['coverage>=3.6'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={'pytest11': ['smartcov = smartcov']},
    zip_safe=False,
)
