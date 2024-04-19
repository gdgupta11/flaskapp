# A python setup file for creating python package

from setuptools import setup, find_packages

setup(
    name='flaskapp',
    version='2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'pymongo'
    ],
    entry_points={
        'console_scripts': [
            'flaskapp = flaskapp.app:run',
        ],
    },
)
