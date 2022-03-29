from setuptools import setup, find_packages

setup(
    name = 'tenai',
    version = '1.0',
    description = 'Uncover part of the mutuals followers of an instagram private account',
    author = 'novitae',
    url = 'https://github.com/novitae/Pinch',
    license = 'GNU General Public License v3 (GPLv3)',
    classifiers = [
        'Programming Language :: Python :: 3.9',
    ],
    packages = find_packages(),
    install_requires = ['pysimpleig', 'requests'],
    entry_points = {'console_scripts': ['tenai = tenai.core:main']}
)