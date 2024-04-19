# A python setup file for creating python package

from setuptools import setup, find_namespace_packages

setup(
    name='flaskapp',
    packages=find_namespace_packages(),
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
