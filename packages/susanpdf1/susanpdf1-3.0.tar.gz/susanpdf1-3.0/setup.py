import setuptools
from pathlib import Path

setuptools.setup(
    name="susanpdf1",
    version=3.0,
    long_decription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
