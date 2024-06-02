"""PyPi vizrecurse setup"""
from pathlib import Path

from setuptools import setup, find_packages

setup(
    name='vizrecurse',
    version='1.1.3',
    author='Cody Pedersen',
    description='Bare bones library to vizualize recursion with one line of code.',
    long_description=(Path(__file__).parent/"README.md").read_text(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
    'Programming Language :: Python :: 3.10',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Intended Audience :: Education'
    ],
    python_requires='>=3.10',
    readme="README.md",
    install_requires=[
        "astroid==3.2.2",
        "contourpy==1.2.1",
        "cycler==0.12.1",
        "dill==0.3.8",
        "fonttools==4.51.0",
        "graphviz==0.20.3",
        "isort==5.13.2",
        "kiwisolver==1.4.5",
        "matplotlib==3.9.0",
        "mccabe==0.7.0",
        "networkx==3.3",
        "numpy==1.26.4",
        "packaging==24.0",
        "pillow==10.3.0",
        "platformdirs==4.2.2",
        "pydot==2.0.0",
        "pygraphviz==1.13",
        "pylint==3.2.2",
        "pyparsing==3.1.2",
        "python-dateutil==2.9.0.post0",
        "six==1.16.0",
        "tomli==2.0.1",
        "tomlkit==0.12.5",
        "typing_extensions==4.12.0"
    ],
    package_data={'vizrecurse': ['py.typed']},
)
