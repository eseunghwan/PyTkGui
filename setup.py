#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from PyTkGui import __version__

with open("README.md", encoding = "utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md", encoding = "utf-8") as history_file:
    history = history_file.read()

with open("requirements.txt", encoding = "utf-8") as require_file:
    requires = require_file.readlines()

setup(
    author="eseunghwan",
    keywords="tkinter python mvvm gui",
    name="PyTkGui",
    author_email='shlee0920@naver.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="python mvvm gui framework on tkinter",
    entry_points={
        'console_scripts': [
            'pytkgui-cli=PyTkGui.cli:main',
        ],
    },
    install_requires=requires,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    packages=[ "PyTkGui", "PyTkGui/assets", "PyTkGui/core", "PyTkGui/widgets" ],
    package_data={
        "": [ "*.png", "*.zip" ]
    },
    include_package_data=True,
    url='https://github.com/eseunghwan/PyTkGui',
    version=__version__,
    zip_safe=False,
)
