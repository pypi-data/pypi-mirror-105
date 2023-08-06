"""
Setup script for easydubins
"""

import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="easydubins",
    version="1.3.1",
    description="To generate dubin curves projection points.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rsrishav/easydubins",
    author="Rishav",
    author_email="rsrishav0@gmail.com",
    license="GPL3",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["easydubins"],
    include_package_data=True,
    install_requires=["importlib_resources"],
    entry_points={"console_scripts": ["easydubins=easydubins.__main__:main"]},
)