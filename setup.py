from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.0'
DESCRIPTION = 'python tools to gather, analize and visualize gcov files produced by c++ projects'

# Setting up
setup(
    name="PrettyGcov",
    version=VERSION,
    author="Andrea Casalino",
    author_email="<andrecasa91@gmail.com>",
    packages=find_packages(),
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[],
    keywords=["gcov", "c++", "coverage", "gcda", "gcno"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    url="https://github.com/andreacasalino/PrettyGcov"
)
