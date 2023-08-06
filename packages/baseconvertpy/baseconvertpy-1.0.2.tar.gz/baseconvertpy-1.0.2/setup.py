import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="baseconvertpy",
    version="1.0.2",
    description="A simple way to convert numbers from one base to another.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Siddharth3141/BaseConvertPy",
    author="Siddharth",
    license="MIT",
    keywords=["python", "base", "conversion", "number"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["baseconvertpy"],
    include_package_data=True,
    entry_points={
    },
)
