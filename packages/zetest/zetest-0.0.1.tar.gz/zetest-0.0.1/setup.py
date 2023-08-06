from glob import glob
from os.path import basename, splitext

from setuptools import setup

setup(
    name="zetest",
    version="0.0.1",
    packages=['test'],
    include_package_data=True,
    zip_safe=False,
)