from setuptools import *
import os

directory = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(directory, "requirements.txt"), encoding = "utf-8") as file:
    requirements = file.readlines()

with open(os.path.join(directory, "README.md"), encoding = "utf-8") as file:
    long_description = file.read()

setup(
    name = "devplayer",
    version = "0.1.2",
    author = "Devansh Singh",
    author_email = "devanshamity@gmail.com",
    url = "https://github.com/Devansh3712/DevPlayer",
    description = "CLI for playing music and creating playlists",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "MIT",
    packages = find_packages(),
    include_package_data = True,
    entry_points = {
        "console_scripts": [
            "dev=devplayer.__main__:dev"
        ]
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = requirements,
)