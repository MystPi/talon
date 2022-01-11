import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="talonlang",
    version="1.0.1",
    description="The Talon programming language",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MystPi/talon",
    author="MystPi",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=["talon"],
    package_data={'': ['*.lark']},
    install_requires=["lark", "tinted"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "tal=talon.talon:main",
        ]
    },
)