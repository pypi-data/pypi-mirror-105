import setuptools
from pathlib import Path

setuptools.setup(
    name="sgdotlite",
    version='1.0.1',
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(
        exclude=["tests", "sgdot_lite/data", "sgdot_lite/examples"]),
    install_requires=Path("requirements.txt").read_text().split("\n")[:-1]
)
