from setuptools import setup, find_packages

setup(
    name = 'privatemutuals',
    version = '1.0',
    description = '',
    author = 'novitae',
    url = 'https://github.com/novitae/InstaPrivateMutuals',
    license = 'GNU General Public License v3 (GPLv3)',
    classifiers = [
        'Programming Language :: Python :: 3.9',
    ],
    packages = find_packages(),
    install_requires = ['pysimpleig', 'requests'],
    entry_points = {'console_scripts': ['pimut = privatemutuals.core:main']}
)