from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Make buttons in pygame with pyg_btn!'

# Setting up
setup(
    name="pyg_btn",
    version=VERSION,
    author="SATAN01 (Shourya sinha)",
    author_email="<shouryasinha001@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'pygame','buttons','game-development'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)