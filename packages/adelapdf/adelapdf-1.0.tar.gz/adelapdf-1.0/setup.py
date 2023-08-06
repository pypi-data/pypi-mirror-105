import setuptools
from pathlib import Path

setuptools.setup(
    name="adelapdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
# setup.py sdist bdist_wheel - generate distribution packages (before deploy)
