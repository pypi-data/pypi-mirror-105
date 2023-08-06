import sys
import codecs
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [ll for ll in f.read().splitlines() if ll]


def long_description():
    with codecs.open('README.rst', 'rb') as readme:
        if not sys.version_info < (3, 0, 0):
            return readme.read().decode('utf-8')


setup(
    name='mdtui',
    version='0.0.2-4',
    description='A TUI to search and download from the new MangaDex API v5',
    long_description=long_description(),
    url='https://git.geraldwu.com/gerald/mdtui',
    author='98WuG',
    license='AGPL-3.0',
    packages=find_packages(exclude=['tests*']),
    entry_points={
        'console_scripts': [
            'mdtui = mdtui.main:main',
        ]
    },
    install_requires=requirements,
)
