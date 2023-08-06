import setuptools
from pathlib import Path

setuptools.setup(
    name="Shoayb",
    version=1.0,
    long_describtion=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=['test', 'data'])
)
