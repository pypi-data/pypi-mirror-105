import setuptools
from pathlib import Path

setuptools.setup(
    name="gentilpdf",
    version="2.0",
    longdescription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
