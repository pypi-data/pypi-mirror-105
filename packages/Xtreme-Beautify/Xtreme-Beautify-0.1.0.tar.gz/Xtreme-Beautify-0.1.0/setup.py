from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.0'
DESCRIPTION = 'beautify the terminal display'
LONG_DESCRIPTION = 'simple tool for beautifying the appearance of the application in the terminal.'

# Setting up
setup(
    name="Xtreme-Beautify",
    version=VERSION,
    author="Exso Kamabay",
    author_email="<lexyong66@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['bs4', 'art', 'url64','string-color','requests'],
    keywords=['python', 'color', 'text', 'font', 'beautifull', 'terminal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)